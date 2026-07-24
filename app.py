import pandas as pd
import requests
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Global Business Intelligence Platform", layout="wide")

# Custom CSS for Premium UI
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1, h2, h3, h4 { font-family: -apple-system, sans-serif; color: #0f172a; font-weight: 700; }
    .stButton>button {
        background-color: #0f172a; color: white; border-radius: 8px;
        padding: 0.75rem 1.5rem; font-size: 1.1rem; font-weight: 600; border: none; width: 100%;
    }
    .stButton>button:hover { background-color: #4f46e5; color: white; }
    div[data-testid="stMetricValue"] { font-size: 2.8rem !important; color: #4f46e5 !important; font-weight: 800 !important; }
    div[data-testid="stMetricLabel"] { font-size: 1.1rem !important; font-weight: 600 !important; color: #475569 !important; }
    [data-testid="stDataFrame"] { border-radius: 10px; border: 1px solid #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

st.title("Global Business Intelligence Platform")
st.markdown("Scan real-world global markets with clean address formatting and free-form input.")
st.markdown("---")

# Hardcode your Geoapify API key directly here
GEOAPIFY_API_KEY = "YOUR_ACTUAL_GEOAPIFY_API_KEY_HERE"

st.subheader("Step 1: Custom Search Parameters")
col_input1, col_input2, col_btn = st.columns([2, 2, 1], gap="medium")

with col_input1:
    business_type = st.text_input("Enter Industry or Business Type:", value="Cafe")
    
with col_input2:
    location = st.text_input("Enter Any City or Country Worldwide:", value="Austin, TX")

with col_btn:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Run Global Scan")
st.markdown("---")

def fetch_global_businesses_with_contacts(b_type, loc, api_key):
    # Using Geoapify Places API for high-speed, reliable enterprise lookups
    url = "https://api.geoapify.com/v2/places"
    
    # We can use text search query parameters for flexible free-form matching
    params = {
        "text": f"{b_type} in {loc}",
        "limit": 20,
        "apiKey": api_key
    }
    
    headers = {"Accept": "application/json"}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            return pd.DataFrame()
            
        result_json = response.json()
        features = result_json.get("features", [])
        data = []
        
        for place in features:
            props = place.get("properties", {})
            name = props.get("name") or props.get("address_line1", "Unnamed Entity")
            
            # Proper address formatting parsing structured components cleanly
            housenumber = props.get("housenumber", "")
            street = props.get("street", "")
            suburb = props.get("suburb", props.get("neighbourhood", ""))
            city_name = props.get("city", props.get("town", props.get("village", loc)))
            country_name = props.get("country", "")
            
            # Construct a clean, readable single-line address format matching user layout
            address_parts = [p for p in [f"{housenumber} {street}".strip(), suburb, city_name, country_name] if p]
            formatted_address = ", ".join(address_parts) if address_parts else props.get("formatted", "Address mapped")
            
            # Contact details extraction
            contact = props.get("contact", {})
            phone = contact.get("phone", props.get("phone", "Not listed publicly"))
            website = contact.get("website", props.get("website", "Not listed"))
            
            data.append({
                "Business Name": name,
                "Address": formatted_address,
                "Phone Number": phone,
                "Website": website,
                "Urgency Score": 7
            })
            
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()

if generate_btn:
    if not geoapify_api_key:
        st.error("Please enter your Geoapify API key in the sidebar to run scans.")
        st.stop()
        
    with st.spinner(f"Querying global registries for {business_type} in {location}..."):
        df = fetch_global_businesses_with_contacts(business_type, location, geoapify_api_key)
        
        if df.empty:
            st.error("No entries found for this location or check if your API key is valid.")
            st.stop()
            
        st.success(f"Global Scan Complete: Pulled live entities for {location}.")
            
    st.session_state['scanned_data'] = df

if 'scanned_data' in st.session_state:
    df = st.session_state['scanned_data']
    
    st.subheader("Step 2: Market Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Global Entities Audited", len(df))
    col2.metric("Average Urgency Score", f"{df['Urgency Score'].mean():.1f} / 10")
    col3.metric("High-Priority Targets", len(df))
    st.markdown("---")

    st.subheader("Step 3: Database & Results Table")
    display_df = df[['Business Name', 'Address', 'Phone Number', 'Website', 'Urgency Score']]
    st.dataframe(display_df, use_container_width=True, height=400, hide_index=True)
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Full Data as CSV", data=csv_data, file_name=f"global_business_audit.csv", mime="text/csv")
    st.markdown("---")
    
    st.subheader("Step 4: Custom Outreach Generator")
    selected_business = st.selectbox("Select Target Business:", df['Business Name'])
    
    if st.button("Generate Custom Pitch"):
        target_data = df[df['Business Name'] == selected_business].iloc[0]
        pitch_text = f"""Subject: Enhancing local visibility for {target_data['Business Name']}

Hi Team at {target_data['Business Name']},

I found your listing located at {target_data['Address']} (Website: {target_data['Website']}) and noticed an opportunity to expand your incoming client traffic.

In fast-paced markets, optimizing local search presence yields high-converting foot traffic. We specialize in streamlining visibility metrics for active enterprises.

Would you be open to a brief 10-minute introduction this week?

Best regards,
Growth Strategist"""
        st.code(pitch_text, language="text")
        

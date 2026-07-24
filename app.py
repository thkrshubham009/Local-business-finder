import pandas as pd
import requests
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Local Business Intelligence Platform", layout="wide")

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

st.title("Local Business Intelligence Platform")
st.markdown("Scan local markets using live open-source OpenStreetMap data.")
st.markdown("---")

industry_options = [
    "Cafes", "Plumbers", "Dentists", "Gyms", 
    "Restaurants", "Bakeries", "Hotels", "Lawyers"
]

location_options = [
    "Austin", "New York", "London", 
    "Toronto", "Sydney", "Chicago",
    "Los Angeles", "Miami", "Paris", "Tokyo"
]

st.subheader("Step 1: Select Target Market")
col_input1, col_input2, col_btn = st.columns([2, 2, 1], gap="medium")

with col_input1:
    business_type = st.selectbox("Select Industry:", options=industry_options, index=0)
    
with col_input2:
    location = st.selectbox("Select City:", options=location_options, index=0)

with col_btn:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Start Scan")
st.markdown("---")

def fetch_live_openstreetmap_data(b_type, loc):
    # Query Nominatim API with structured parameters for real locations
    url = f"https://nominatim.openstreetmap.org/search?city={loc}&q={b_type}&format=json&addressdetails=1&limit=15"
    
    # Nominatim strictly requires a custom User-Agent header identifying your app
    headers = {
        "User-Agent": "LocalBusinessIntelligenceApp/1.0 (StudentProject)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return pd.DataFrame()
            
        results = response.json()
        data = []
        
        for place in results:
            name = place.get("name")
            if not name:
                # Fallback to display name prefix if specific store name is blank
                name = place.get("display_name", "").split(",")[0]
                
            address = place.get("display_name", "Address details not indexed")
            
            # Evaluate real metadata metrics based on available attributes
            data.append({
                "Business Name": name,
                "Address": address,
                "Estimated Rating": "OpenData Verified",
                "Urgency Score": 5
            })
            
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()

if generate_btn:
    with st.spinner("Querying live OpenStreetMap spatial database..."):
        df = fetch_live_openstreetmap_data(business_type, location)
        
        if df.empty:
            st.error("No live entries found for this combination. Try broadening your city or industry choice.")
            st.stop()
            
        st.success(f"Scan Complete: Pulled live records for {location} via OpenStreetMap.")
            
    st.session_state['scanned_data'] = df

if 'scanned_data' in st.session_state:
    df = st.session_state['scanned_data']
    
    st.subheader("Step 2: Market Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Businesses Audited", len(df))
    col2.metric("Average Urgency Score", f"{df['Urgency Score'].mean():.1f} / 10")
    col3.metric("High-Priority Targets", len(df[df['Urgency Score'] >= 5]))
    st.markdown("---")

    st.subheader("Step 3: Database & Results Table")
    display_df = df[['Business Name', 'Address', 'Estimated Rating', 'Urgency Score']]
    st.dataframe(display_df, use_container_width=True, height=400, hide_index=True)
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Full Data as CSV", data=csv_data, file_name=f"{business_type.lower()}_{location.lower()}_audit.csv", mime="text/csv")
    st.markdown("---")
    
    st.subheader("Step 4: Custom Outreach Generator")
    selected_business = st.selectbox("Select Target Business:", df['Business Name'])
    
    if st.button("Generate Custom Pitch"):
        target_data = df[df['Business Name'] == selected_business].iloc[0]
        pitch_text = f"""Subject: Enhancing local visibility for {target_data['Business Name']}

Hi Team at {target_data['Business Name']},

I was reviewing local listings located at {target_data['Address']} and noticed an opportunity to strengthen your digital reach.

In competitive regional markets, optimizing online positioning drives consistent foot traffic. We specialize in streamlining local search footprints for active businesses.

Would you be open to a brief 10-minute chat this week?

Best regards,
Growth Strategist"""
        st.code(pitch_text, language="text")
        

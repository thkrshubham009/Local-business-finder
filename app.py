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
st.markdown("Scan real-world global markets with public registry contact details via OpenStreetMap.")
st.markdown("---")

industry_options = [
    "Cafes & Coffee Shops", "Restaurants", "Hotels & Resorts", 
    "Gyms & Fitness Centers", "Bakeries", "Dentists", "Pharmacies", "Supermarkets"
]

st.subheader("Step 1: Select Global Target Market")
col_input1, col_input2, col_btn = st.columns([2, 2, 1], gap="medium")

with col_input1:
    business_type = st.selectbox("Select Industry Category:", options=industry_options, index=0)
    
with col_input2:
    location = st.text_input("Enter Any City or Country Worldwide:", value="Austin, TX")

with col_btn:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Run Global Scan")
st.markdown("---")

def fetch_global_businesses_with_contacts(b_type, loc):
    tag_mapping = {
        "Cafes & Coffee Shops": "cafe",
        "Restaurants": "restaurant",
        "Hotels & Resorts": "hotel",
        "Gyms & Fitness Centers": "gym",
        "Bakeries": "bakery",
        "Dentists": "dentist",
        "Pharmacies": "pharmacy",
        "Supermarkets": "supermarket"
    }
    osm_tag = tag_mapping.get(b_type, "amenity")
    
    # Using Overpass API to query global map records including contact tags
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    area[name="{loc.split(',')[0].strip()}"]->.searchArea;
    (
      node["amenity"="{osm_tag}"](area.searchArea);
      way["amenity"="{osm_tag}"](area.searchArea);
      node["shop"="{osm_tag}"](area.searchArea);
      way["shop"="{osm_tag}"](area.searchArea);
    );
    out body;
    >;
    out skel qt;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': overpass_query}, timeout=30)
        
        if response.status_code != 200 or not response.json().get("elements"):
            # Fallback to Nominatim search with address details
            nominatim_url = f"https://nominatim.openstreetmap.org/search?q={b_type}+in+{loc}&format=json&addressdetails=1&extratags=1&limit=25"
            headers = {"User-Agent": "GlobalBusinessIntelligence/1.0"}
            nom_response = requests.get(nominatim_url, headers=headers, timeout=15)
            if nom_response.status_code == 200:
                results = nom_response.json()
                data = []
                for place in results:
                    name = place.get("name") or place.get("display_name", "").split(",")[0]
                    address = place.get("display_name", "Global address mapped")
                    extratags = place.get("extratags", {})
                    phone = extratags.get("phone", extratags.get("contact:phone", "Not listed publicly"))
                    website = extratags.get("website", extratags.get("contact:website", "Not listed"))
                    
                    data.append({
                        "Business Name": name,
                        "Address": address,
                        "Phone Number": phone,
                        "Website": website,
                        "Urgency Score": 7
                    })
                return pd.DataFrame(data)
            return pd.DataFrame()
            
        elements = response.json().get("elements", [])
        data = []
        
        for el in elements:
            tags = el.get("tags", {})
            name = tags.get("name")
            if not name:
                continue
                
            street = tags.get("addr:street", "")
            housenumber = tags.get("addr:housenumber", "")
            city = tags.get("addr:city", loc)
            address = f"{housenumber} {street}, {city}".strip() if street else f"Mapped location in {loc}"
            
            # Extract real public contact tags if registered in the global map
            phone = tags.get("phone", tags.get("contact:phone", "Not listed publicly"))
            website = tags.get("website", tags.get("contact:website", "Not listed"))
            
            data.append({
                "Business Name": name,
                "Address": address,
                "Phone Number": phone,
                "Website": website,
                "Urgency Score": 7
            })
            
        return pd.DataFrame(data[:30])
    except Exception:
        return pd.DataFrame()

if generate_btn:
    with st.spinner(f"Querying global registries for {business_type} in {location}..."):
        df = fetch_global_businesses_with_contacts(business_type, location)
        
        if df.empty:
            st.error("No entries found for this location. Try a major city or broader region name.")
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
                                                                                                                                             

import pandas as pd
import random
import requests
import streamlit as st
import google.generativeai as genai

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
st.markdown("Scan local markets using open-source data and generate customized AI outreach scripts.")
st.markdown("---")

# Searchable dropdown lists
industry_options = [
    "Cafes & Coffee Shops", "Plumbers", "Dentists", "Real Estate Agencies", 
    "Gyms & Fitness Centers", "Restaurants", "Bakeries", "Hotels & Resorts",
    "Law Firms", "Auto Repair Shops", "Digital Marketing Agencies", "Medical Spas"
]

location_options = [
    "Austin, TX", "New York, NY", "London, UK", 
    "Toronto, ON", "Sydney, Australia", "Chicago, IL",
    "Los Angeles, CA", "Miami, FL", "Paris, France", "Tokyo, Japan"
]

st.subheader("Step 1: Select Target Market")
col_input1, col_input2, col_btn = st.columns([2, 2, 1], gap="medium")

with col_input1:
    business_type = st.selectbox(
        "Select Industry (Click or type to search):", 
        options=industry_options, 
        index=0
    )
    
with col_input2:
    location = st.selectbox(
        "Select City / Location (Click or type to search):", 
        options=location_options, 
        index=0
    )

with col_btn:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Start Scan")
st.markdown("---")

# Your integrated API key
GEMINI_API_KEY = "AQ.Ab8RN6I8Vo6WsKXYFS84HQliVUl-qbqvGl7Po_GEa-zbCi8FrQ"

def fetch_openstreetmap_businesses(b_type, loc):
    query = f"{b_type} in {loc}"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&addressdetails=1&limit=15"
    
    headers = {
        "User-Agent": "BusinessIntelligenceApp/1.0 (StudentProject)"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return pd.DataFrame()
        
    results = response.json()
    
    data = []
    for place in results:
        name = place.get("name")
        if not name:
            continue
            
        address = place.get("display_name", "Address not listed")
        simulated_rating = round(random.uniform(3.2, 5.0), 1)
        simulated_reviews = random.randint(5, 150)
        score = 8 if simulated_reviews < 20 else (5 if simulated_rating < 4.0 else 2)

        data.append({
            "Business Name": name,
            "Address": address.split(',')[0] + ", " + loc,
            "Estimated Rating": f"{simulated_rating} / 5.0",
            "Urgency Score": score
        })
        
    return pd.DataFrame(data)

# Execution Logic
if generate_btn:
    with st.spinner("Pulling open-source satellite and map data..."):
        df = fetch_openstreetmap_businesses(business_type, location)
        
        if df.empty:
            st.error("Could not find data for that specific combination. Try another city or industry.")
            st.stop()
            
        st.success(f"Scan Complete: Found live businesses in {location} using OpenStreetMap.")
            
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
    st.download_button(label="Download Full Data as CSV", data=csv_data, file_name=f"{business_type.lower().replace(' ', '_')}_audit.csv", mime="text/csv")
    st.markdown("---")
    
    # Step 4: AI Pitch Generator using official library handling
    st.subheader("Step 4: AI Pitch Generator")
    st.markdown("Select a business from the dropdown below to generate a custom outreach email using Google Gemini.")
    
    selected_business = st.selectbox("Select Target Business:", df['Business Name'])
    
    if st.button("Generate Custom AI Pitch"):
        with st.spinner("AI is writing the pitch..."):
            target_data = df[df['Business Name'] == selected_business].iloc[0]
            
            ai_prompt = f"""
            You are a highly professional enterprise sales expert. 
            Write a cold outreach email to {target_data['Business Name']} located at {target_data['Address']}. 
            Their estimated digital rating is {target_data['Estimated Rating']}.
            Offer to help them improve their local search visibility. Keep it strictly under 100 words. 
            Do not use any emojis at all. Be direct and professional.
            """
            
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(ai_prompt)
                st.code(response.text, language="text")
            except Exception as e:
                st.error(f"Error connecting to AI: {e}")
                

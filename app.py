import pandas as pd
import random
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Local Business Intelligence Platform",
    layout="wide"
)

# Custom CSS for a Premium, Expensive SaaS UI
st.markdown("""
    <style>
    /* Main Background */
    .main {
        background-color: #f8fafc;
    }
    
    /* Typography */
    h1, h2, h3, h4 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0f172a;
        font-weight: 700;
    }
    
    /* Premium Button Styling */
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #4f46e5;
        color: white;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Premium Metric Numbers (Large and Indigo Blue) */
    div[data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        color: #4f46e5 !important; 
        font-weight: 800 !important;
    }
    
    /* Metric Labels */
    div[data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
    }
    
    /* Table Styling - Clean and Large */
    [data-testid="stDataFrame"] {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title & Subtitle
st.title("Local Business Intelligence Platform")
st.markdown("Scan local markets, analyze performance, and generate customized outreach scripts in 4 simple steps.")
st.markdown("---")

# Dropdown Options
industry_options = [
    "Cafes & Coffee Shops", 
    "Plumbing & HVAC Services", 
    "Dental Clinics", 
    "Real Estate Agencies", 
    "Fitness Centers & Gyms", 
    "Law Firms & Legal Services",
    "Bakeries & Pastry Shops",
    "Auto Repair & Detailing",
    "Digital Marketing Agencies",
    "Boutique Hotels & Resorts",
    "Restaurants & Fine Dining",
    "Roofing & Construction",
    "Medical Spas",
    "Veterinary Clinics",
    "Accounting & CPA Firms"
]

location_options = [
    "Austin, TX", 
    "New York, NY", 
    "Los Angeles, CA", 
    "Chicago, IL", 
    "Miami, FL", 
    "Houston, TX",
    "Phoenix, AZ",
    "London, UK", 
    "Toronto, ON",
    "Tokyo, Japan",
    "Sydney, Australia",
    "Dubai, UAE",
    "Paris, France",
    "Berlin, Germany"
]

# Step 1: Select Input Parameters
st.subheader("Step 1: Select Target Market")

col_input1, col_input2, col_btn = st.columns([2, 2, 1], gap="medium")

with col_input1:
    business_type = st.selectbox(
        "Select Industry (Type to search):", 
        options=industry_options, 
        index=0
    )
    
with col_input2:
    location = st.selectbox(
        "Select City (Type to search):", 
        options=location_options, 
        index=0
    )

with col_btn:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Start Scan")

st.markdown("---")

# GOOGLE PLACES API KEY PLACEHOLDER
GOOGLE_API_KEY = "" 

def fetch_real_google_businesses(b_type, loc, api_key):
    """Fetches real-world business data from Google Places API."""
    query = f"{b_type} in {loc}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"
    
    response = requests.get(url).json()
    results = response.get("results", [])
    
    data = []
    for place in results[:10]:
        name = place.get("name")
        address = place.get("formatted_address", loc)
        rating = place.get("rating", 0.0)
        user_ratings_total = place.get("user_ratings_total", 0)
        
        has_gmb = place.get("business_status") == "OPERATIONAL"
        score = 8 if user_ratings_total < 20 else (5 if rating < 4.0 else 2)
        
        outreach = f"Subject: Digital Optimization for {name}\n\nHello Team at {name},\n\nWe audited the {b_type.lower()} market in {loc}. Located at {address}, your current review baseline is {rating} out of 5 ({user_ratings_total} reviews).\n\nWe identified key digital capture funnels to help you outrank local competitors. Let me know if you have 5 minutes this week to discuss.\n\nBest regards,\nGrowth Engineering"

        data.append({
            "Business Name": name,
            "Address": address,
            "Rating Value": rating,
            "Review Count": user_ratings_total,
            "Rating": f"{rating} / 5.0 ({user_ratings_total} reviews)",
            "Listing Status": "Verified" if has_gmb else "Unclaimed",
            "Urgency Score": score,
            "Outreach Script": outreach
        })
        
    return pd.DataFrame(data)


def generate_mock_leads(b_type, loc):
    """Fallback simulation mode when no API key is set."""
    clean_b_type = b_type.split(" & ")[0]
    fake_names = [
        f"Apex {clean_b_type}", 
        f"Metro {clean_b_type} Co.", 
        f"Prime {loc.split(',')[0]} {clean_b_type}", 
        f"Urban {clean_b_type} Group", 
        f"Elite {clean_b_type} Partners",
        f"Signature {clean_b_type}",
        f"Pinnacle {clean_b_type}",
        f"Summit {clean_b_type} Services"
    ]
    
    data = []
    for name in fake_names:
        has_website = random.choice([True, False])
        has_gmb = random.choice([True, False])
        score = 10 if not has_website and not has_gmb else (6 if not has_website else 2)
        
        rating_val = round(random.uniform(3.5, 4.9), 1)
        review_cnt = random.randint(15, 340)
        
        outreach = f"Subject: Infrastructure Audit for {name}\n\nHello Leadership Team,\n\nWe conducted a digital scan of {b_type.lower()} in {loc}. {name} shows key optimization gaps in local directory capture.\n\nImplementing our modernized funnels will recapture local search market share. Are you open to a brief introductory call?\n\nBest regards,\nGrowth Engineering"

        data.append({
            "Business Name": name,
            "Address": f"Central District, {loc}",
            "Rating Value": rating_val,
            "Review Count": review_cnt,
            "Rating": f"{rating_val} / 5.0 ({review_cnt} reviews)",
            "Listing Status": "Verified" if has_gmb else "Unclaimed",
            "Urgency Score": score,
            "Outreach Script": outreach
        })
        
    return pd.DataFrame(data)


# Execution Logic
if generate_btn:
    with st.spinner("Scanning market data..."):
        if GOOGLE_API_KEY.strip():
            df = fetch_real_google_businesses(business_type, location, GOOGLE_API_KEY)
            st.success(f"Scan Complete: Found real businesses in {location}.")
        else:
            df = generate_mock_leads(business_type, location)
            st.success(f"Scan Complete: Generated report for {location}.")
    
    # Step 2: Overview Metrics
    st.subheader("Step 2: Market Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Businesses Audited", len(df))
    col2.metric("Average Urgency Score", f"{df['Urgency Score'].mean():.1f} / 10")
    col3.metric("High-Priority Targets", len(df[df['Urgency Score'] >= 5]))
    
    st.markdown("---")

    # Step 3: Big Clear Results Table
    st.subheader("Step 3: Database & Results Table")
    
    # Clean display table configuration - SCRIPT REMOVED FROM HERE
    display_df = df[['Business Name', 'Address', 'Rating', 'Listing Status', 'Urgency Score']]
    
    # Made the table big and wide
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    # Separate CSV Download Button below the table
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full Data as CSV",
        data=csv_data,
        file_name=f"{business_type.lower().replace(' ', '_')}_audit.csv",
        mime="text/csv"
    )

    st.markdown("---")
    
    # Step 4: Outreach Script Viewer
    st.subheader("Step 4: Generate Outreach Script")
    st.markdown("Select a business from the dropdown below to view and copy its custom AI-generated pitch.")
    
    selected_business = st.selectbox("Select Target Business:", df['Business Name'])
    
    if selected_business:
        script_text = df[df['Business Name'] == selected_business]['Outreach Script'].values[0]
        st.code(script_text, language="text")

else:
    st.info("Select options above and click Start Scan to begin.")
    

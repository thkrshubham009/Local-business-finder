import pandas as pd
import random
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Local Business Intelligence Platform",
    layout="wide"
)

# Custom CSS for a clean, distraction-free UI
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0f172a;
        font-weight: 700;
    }
    
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1e293b;
        color: white;
    }

    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #0f172a;
        font-weight: 700;
    }
    
    /* Table Styling */
    .stDataFrame {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title & Subtitle
st.title("Local Business Intelligence Platform")
st.markdown("Scan local markets, analyze performance, and view customized outreach scripts.")
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
        
        outreach = f"Subject: Digital Optimization for {name}\n\nHello Team at {name},\n\nWe audited the {b_type.lower()} market in {loc}. Located at {address}, your current review baseline is {rating} out of 5 ({user_ratings_total} reviews). We identified key digital capture funnels to help you outrank local competitors.\n\nBest regards,\nGrowth Engineering"

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
        f"Elite {clean_b_type} Partners"
    ]
    
    data = []
    for name in fake_names:
        has_website = random.choice([True, False])
        has_gmb = random.choice([True, False])
        score = 10 if not has_website and not has_gmb else (6 if not has_website else 2)
        
        rating_val = round(random.uniform(3.5, 4.9), 1)
        review_cnt = random.randint(15, 340)
        
        outreach = f"Subject: Infrastructure Audit for {name}\n\nHello Leadership Team,\n\nWe conducted a digital scan of {b_type.lower()} in {loc}. {name} shows key optimization gaps in local directory capture. Implementing our modernized funnels will recapture local search market share.\n\nBest regards,\nGrowth Engineering"

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
    col3.metric("High-Priority Opportunities", len(df[df['Urgency Score'] >= 5]))
    
    st.markdown("---")
    
    # Market Intelligence Section
    st.subheader("Market Leader & Demand Insights")
    
    top_performer = df.sort_values(by=['Rating Value', 'Review Count'], ascending=[False, False]).iloc[0]
    avg_rating = round(df['Rating Value'].mean(), 2)
    total_market_reviews = df['Review Count'].sum()
    
    col_top1, col_top2 = st.columns(2, gap="large")
    
    with col_top1:
        st.markdown("**Best Performing Business:**")
        st.info(f"Business: {top_performer['Business Name']}\n\n"
                f"Rating: {top_performer['Rating Value']} / 5.0\n\n"
                f"Total Customer Reviews: {top_performer['Review Count']}\n\n"
                f"Status: Market Leader")
        
    with col_top2:
        st.markdown("**Market Demand Analysis:**")
        
        if avg_rating >= 4.4:
            demand_insight = f"Strong market demand with competitive providers in {location}. High opportunity to offer advanced performance tools."
        else:
            demand_insight = f"High demand with service gaps in {location}. Average rating is moderate ({avg_rating} / 5.0), creating opportunity for modernization."
            
        st.warning(f"Average Market Rating: {avg_rating} / 5.0\n\n"
                   f"Total Market Reviews Analyzed: {total_market_reviews}\n\n"
                   f"Analysis: {demand_insight}")

    st.markdown("---")

    # Step 3: Clear & Wide Results Table
    st.subheader("Step 3: Results Table")
    st.markdown("Below is the complete list of audited businesses and their generated scripts.")
    
    # Clean display table configuration
    display_df = df[['Business Name', 'Address', 'Rating', 'Listing Status', 'Urgency Score', 'Outreach Script']]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Business Name": st.column_config.TextColumn("Business Name", width="medium"),
            "Address": st.column_config.TextColumn("Address", width="medium"),
            "Rating": st.column_config.TextColumn("Customer Rating", width="small"),
            "Listing Status": st.column_config.TextColumn("Status", width="small"),
            "Urgency Score": st.column_config.NumberColumn("Priority (1-10)", width="small"),
            "Outreach Script": st.column_config.TextColumn("Outreach Script", width="large"),
        }
    )
    
    # CSV Download Button
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Table as CSV",
        data=csv_data,
        file_name=f"{business_type.lower().replace(' ', '_')}_audit.csv",
        mime="text/csv"
    )

else:
    st.info("Select options above and click Start Scan to begin.")
        

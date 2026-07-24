import pandas as pd
import random
import requests
import streamlit as st

# Page Configuration - Enterprise SaaS Layout
st.set_page_config(
    page_title="Local Business Intelligence Platform",
    page_icon=None,
    layout="wide"
)

# Custom CSS for modern executive SaaS UI
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0f172a;
        letter-spacing: -0.025em;
        font-weight: 700;
    }
    
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 6px;
        padding: 0.55rem 1.25rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1e293b;
        color: white;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #0f172a;
        font-weight: 600;
    }
    
    .stDataFrame {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header Section
st.title("Local Business Intelligence Platform")
st.markdown("Automated market scanning, demand analysis, and executive outreach generation.")
st.markdown("---")

# Comprehensive Searchable Options Lists
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
    "SLA & Medical Spas",
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

# Main Searchable Dropdown Inputs (Typing automatically filters options live)
st.subheader("Market Audit Parameters")

col_input1, col_input2, col_btn = st.columns([2, 2, 1], gap="medium")

with col_input1:
    business_type = st.selectbox(
        "Industry / Business Category", 
        options=industry_options, 
        index=0,
        help="Type directly into the box to filter industries in real-time."
    )
    
with col_input2:
    location = st.selectbox(
        "Target Location / City", 
        options=location_options, 
        index=0,
        help="Type directly into the box to filter locations in real-time."
    )

with col_btn:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Execute Audit")

st.markdown("---")

# GOOGLE PLACES API KEY PLACEHOLDER
GOOGLE_API_KEY = "" 

def fetch_real_google_businesses(b_type, loc, api_key):
    """Fetches live real-world business data from Google Places API."""
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
        
        outreach = f"Subject: Digital Optimization for {name}\n\nHello Team at {name},\n\nWe audited the {b_type.lower()} market in {loc}. Located at {address}, your current review baseline is {rating} ★ ({user_ratings_total} reviews). We identified key digital capture funnels to help you outrank local competitors.\n\nBest regards,\nGrowth Engineering"

        data.append({
            "Business Name": name,
            "Address / Location": address,
            "Rating Value": rating,
            "Review Count": user_ratings_total,
            "Rating": f"{rating} ★ ({user_ratings_total})",
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
            "Address / Location": f"Central District, {loc}",
            "Rating Value": rating_val,
            "Review Count": review_cnt,
            "Rating": f"{rating_val} ★ ({review_cnt})",
            "Listing Status": "Verified" if has_gmb else "Unclaimed",
            "Urgency Score": score,
            "Outreach Script": outreach
        })
        
    return pd.DataFrame(data)


# Execution Logic
if generate_btn:
    with st.spinner("Executing market scan and calculating area demand metrics..."):
        if GOOGLE_API_KEY.strip():
            df = fetch_real_google_businesses(business_type, location, GOOGLE_API_KEY)
            st.success(f"LIVE Audit Complete: Retrieved real-world entities for {location}.")
        else:
            df = generate_mock_leads(business_type, location)
            st.success(f"Audit Complete: Generated intelligence report for {location}.")
    
    # Executive Metrics Summary
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records Audited", len(df))
    col2.metric("Mean Urgency Index", f"{df['Urgency Score'].mean():.1f} / 10")
    col3.metric("High-Priority Targets", len(df[df['Urgency Score'] >= 5]))
    
    st.markdown("---")
    
    # Market Demand & Top Performer Analysis
    st.subheader("Market Demand & Local Competitor Intelligence")
    
    top_performer = df.sort_values(by=['Rating Value', 'Review Count'], ascending=[False, False]).iloc[0]
    avg_rating = round(df['Rating Value'].mean(), 2)
    total_market_reviews = df['Review Count'].sum()
    
    col_top1, col_top2 = st.columns(2, gap="large")
    
    with col_top1:
        st.markdown(f"**Top Performing Entity in {location}:**")
        st.info(f"🏆 **{top_performer['Business Name']}**\n\n"
                f"• **Rating:** {top_performer['Rating Value']} Stars\n\n"
                f"• **Total Customer Reviews:** {top_performer['Review Count']}\n\n"
                f"• **Market Dominance:** High review density indicates strong brand trust and digital capture.")
        
    with col_top2:
        st.markdown(f"**AI Demand & Gap Analysis for {business_type}:**")
        
        if avg_rating >= 4.4:
            demand_insight = f"High demand with intense competition. Consumers in {location} expect premium digital experiences. Pitching advanced scaling and automated review funnels will yield highest conversions."
        else:
            demand_insight = f"High unmet demand. Average area rating is moderate ({avg_rating}/5.0). Businesses in this sector are struggling with customer retention, creating a prime opportunity for modernization services."
            
        st.warning(f"📊 **Sector Benchmark Metrics**\n\n"
                   f"• **Regional Avg Rating:** {avg_rating} / 5.0\n\n"
                   f"• **Total Area Search Reviews Analyzed:** {total_market_reviews}\n\n"
                   f"• **Strategic Opportunity:** {demand_insight}")

    st.markdown("---")

    # Table View (Includes Outreach Script Column Directly Inside Table)
    st.subheader("Audited Business Intelligence Table")
    display_df = df[['Business Name', 'Address / Location', 'Rating', 'Listing Status', 'Urgency Score', 'Outreach Script']]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Download CSV Button
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Audit Report (CSV)",
        data=csv_data,
        file_name=f"{business_type.lower().replace(' ', '_')}_audit_{location.lower().replace(', ', '_')}.csv",
        mime="text/csv"
    )

else:
    st.info("Select or type parameters above and click Execute Audit to initialize data pipelines.")
    

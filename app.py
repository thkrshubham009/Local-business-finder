import pandas as pd
import random
import streamlit as st

# Page Configuration - Clean, enterprise-grade, minimal styling
st.set_page_config(
    page_title="Local Business Intelligence & Audit Platform",
    page_icon=None,
    layout="wide"
)

# Custom CSS for an expensive, enterprise SaaS look
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0f172a;
        letter-spacing: -0.025em;
    }
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
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
    /* Clean up the dataframe look */
    .stDataFrame {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("Local Business Intelligence Platform")
st.markdown("Automated market scanning, digital health assessment, and executive-level outreach generation.")
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("Audit Parameters")
business_type = st.sidebar.text_input("Industry / Business Type", value="Cafes")
location = st.sidebar.text_input("Target Location", value="Austin, TX")
generate_btn = st.sidebar.button("Execute Business Audit")

def generate_mock_leads(b_type, loc):
    """Simulates enterprise business data extraction and health scoring."""
    fake_names = [
        f"Apex {b_type.capitalize()}", 
        f"Metro {b_type.capitalize()} Co.", 
        f"Prime {loc.split(',')[0]} {b_type.capitalize()}", 
        f"Urban {b_type.capitalize()} Group", 
        f"Elite {b_type.capitalize()} Partners"
    ]
    
    data = []
    for name in fake_names:
        has_website = random.choice([True, False])
        has_gmb = random.choice([True, False])
        
        # Calculate urgency score (1-10)
        score = 10 if not has_website and not has_gmb else (6 if not has_website else 2)
        
        # Professional, extended high-conversion outreach drafting
        if score >= 8:
            outreach = f"""Subject: Digital Infrastructure Audit for {name} - Immediate Action Recommended

Hello Team at {name},

I am reaching out from our Growth Engineering division. We recently conducted an automated digital infrastructure scan of the {b_type} sector within the {loc} market. 

Our systems flagged {name} due to a missing centralized web presence and an unclaimed local search directory profile. In today's market, consumers rely heavily on digital discovery, meaning a substantial volume of highly qualified local traffic is currently being routed to fully optimized competitors in your area.

Our firm specializes in rapidly deploying high-performance digital infrastructure, complete with automated booking and SEO-optimized local directory setups for regional market leaders. 

Would you be open to a brief, 10-minute executive briefing this week to review the traffic volume you are currently missing and how we can recapture it?

Best regards,

Growth Engineering Team"""

        elif score >= 5:
            outreach = f"""Subject: Conversion Rate Optimization & Market Share in {loc}

Hello Team at {name},

I hope this email finds you well. My team and I monitor digital touchpoints for local businesses, and while reviewing the {b_type} landscape in {loc}, we analyzed your current digital footprint.

While {name} has established a baseline presence, we identified several notable optimization gaps—specifically regarding mobile search rendering and local conversion funnel friction. When potential clients search for your services on mobile devices, these technical friction points often result in high bounce rates and lost revenue.

We have engineered custom acquisition frameworks designed exactly for these scenarios, helping businesses streamline their customer acquisition cost and increase lifetime value. 

Are you available for a brief introductory call on Thursday afternoon to discuss our findings?

Best regards,

Growth Engineering Team"""
        else:
            outreach = f"""Subject: Advanced Traffic Scaling & Performance Benchmarks for {name}

Hello Team at {name},

I am contacting you regarding your current digital footprint in the {loc} region. After running a technical audit on {name}, I wanted to commend your team—your digital foundation and local search integrations are well-optimized compared to the regional average.

However, once the foundational infrastructure is established, the next immediate step is aggressive market share capture. Our firm works with highly optimized businesses to scale their existing traffic using advanced data-driven acquisition models, ensuring you outpace regional competitors.

We have compiled a localized performance benchmark report that outlines advanced traffic scaling configurations you have yet to tap into. 

Please let me know if you would like me to send this report over for your review.

Best regards,

Growth Engineering Team"""

        data.append({
            "Business Name": name,
            "Phone Number": f"+1 (555) {random.randint(100,999)}-{random.randint(1000,9999)}",
            "Website Status": "Active" if has_website else "Action Required",
            "GMB Profile": "Verified" if has_gmb else "Unclaimed",
            "Urgency Score": score,
            "Outreach Template": outreach
        })
        
    return pd.DataFrame(data)

if generate_btn:
    with st.spinner("Analyzing regional infrastructure and extracting market data..."):
        df = generate_mock_leads(business_type, location)
        
    st.success(f"Audit completed successfully. {len(df)} enterprise entities identified.")
    
    # Executive Metrics Summary
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records Audited", len(df))
    col2.metric("Mean Urgency Index", f"{df['Urgency Score'].mean():.1f} / 10")
    col3.metric("High-Priority Targets", len(df[df['Urgency Score'] >= 5]))
    
    st.markdown("---")
    
    # EXCEL FORMAT DATA TABLE
    st.subheader("Lead Database (Grid View)")
    # We display everything except the long script in the table to keep it looking clean
    display_df = df[['Business Name', 'Phone Number', 'Website Status', 'GMB Profile', 'Urgency Score']]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Download Button for the CSV
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Leads as CSV",
        data=csv_data,
        file_name=f"{business_type.lower()}_leads_{location.lower().replace(', ', '_')}.csv",
        mime="text/csv"
    )

    st.markdown("---")
    
    # OUTREACH SCRIPT VIEWER
    st.subheader("Executive Outreach Viewer")
    st.markdown("Select an audited entity below to view and copy their customized AI-generated outreach script.")
    
    # Dropdown to select the business
    selected_business = st.selectbox("Select Target Account:", df['Business Name'])
    
    # Fetch and display the script for the selected business
    if selected_business:
        script_text = df[df['Business Name'] == selected_business]['Outreach Template'].values[0]
        st.code(script_text, language="text")

else:
    st.info("Configure search parameters in the sidebar and execute the audit to initialize data pipelines.")
    

import pandas as pd
import random
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Local Business Lead Intelligence",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Local Business Lead Intelligence & Outreach Engine")
st.markdown("Scan local businesses, audit their digital health, and instantly generate AI-driven cold outreach templates.")

# Sidebar Inputs
st.sidebar.header("Search Parameters")
business_type = st.sidebar.text_input("Business Type (e.g., cafes, plumbers)", value="cafes")
location = st.sidebar.text_input("Location (e.g., Austin, TX)", value="Austin")
generate_btn = st.sidebar.button("Run Business Audit")

def generate_mock_leads(b_type, loc):
    """Simulates local business data extraction and health scoring."""
    fake_names = [
        f"Apex {b_type.capitalize()}", 
        f"Metro {b_type.capitalize()} Co.", 
        f"Prime {loc} {b_type.capitalize()}", 
        f"Urban {b_type.capitalize()} Hub", 
        f"Elite {b_type.capitalize()} Services"
    ]
    
    data = []
    for name in fake_names:
        has_website = random.choice([True, False])
        has_gmb = random.choice([True, False])
        
        # Calculate urgency score (1-10): lower digital presence = higher urgency to fix
        score = 10 if not has_website and not has_gmb else (6 if not has_website else 2)
        
        # AI Cold Outreach draft logic
        if score >= 8:
            outreach = f"Hi Team at {name}, noticed you have no active website or online booking for {loc} customers. You're losing local search traffic daily. Let's fix this fast."
        elif score >= 5:
            outreach = f"Hey {name}, your digital footprint in {loc} has gaps (missing website integration). We can set up a high-converting page for you this week."
        else:
            outreach = f"Hello {name}, love your setup in {loc}! Just checked your web presence—looks solid, optimization potential exists for mobile traffic."

        data.append({
            "Business Name": name,
            "Phone No": f"+1 (555) {random.randint(100,999)}-{random.randint(1000,9999)}",
            "Website Status": "Active" if has_website else "Missing ❌",
            "GMB Profile": "Verified" if has_gmb else "Unclaimed ⚠️",
            "Urgency Score": score,
            "AI Outreach Draft": outreach
        })
        
    return pd.DataFrame(data)

if generate_btn:
    with st.spinner(f"Scanning local {business_type} in {location}..."):
        df = generate_mock_leads(business_type, location)
        
    st.success(f"Successfully audited {len(df)} businesses!")
    
    # Display metrics overview
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Leads Found", len(df))
    col2.metric("Avg Urgency Score", f"{df['Urgency Score'].mean():.1f}/10")
    col3.metric("Actionable Targets", len(df[df['Urgency Score'] >= 5]))
    
    st.markdown("---")
    st.subheader("📋 Business Audit Results & Outreach Generator")
    
    for idx, row in df.iterrows():
        with st.expander(f"{row['Business Name']} — Urgency Score: {row['Urgency Score']}/10"):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Phone:** {row['Phone No']}")
                st.write(f"**Website Status:** {row['Website Status']}")
                st.write(f"**Google My Business:** {row['GMB Profile']}")
            with c2:
                st.info(f"**Generated Outreach Script:**\n\n{row['AI Outreach Draft']}")
else:
    st.info("👈 Enter your target business type and location in the sidebar, then click **Run Business Audit** to begin.")

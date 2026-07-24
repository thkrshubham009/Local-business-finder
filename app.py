import pandas as pd
import requests
import streamlit as st
from urllib.parse import urljoin

# ----------------------------
# CONFIG
# ----------------------------

st.set_page_config(
    page_title="Global Business Intelligence Platform",
    layout="wide"
)

GEOAPIFY_API_KEY = st.secrets.get("GEOAPIFY_API_KEY", "")

# ----------------------------
# UI
# ----------------------------

st.title("Global Business Intelligence Platform")
st.markdown(
    "Search businesses worldwide using Geoapify and identify businesses with websites and contact pages."
)

st.divider()

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    business_type = st.text_input(
        "Business Type",
        value="Cafe"
    )

with col2:
    location = st.text_input(
        "Location",
        value="Austin, TX"
    )

with col3:
    st.write("")
    st.write("")
    run_scan = st.button("Run Scan")

# ----------------------------
# HELPERS
# ----------------------------

CONTACT_PATHS = [
    "/contact",
    "/contact-us",
    "/contactus",
    "/about",
    "/about-us"
]


def normalize_website(url):
    if not url or url == "Not listed":
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def check_contact_page(website):
    website = normalize_website(website)

    if not website:
        return "No Website"

    try:
        r = requests.get(
            website,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if r.status_code >= 400:
            return "Website Unreachable"

        for path in CONTACT_PATHS:
            test_url = urljoin(website, path)

            try:
                resp = requests.get(
                    test_url,
                    timeout=5,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

                if resp.status_code == 200:
                    return "Contact Page Found"

            except Exception:
                pass

        return "Website Found"

    except Exception:
        return "Website Unreachable"


def calculate_urgency(website, phone):
    score = 5

    if not website or website == "Not listed":
        score += 3

    if not phone or phone == "Not listed":
        score += 2

    return min(score, 10)


@st.cache_data(ttl=3600)
def fetch_businesses(business_type, location, api_key):

    url = "https://api.geoapify.com/v2/places"

    params = {
        "text": f"{business_type} in {location}",
        "limit": 50,
        "apiKey": api_key
    }

    response = requests.get(url, params=params, timeout=15)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()
    features = data.get("features", [])

    rows = []

    for place in features:

        props = place.get("properties", {})
        contact = props.get("contact", {})

        name = (
            props.get("name")
            or props.get("address_line1")
            or "Unnamed Business"
        )

        address = (
            props.get("formatted")
            or "Address unavailable"
        )

        phone = (
            contact.get("phone")
            or props.get("phone")
            or "Not listed"
        )

        website = (
            contact.get("website")
            or props.get("website")
            or "Not listed"
        )

        contact_status = check_contact_page(website)

        urgency = calculate_urgency(
            website,
            phone
        )

        rows.append(
            {
                "Business Name": name,
                "Address": address,
                "Phone Number": phone,
                "Website": website,
                "Website Status": contact_status,
                "Urgency Score": urgency
            }
        )

    return pd.DataFrame(rows)

# ----------------------------
# SEARCH
# ----------------------------

if run_scan:

    if not GEOAPIFY_API_KEY:
        st.error(
            "Add GEOAPIFY_API_KEY to Streamlit secrets."
        )
        st.stop()

    with st.spinner("Scanning businesses..."):

        df = fetch_businesses(
            business_type,
            location,
            GEOAPIFY_API_KEY
        )

    if df.empty:
        st.warning("No businesses found.")
        st.stop()

    st.session_state["results"] = df

# ----------------------------
# RESULTS
# ----------------------------

if "results" in st.session_state:

    df = st.session_state["results"]

    st.subheader("Market Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Businesses Found",
        len(df)
    )

    c2.metric(
        "With Website",
        len(df[df["Website"] != "Not listed"])
    )

    c3.metric(
        "Average Urgency",
        round(df["Urgency Score"].mean(), 1)
    )

    st.divider()

    st.subheader("Results")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv_data

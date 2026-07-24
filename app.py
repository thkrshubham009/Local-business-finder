import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Business Search", layout="wide")
st.title("Business Search")

API_KEY = st.secrets.get("GEOAPIFY_API_KEY","")

business = st.text_input("Business type","Cafe")
location = st.text_input("Location","Austin, TX")

@st.cache_data
def geocode(q):
    r=requests.get(
        "https://api.geoapify.com/v1/geocode/search",
        params={"text":q,"apiKey":API_KEY},
        timeout=20,
    )
    r.raise_for_status()
    feats=r.json().get("features",[])
    if not feats:
        return None
    c=feats[0]["geometry"]["coordinates"]
    return c[1],c[0]

@st.cache_data
def search(lat,lon,category):
    r=requests.get(
        "https://api.geoapify.com/v2/places",
        params={
            "categories":"commercial",
            "filter":f"circle:{lon},{lat},5000",
            "limit":50,
            "apiKey":API_KEY,
        },
        timeout=20,
    )
    r.raise_for_status()
    rows=[]
    for f in r.json().get("features",[]):
        p=f.get("properties",{})
        name=p.get("name","")
        if category.lower() not in name.lower() and category.lower() not in str(p).lower():
            continue
        rows.append({
            "Business":name,
            "Address":p.get("formatted",""),
            "Phone":p.get("contact",{}).get("phone",""),
            "Website":p.get("contact",{}).get("website",""),
        })
    return pd.DataFrame(rows)

if st.button("Search"):
    if not API_KEY:
        st.error("Set GEOAPIFY_API_KEY in Streamlit secrets.")
    else:
        coords=geocode(location)
        if not coords:
            st.error("Location not found.")
        else:
            df=search(coords[0],coords[1],business)
            if df.empty:
                st.warning("No matching businesses found.")
            else:
                st.dataframe(df,use_container_width=True)
                st.download_button(
                    "Download CSV",
                    df.to_csv(index=False).encode(),
                    "businesses.csv",
                    "text/csv"
                )
                

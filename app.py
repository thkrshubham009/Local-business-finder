import os
import json
import streamlit as st
import pandas as pd
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError, PermissionDenied, ResourceExhausted

# --- Page Configuration ---
st.set_page_config(
    page_title="OpportunityOS – AI Opportunity Navigator",
    page_icon="O",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Clean SaaS Styling (Fixed button visibility, text readability, form buttons, and download button styling) ---
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #0F172A !important;
        color: #111827;
    }
    
    /* Main Content Area Container */
    .main .block-container {
        background-color: #0F172A;
        color: #111827;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Base Typography adjustments for dark canvas background */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    .stMarkdown p, .stMarkdown span, .stMarkdown li {
        color: #F8FAFC !important;
    }

    /* Cards - White background with dark primary and secondary text */
    .roadmap-container, div[data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 24px;
    }

    /* Typography inside white cards */
    .roadmap-container h1, .roadmap-container h2, .roadmap-container h3, .roadmap-container h4, .roadmap-container h5, .roadmap-container h6 {
        color: #111827 !important;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 8px;
        margin-top: 24px;
    }

    .roadmap-container p, .roadmap-container li, .roadmap-container span {
        color: #6B7280 !important;
    }
    
    .roadmap-container strong {
        color: #111827 !important;
    }

    /* Form specific styles */
    div[data-testid="stForm"] label {
        color: #111827 !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stForm"] p, div[data-testid="stForm"] span {
        color: #111827 !important;
    }

    /* Universal Button Styling (Fixes black buttons and ensures white text for all button variants including Download & Submit) */
    .stButton > button, 
    div[data-testid="stFormSubmitButton"] > button, 
    div[data-testid="stDownloadButton"] > button,
    button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        min-height: 48px;
        border: none !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: background-color 0.2s ease;
        opacity: 1 !important;
        visibility: visible !important;
        width: 100%;
    }
    
    .stButton > button *, 
    div[data-testid="stFormSubmitButton"] > button *, 
    div[data-testid="stDownloadButton"] > button *,
    button * {
        color: #FFFFFF !important;
        opacity: 1 !important;
        fill: #FFFFFF !important;
    }

    .stButton > button:hover, 
    div[data-testid="stFormSubmitButton"] > button:hover, 
    div[data-testid="stDownloadButton"] > button:hover,
    button:hover {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }
    
    .stButton > button:hover *, 
    div[data-testid="stFormSubmitButton"] > button:hover *, 
    div[data-testid="stDownloadButton"] > button:hover *,
    button:hover * {
        color: #FFFFFF !important;
    }
    
    /* Inputs */
    input, select, textarea {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }

    /* Navigation Header */
    .nav-header {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        color: #FFFFFF;
    }
    
    /* Developer Profile Card Styling */
    .dev-profile-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Navigation State Management ---
if 'nav_tab' not in st.session_state:
    st.session_state.nav_tab = "Landing"

def set_tab(tab_name):
    st.session_state.nav_tab = tab_name

# --- Top Navigation Bar ---
col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
with col1:
    st.markdown("<div class='nav-header'>OpportunityOS</div>", unsafe_allow_html=True)
with col2:
    if st.button("Navigator", key="nav_home"):
        set_tab("Landing")
with col3:
    if st.button("About", key="nav_about"):
        set_tab("About")
with col4:
    if st.button("Resources", key="nav_resources"):
        set_tab("Resources")

st.markdown("<hr style='margin-top: 0; margin-bottom: 2rem; border-color: #334155;'>", unsafe_allow_html=True)

# --- About Tab Content (Updated Developer Profile) ---
if st.session_state.nav_tab == "About":
    st.markdown("## About the Developer")
    st.markdown("""
        <div class='dev-profile-card'>
            <h2 style='color: #FFFFFF !important; border-bottom: 1px solid #334155; padding-bottom: 12px; margin-top: 0;'>Shubham Thakur</h2>
            <p style='color: #E2E8F0 !important; font-size: 1.1rem; line-height: 1.6;'>
                17-year-old student currently studying at HIM Academy, Vikasnagar, India.
            </p>
            <p style='color: #CBD5E1 !important; font-size: 1rem; line-height: 1.6;'>
                Deeply interested in Artificial Intelligence, emerging technologies, entrepreneurship, and solving real-world problems through software.
            </p>
            <p style='color: #CBD5E1 !important; font-size: 1rem; line-height: 1.6;'>
                OpportunityOS was designed and developed entirely using a mobile phone, demonstrating that innovation is driven by ideas and persistence rather than expensive hardware.
            </p>
            <p style='color: #CBD5E1 !important; font-size: 1rem; line-height: 1.6;'>
                This project aims to help students discover scholarships, competitions, government schemes, free learning resources, and personalized career roadmaps using AI.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- Resources Tab Content ---
if st.session_state.nav_tab == "Resources":
    st.markdown("## Platform Resources & Frameworks")
    st.markdown("Access foundational guides and open educational repositories integrated into our system architecture.")
    st.markdown("### Verified Open Portals")
    st.markdown("- **Global Scholarship Gateways:** Comprehensive repositories for international grants.")
    st.markdown("- **Open Courseware Index:** Direct indexing of MIT, Harvard, and Stanford public syllabi.")
    st.markdown("- **Competitive Programming & Hackathons:** Global calendars for algorithmic and engineering challenges.")
    st.stop()

# --- Gemini API Configuration with Caching ---
@st.cache_resource
def py_genai_configure(key):
    genai.configure(api_key=key)

def get_gemini_client():
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return None, "Gemini API key not configured. Please add GEMINI_API_KEY in Streamlit Secrets."
        
        api_key = st.secrets["GEMINI_API_KEY"]
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            return None, "Gemini API key not configured. Please add GEMINI_API_KEY in Streamlit Secrets."
            
        py_genai_configure(api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model, None
    except Exception:
        return None, "The configured Gemini API key is invalid or has been revoked. Generate a new key in Google AI Studio and update Streamlit Secrets."

# --- AI Roadmap Generation Logic with Optimization ---
@st.cache_data(show_spinner=False)
def cached_generate_roadmap_text(prompt_text):
    model, err = get_gemini_client()
    if err:
        return None, err
    try:
        response = model.generate_content(prompt_text)
        return response.text, None
    except PermissionDenied:
        return None, "The configured Gemini API key is invalid or has been revoked. Generate a new key in Google AI Studio and update Streamlit Secrets."
    except ResourceExhausted:
        return None, "Rate Limit Exceeded: You have hit the API quota limit. Please try again later."
    except GoogleAPICallError as g_err:
        return None, f"Google API Error: {g_err.message}"
    except Exception:
        return None, "The configured Gemini API key is invalid or has been revoked. Generate a new key in Google AI Studio and update Streamlit Secrets."

def generate_roadmap(profile_data):
    prompt = f"""
    You are an expert career mentor. Based on the student profile below, generate a comprehensive career and opportunity roadmap using sections 1 through 9:
    
    Profile: Age {profile_data['age']}, Country {profile_data['country']}, State/Province {profile_data['state']}, City {profile_data['city']}, Education Level {profile_data['education_level']}, Current Class/Year {profile_data['current_class']}, Career Goal {profile_data['career_goal']}, Preferred Career {profile_data['preferred_career']}, Interests {profile_data['interests']}, Favourite Subjects {profile_data['favourite_subjects']}, Skills {profile_data['skills']}, Family Income {profile_data['family_income']}, Languages {profile_data['languages']}, Preferred Study Country {profile_data['preferred_country']}, Dream University {profile_data['dream_university']}, Extracurricular Activities {profile_data['extracurricular_activities']}, Certificates {profile_data['certificates']}, Projects Built {profile_data['projects_built']}, Volunteer Experience {profile_data['volunteer_experience']}, Research Experience {profile_data['research_experience']}, Olympiads {profile_data['olympiads']}, Hackathons {profile_data['hackathons']}, Leadership Experience {profile_data['leadership_experience']}, Portfolio Website {profile_data['portfolio_website']}, GitHub Profile {profile_data['github_profile']}, LinkedIn Profile {profile_data['linkedin_profile']}.
    
    Provide clear Markdown sections for:
    ## Section 1: Opportunity Summary
    ## Section 2: Scholarships
    ## Section 3: Government Schemes
    ## Section 4: Competitions
    ## Section 5: Free Learning Resources
    ## Section 6: Six-Month Roadmap
    ## Section 7: Portfolio Suggestions
    ## Section 8: Skill Gap Analysis
    ## Section 9: AI Mentor Advice
    """
    return cached_generate_roadmap_text(prompt)

# --- Landing Page & Form View ---
if st.session_state.nav_tab == "Landing":
    if 'roadmap_result' not in st.session_state:
        st.markdown("### AI Opportunity Navigator")
        st.markdown("#### Discover scholarships, competitions, government schemes, free learning resources, and a personalized career roadmap—all in one place.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("profile_form"):
            st.markdown("#### Complete Your Profile")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                age = st.text_input("Age", placeholder="Enter your age...")
                country = st.text_input("Country", placeholder="Enter your country...")
                state = st.text_input("State / Province", placeholder="Enter your state or province...")
            with c2:
                city = st.text_input("City", placeholder="Enter your city...")
                education_level = st.text_input("Education Level", placeholder="e.g., High School, Undergraduate...")
                current_class = st.text_input("Current Class or Year", placeholder="e.g., Grade 12, Year 2...")
            with c3:
                career_goal = st.text_input("Career Goal", placeholder="e.g., AI Research Scientist...")
                preferred_career = st.text_input("Preferred Career", placeholder="e.g., Machine Learning Engineer...")
                languages = st.text_input("Languages (Optional)", placeholder="e.g., English, Spanish...")

            c4, c5, c6 = st.columns(3)
            with c4:
                interests = st.text_area("Interests", placeholder="e.g., Machine Learning, Robotics...")
                favourite_subjects = st.text_input("Favourite Subjects", placeholder="e.g., Mathematics, Physics...")
                skills = st.text_area("Skills (Optional)", placeholder="e.g., Python, Git, Linear Algebra...")
            with c5:
                family_income = st.text_input("Family Income (Optional)", placeholder="Enter family income...")
                preferred_country = st.text_input("Preferred Study Country (Optional)", placeholder="e.g., United States...")
                dream_university = st.text_input("Dream University (Optional)", placeholder="e.g., Stanford University...")
            with c6:
                extracurricular_activities = st.text_area("Extracurricular Activities", placeholder="e.g., Debate Club, Model UN...")
                certificates = st.text_area("Certificates", placeholder="e.g., AWS Certified, Coursera ML...")
                projects_built = st.text_area("Projects Built", placeholder="e.g., Smart Attendance System...")

            c7, c8, c9 = st.columns(3)
            with c7:
                volunteer_experience = st.text_area("Volunteer Experience", placeholder="e.g., Teaching math to kids...")
                research_experience = st.text_area("Research Experience", placeholder="e.g., Published paper on NLP...")
            with c8:
                olympiads = st.text_area("Olympiads", placeholder="e.g., IMO, Physics Olympiad...")
                hackathons = st.text_area("Hackathons", placeholder="e.g., NASA Space Apps Winner...")
            with c9:
                leadership_experience = st.text_area("Leadership Experience", placeholder="e.g., Student Council President...")
                portfolio_website = st.text_input("Portfolio Website (Optional)", placeholder="https://yourportfolio.com")
                github_profile = st.text_input("GitHub Profile (Optional)", placeholder="https://github.com/username")
                linkedin_profile = st.text_input("LinkedIn Profile (Optional)", placeholder="https://linkedin.com/in/username")

            submitted = st.form_submit_button("Generate My Roadmap")
            
            if submitted:
                profile_data = {
                    "age": age, 
                    "country": country, 
                    "state": state, 
                    "city": city,
                    "education_level": education_level, 
                    "current_class": current_class,
                    "career_goal": career_goal, 
                    "preferred_career": preferred_career,
                    "interests": interests, 
                    "favourite_subjects": favourite_subjects,
                    "skills": skills,
                    "family_income": family_income, 
                    "languages": languages,
                    "preferred_country": preferred_country, 
                    "dream_university": dream_university,
                    "extracurricular_activities": extracurricular_activities,
                    "certificates": certificates,
                    "projects_built": projects_built,
                    "volunteer_experience": volunteer_experience,
                    "research_experience": research_experience,
                    "olympiads": olympiads,
                    "hackathons": hackathons,
                    "leadership_experience": leadership_experience,
                    "portfolio_website": portfolio_website,
                    "github_profile": github_profile,
                    "linkedin_profile": linkedin_profile
                }
                
                with st.spinner("Analyzing profile and generating your personalized roadmap..."):
                    result, err_msg = generate_roadmap(profile_data)
                    if result:
                        st.session_state.roadmap_result = result
                        st.rerun()
                    else:
                        st.error(err_msg)

    else:
        st.markdown("## Your Personalized Opportunity Roadmap")
        
        st.markdown("<div class='roadmap-container'>", unsafe_allow_html=True)
        st.markdown(st.session_state.roadmap_result)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_dl1, col_dl2, col_back = st.columns([1, 1, 2])
        with col_dl1:
            st.download_button(
                label="Download Markdown",
                data=st.session_state.roadmap_result,
                file_name="OpportunityOS_Roadmap.md",
                mime="text/markdown"
            )
        with col_dl2:
            if st.button("Reset Profile"):
                del st.session_state.roadmap_result
                st.rerun()
    

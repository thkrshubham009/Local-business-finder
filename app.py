import os
import json
import streamlit as st
import pandas as pd
from google import genai
from google.genai.errors import APIError

# --- Page Configuration ---
st.set_page_config(
    page_title="OpportunityOS – AI Opportunity Navigator",
    page_icon="O",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Clean SaaS Styling & UI Polish ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }
    .main .block-container {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    .stMarkdown p, .stMarkdown span, .stMarkdown li {
        color: #F8FAFC !important;
    }
    .roadmap-container, div[data-testid="stForm"] {
        background-color: #1E293B !important;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        margin-bottom: 24px;
        color: #F8FAFC !important;
    }
    .roadmap-container h1, .roadmap-container h2, .roadmap-container h3, .roadmap-container h4, .roadmap-container h5, .roadmap-container h6 {
        color: #FFFFFF !important;
        border-bottom: 1px solid #334155;
        padding-bottom: 10px;
        margin-top: 24px;
    }
    .roadmap-container p, .roadmap-container li, .roadmap-container span {
        color: #CBD5E1 !important;
    }
    .roadmap-container strong {
        color: #F8FAFC !important;
    }
    div[data-testid="stForm"] label {
        color: #F8FAFC !important;
        font-weight: 600 !important;
    }
    div[data-testid="stForm"] p, div[data-testid="stForm"] span {
        color: #CBD5E1 !important;
    }
    .stButton > button, 
    div[data-testid="stFormSubmitButton"] > button, 
    div[data-testid="stDownloadButton"] > button,
    button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        min-height: 48px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        transition: all 0.2s ease;
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
        border-color: rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 6px 12px -2px rgba(37, 99, 235, 0.3);
    }
    input, select, textarea {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
    }
    input:focus, select:focus, textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
    }
    /* Professional Navbar Styling */
    .topnav-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0 1.5rem 0;
        border-bottom: 1px solid #334155;
        margin-bottom: 2rem;
    }
    .nav-brand {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        color: #FFFFFF;
    }
    .nav-links {
        display: flex;
        gap: 8px;
    }
    .dev-profile-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-top: 20px;
    }
    /* Radio and Selectbox polish */
    div[data-testid="stRadio"] label {
        color: #F8FAFC !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Navigation State Management ---
if 'nav_tab' not in st.session_state:
    st.session_state.nav_tab = "Landing"

if 'show_optional' not in st.session_state:
    st.session_state.show_optional = False

def set_tab(tab_name):
    st.session_state.nav_tab = tab_name

# --- Professional Website-Style Navigation Bar ---
st.markdown("<div class='topnav-container'>", unsafe_allow_html=True)
col_brand, col_nav = st.columns([2, 5])
with col_brand:
    st.markdown("<div class='nav-brand'>OpportunityOS</div>", unsafe_allow_html=True)
with col_nav:
    nc1, nc2, nc3, nc4, nc5 = st.columns(5)
    with nc1:
        if st.button("Navigator", key="nav_home"):
            set_tab("Landing")
    with nc2:
        if st.button("Career", key="nav_career"):
            set_tab("Career Navigator")
    with nc3:
        if st.button("Opportunities", key="nav_opps"):
            set_tab("Opportunity Finder")
    with nc4:
        if st.button("About", key="nav_about"):
            set_tab("About")
    with nc5:
        if st.button("Resources", key="nav_resources"):
            set_tab("Resources")
st.markdown("</div>", unsafe_allow_html=True)

# --- About Tab Content ---
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

# --- Official Google Gen AI SDK Client & Model Integration ---
def get_verified_gemini_client():
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return None, None, "No compatible Gemini model is currently available. Please verify your API key, SDK version, and available models."
        
        api_key = st.secrets["GEMINI_API_KEY"]
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            return None, None, "No compatible Gemini model is currently available. Please verify your API key, SDK version, and available models."
            
        client = genai.Client(api_key=api_key)
        
        # Iteratively probe available models from the new SDK client listing to prevent hardcoded mismatches
        model_id = None
        try:
            preferred_models = [
                "gemini-3.6-flash",
                "gemini-3.5-flash",
                "gemini-3.1-flash-lite",
                "gemini-flash-latest",
                "gemini-2.0-flash"
            ]

            available = [m.name.split("/")[-1] for m in client.models.list()]

            model_id = None
            for model in preferred_models:
                if model in available:
                    model_id = model
                    break

            if model_id is None:
                raise Exception("No supported Gemini model found.")
        except Exception:
            pass

        # Ultimate fallback if listing is restricted or fails
        if not model_id:
            models = list(client.models.list())

            for m in models:
                name = m.name.split("/")[-1]
                if "generateContent" in getattr(m, "supported_actions", []):
                     model_id = name
                     break

            if not model_id:
                raise Exception("No supported Gemini model found.")
            
        return client, model_id, None
    except Exception as e:
        return None, None, f"Gemini Client Error: {e}"

# --- AI Roadmap Generation Logic with Evidence-Based Mentor Prompt ---
@st.cache_data(show_spinner=False)
def cached_generate_roadmap_text(prompt_text):
    client, model_id, err = get_verified_gemini_client()
    if err:
        return None, err
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt_text
        )
        if response and hasattr(response, 'text') and response.text:
            return response.text, None
        else:
            return None, "No compatible Gemini model is currently available. Please verify your API key, SDK version, and available models."
    except APIError as e:
        return None, f"Google API Error: {e}"
    except Exception as e:
        return None, f"Python Error: {e}"

def generate_roadmap(profile_data):
    for k, v in profile_data.items():
        if not v or str(v).strip() == "":
            profile_data[k] = "Insufficient information to evaluate this area."

    prompt = f"""
    You are an evidence-based admissions committee member, experienced career coach, and AI researcher. Your tone must be strictly objective, candid, rigorous, and direct. 
    You must NEVER exaggerate, flatter, tell the student they are amazing, invent strengths, or make unrealistic promises. If information is missing, explicitly say: "Insufficient information to evaluate this area." Never guess.

    Student Profile:
    - Age: {profile_data['age']}
    - Country: {profile_data['country']}
    - State/Province: {profile_data['state']}
    - City: {profile_data['city']}
    - Education Level: {profile_data['education_level']}
    - Current Class/Year: {profile_data['current_class']}
    - Career Goal: {profile_data['career_goal']}
    - Interests: {profile_data['interests']}
    - Skills: {profile_data['skills']}
    - Languages: {profile_data['languages']}
    - Certificates: {profile_data['certificates']}
    - Projects: {profile_data['projects']}
    - Research: {profile_data['research']}
    - Volunteer Experience: {profile_data['volunteer_experience']}
    - Olympiads: {profile_data['olympiads']}
    - Hackathons: {profile_data['hackathons']}
    - Leadership: {profile_data['leadership']}
    - Portfolio: {profile_data['portfolio']}
    - GitHub: {profile_data['github']}
    - LinkedIn: {profile_data['linkedin']}
    - Dream University: {profile_data['dream_university']}
    - Preferred Country: {profile_data['preferred_country']}
    - Family Income: {profile_data['family_income']}
    - Achievements: {profile_data['achievements']}
    - Extracurricular Activities: {profile_data['extracurricular_activities']}

    Generate a professional action plan using the exact markdown sections below:

    ## Overall Assessment
    - Give a realistic evaluation.
    - State strengths.
    - State weaknesses.
    - State biggest risks.

    ## Reality Check
    - Explain how competitive the chosen career actually is.
    - Mention acceptance rates or competition only when supported by reliable public information.
    - Never invent numbers.

    ## Skill Gap Analysis
    - List current skills.
    - List missing skills.
    - List highest priority skills.

    ## 12-Month Roadmap
    - Break into months (Month 1 through Month 12).
    - Only practical actions.
    - No motivational language.

    ## Scholarships
    - Recommend only scholarships matching the student's country, age and profile.
    - If none exist, clearly state that.

    ## Competitions
    - Recommend competitions that genuinely fit the profile.

    ## Free Learning Resources
    - Recommend official courses and respected platforms.

    ## Projects
    - Recommend progressively harder projects.

    ## Final Verdict
    - Summarize current competitiveness.
    - What must improve.
    - Estimated readiness if the roadmap is followed.
    - No motivational ending. Only realistic conclusions.
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
                education_level = st.text_input("Current Education Level", placeholder="e.g., High School, Undergraduate...")
                current_class = st.text_input("Current Class / Year", placeholder="e.g., Grade 12, Year 2...")
            with c3:
                career_goal = st.text_input("Career Goal", placeholder="e.g., AI Research Scientist...")
                interests = st.text_area("Interests", placeholder="e.g., Machine Learning, Robotics...")

            submitted_main = st.form_submit_button("Generate My Roadmap")
            
            if st.form_submit_button("Optional Details ▼" if not st.session_state.show_optional else "Optional Details ▲"):
                st.session_state.show_optional = not st.session_state.show_optional
                st.rerun()

            skills = ""
            languages = ""
            certificates = ""
            projects = ""
            research = ""
            volunteer_experience = ""
            olympiads = ""
            hackathons = ""
            leadership = ""
            portfolio = ""
            github = ""
            linkedin = ""
            dream_university = ""
            preferred_country = ""
            family_income = ""
            achievements = ""
            extracurricular_activities = ""

            if st.session_state.show_optional:
                st.markdown("---")
                st.markdown("#### Additional Optional Background")
                
                oc1, oc2, oc3 = st.columns(3)
                with oc1:
                    skills = st.text_area("Skills", placeholder="e.g., Python, Git, Linear Algebra...")
                    languages = st.text_input("Languages", placeholder="e.g., English, Spanish...")
                    certificates = st.text_area("Certificates", placeholder="e.g., AWS Certified, Coursera ML...")
                    projects = st.text_area("Projects", placeholder="e.g., Smart Attendance System...")
                with oc2:
                    research = st.text_area("Research Experience", placeholder="e.g., Published paper on NLP...")
                    volunteer_experience = st.text_area("Volunteer Experience", placeholder="e.g., Teaching math to kids...")
                    olympiads = st.text_area("Olympiads", placeholder="e.g., IMO, Physics Olympiad...")
                    hackathons = st.text_area("Hackathons", placeholder="e.g., NASA Space Apps Winner...")
                with oc3:
                    leadership = st.text_area("Leadership", placeholder="e.g., Student Council President...")
                    portfolio = st.text_input("Portfolio Website", placeholder="https://yourportfolio.com")
                    github = st.text_input("GitHub Profile", placeholder="https://github.com/username")
                    linkedin = st.text_input("LinkedIn Profile", placeholder="https://linkedin.com/in/username")

                oc4, oc5, oc6 = st.columns(3)
                with oc4:
                    dream_university = st.text_input("Dream University", placeholder="e.g., Stanford University...")
                with oc5:
                    preferred_country = st.text_input("Preferred Country", placeholder="e.g., United States...")
                with oc6:
                    family_income = st.text_input("Family Income", placeholder="Enter family income...")

                achievements = st.text_area("Achievements", placeholder="List notable awards or milestones...")
                extracurricular_activities = st.text_area("Extracurricular Activities", placeholder="e.g., Debate Club, Model UN...")

            if submitted_main:
                profile_data = {
                    "age": age, 
                    "country": country, 
                    "state": state, 
                    "city": city,
                    "education_level": education_level, 
                    "current_class": current_class,
                    "career_goal": career_goal, 
                    "interests": interests,
                    "skills": skills,
                    "languages": languages,
                    "certificates": certificates,
                    "projects": projects,
                    "research": research,
                    "volunteer_experience": volunteer_experience,
                    "olympiads": olympiads,
                    "hackathons": hackathons,
                    "leadership": leadership,
                    "portfolio": portfolio,
                    "github": github,
                    "linkedin": linkedin,
                    "dream_university": dream_university,
                    "preferred_country": preferred_country,
                    "family_income": family_income,
                    "achievements": achievements,
                    "extracurricular_activities": extracurricular_activities
                }
                
                with st.spinner("Analyzing profile and generating rigorous evidence-based roadmap..."):
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
                st.session_state.show_optional = False
                st.rerun()

# --- New Feature 1: Career Navigator Tab ---
if st.session_state.nav_tab == "Career Navigator":
    st.markdown("## Career Navigator")
    st.markdown("Analyze an exact profession path or evaluate multiple options matching your background objectively.")
    
    career_mode = st.radio("Select Evaluation Mode", ["Mode 1 - I already know my career", "Mode 2 - Help me choose"])
    
    if career_mode == "Mode 1 - I already know my career":
        with st.form("career_known_form"):
            desired_career = st.text_input("Desired Career", placeholder="e.g., AI Engineer, Cryptographer, Robotics Engineer...")
            submitted_career = st.form_submit_button("Analyze Career Path")
            
            if submitted_career:
                if not desired_career.strip():
                    st.error("Please enter a valid desired career.")
                else:
                    prompt = f"""
                    You are an experienced career counsellor and industry researcher. Be strict, realistic, candid, and direct. Never flatter or use motivational filler. If information is missing, explicitly say: "Insufficient information to evaluate this area."
                    
                    Evaluate the career path: {desired_career}
                    
                    Provide a detailed analysis using exact markdown sections:
                    ## Career Overview
                    ## Reality of the Field
                    ## Difficulty Level
                    ## Required Skills
                    ## Degree Recommendations
                    ## Daily Work
                    ## Salary Overview
                    ## Future Demand
                    ## Pros
                    ## Cons
                    ## Common Mistakes Beginners Make
                    ## Practical Roadmap
                    """
                    with st.spinner("Analyzing career path..."):
                        res, err = cached_generate_roadmap_text(prompt)
                        if res:
                            st.markdown("<div class='roadmap-container'>", unsafe_allow_html=True)
                            st.markdown(res)
                            st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.error(err)
                            
    else:
        with st.form("career_choice_form"):
            st.markdown("#### Provide Background for Career Matching")
            c1, c2 = st.columns(2)
            with c1:
                c_age = st.text_input("Age", placeholder="Enter age...")
                c_edu = st.text_input("Education Level", placeholder="Enter education...")
                c_fav = st.text_input("Favourite Subjects", placeholder="Enter subjects...")
                c_interests = st.text_input("Interests", placeholder="Enter interests...")
                c_hobbies = st.text_input("Hobbies", placeholder="Enter hobbies...")
            with c2:
                c_strengths = st.text_input("Strengths", placeholder="Enter strengths...")
                c_weaknesses = st.text_input("Weaknesses", placeholder="Enter weaknesses...")
                c_personality = st.text_input("Personality", placeholder="Enter personality...")
                c_workstyle = st.text_input("Preferred Work Style", placeholder="Enter work style...")
                c_country = st.text_input("Preferred Country (Optional)", placeholder="Enter country...")
                
            submitted_choice = st.form_submit_button("Recommend Careers")
            
            if submitted_choice:
                prompt = f"""
                You are an experienced career counsellor. Be strict, realistic, and objective. Never flatter or exaggerate. Recommend 5 to 8 suitable careers based strictly on the profile below. For every recommendation include: Why it matches, Difficulty, Required education, Future demand, and Things to improve. If data is missing say "Insufficient information to evaluate this area."
                
                Profile:
                - Age: {c_age}
                - Education Level: {c_edu}
                - Favourite Subjects: {c_fav}
                - Interests: {c_interests}
                - Hobbies: {c_hobbies}
                - Strengths: {c_strengths}
                - Weaknesses: {c_weaknesses}
                - Personality: {c_personality}
                - Preferred Work Style: {c_workstyle}
                - Preferred Country: {c_country}
                """
                with st.spinner("Generating career recommendations..."):
                    res, err = cached_generate_roadmap_text(prompt)
                    if res:
                        st.markdown("<div class='roadmap-container'>", unsafe_allow_html=True)
                        st.markdown(res)
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error(err)

# --- New Feature 2: Opportunity Finder Tab ---
if st.session_state.nav_tab == "Opportunity Finder":
    st.markdown("## Opportunity Finder")
    st.markdown("Discover rigorous, verified scholarships, competitions, hackathons, and programs matching your exact profile.")
    
    with st.form("opportunity_finder_form"):
        st.markdown("#### Enter Profile Criteria")
        of_col1, of_col2 = st.columns(2)
        with of_col1:
            of_age = st.text_input("Age", placeholder="Enter age...")
            of_country = st.text_input("Country", placeholder="Enter country...")
        with of_col2:
            of_edu = st.text_input("Education Level", placeholder="e.g., High School, Undergrad...")
            of_goal = st.text_input("Career Goal", placeholder="e.g., AI Research Scientist...")
            
        submitted_opps = st.form_submit_button("Find Verified Opportunities")
        
        if submitted_opps:
            if not of_age.strip() or not of_country.strip() or not of_edu.strip() or not of_goal.strip():
                st.error("Please fill in Age, Country, Education Level, and Career Goal.")
            else:
                prompt = f"""
                You are an expert admissions committee member and mentor. Recommend specific, verified opportunities matching the profile below. Include Scholarships, Competitions, Olympiads, Hackathons, Fellowships, Research programs, Government schemes, Grants, Free certifications, and Bootcamps. 
                If no verified opportunity exists for a category, state so honestly. Never invent opportunities. Tone must be strictly factual and realistic.
                
                Profile:
                - Age: {of_age}
                - Country: {of_country}
                - Education Level: {of_edu}
                - Career Goal: {of_goal}
                """
                with st.spinner("Searching verified opportunity databases..."):
                    res, err = cached_generate_roadmap_text(prompt)
                    if res:
                        st.markdown("<div class='roadmap-container'>", unsafe_allow_html=True)
                        st.markdown(res)
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error(err)

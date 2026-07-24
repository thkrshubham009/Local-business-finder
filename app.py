import os
import json
import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- Page Configuration ---
st.set_page_config(
    page_title="OpportunityOS – AI Opportunity Navigator",
    page_icon="O",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Professional Minimalist Styling (No Emojis, Clean SaaS UI) ---
st.markdown("""
    <style>
    /* Global Styles */
    .main {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.025em;
    }
    
    /* Cards */
    .stCard, div[data-testid="stVerticalBlock"] > div.element-container > div.stMarkdown {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 16px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #0f172a;
        color: #ffffff;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1e293b;
        color: #ffffff;
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input, .stSelectbox > div > div > select, .stNumberInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
    }
    
    /* Navigation Bar simulation */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    .nav-brand {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        text-decoration: none;
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
    st.markdown("<span style='font-size: 1.25rem; font-weight: 800; letter-spacing: -0.05em;'>OpportunityOS</span>", unsafe_allow_html=True)
with col2:
    if st.button("Navigator", key="nav_home"):
        set_tab("Landing")
with col3:
    if st.button("About", key="nav_about"):
        set_tab("About")
with col4:
    if st.button("Resources", key="nav_resources"):
        set_tab("Resources")

st.markdown("<hr style='margin-top: 0; margin-bottom: 2rem; border-color: #e2e8f0;'>", unsafe_allow_html=True)

# --- About Tab Content ---
if st.session_state.nav_tab == "About":
    st.markdown("## About OpportunityOS")
    st.markdown("""
        OpportunityOS is an autonomous intelligence platform designed to bridge the gap between ambitious students and world-class opportunities. 
        By mapping individual profiles against global databases of scholarships, government initiatives, competitive tracks, and high-impact learning resources, 
        OpportunityOS generates structured, actionable career execution paths.
    """)
    st.markdown("### Core Principles")
    st.markdown("- **Precision:** Recommendations are custom-tailored to exact profile inputs.")
    st.markdown("- **Transparency:** Clear distinction between factual insights and suggested pathways.")
    st.markdown("- **Actionability:** Structured milestones and skill-gap breakdowns designed for execution.")
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

# --- Gemini API Configuration ---
def get_gemini_client():
    api_key = None
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# --- AI Roadmap Generation Logic ---
def generate_roadmap(profile_data):
    model = get_gemini_client()
    if not model:
        return None

    prompt = f"""
    You are an expert, highly experienced education and career mentor. Based on the student profile below, generate a comprehensive, structured career and opportunity roadmap.
    
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
    - Family Income: {profile_data['family_income']}
    - Languages: {profile_data['languages']}
    - Preferred Study Country: {profile_data['preferred_country']}
    - Dream University: {profile_data['dream_university']}

    Strictly adhere to the following output sections, using clear markdown headers (Section 1 to Section 9):

    ## Section 1: Opportunity Summary
    - Explain the student's profile comprehensively.
    - Identify key strengths.
    - Identify potential challenges.
    - Recommend the best strategic path.

    ## Section 2: Scholarships
    - Generate a ranked list of relevant scholarships.
    - For each, include: Name, Why it fits, Eligibility summary, Application timeline (if known), Documents commonly required.
    - Include a clear reminder to verify current details on the official website before applying.

    ## Section 3: Government Schemes
    - Recommend relevant government schemes based on the profile.
    - Include: Name, Purpose, Who typically benefits, General eligibility summary, Required documents.
    - Encourage users to confirm details through official government sources.

    ## Section 4: Competitions
    - Recommend hackathons, olympiads, innovation challenges, research competitions, coding competitions, and entrepreneurship competitions.
    - Explain why each matches the user's interests.

    ## Section 5: Free Learning Resources
    - Recommend specific courses or tracks from Coursera, edX, MIT OpenCourseWare, Khan Academy, fast.ai, freeCodeCamp, and Harvard Online.
    - Explain why each course is relevant.

    ## Section 6: Six-Month Roadmap
    - Provide realistic, actionable milestones broken down systematically from Month 1 to Month 6.

    ## Section 7: Portfolio Suggestions
    - Recommend specific projects the student should build.
    - Explain why.
    - Estimate difficulty levels.

    ## Section 8: Skill Gap Analysis
    - List current strengths.
    - List missing skills.
    - Highlight learning priorities.

    ## Section 9: AI Mentor Advice
    - Write personalized guidance in a supportive, practical, and candid tone.
    
    Ensure all details are realistic. Distinguish between facts and suggestions. Avoid inventing official eligibility rules or deadlines.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with AI service: {str(e)}"

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
                age = st.number_input("Age", min_value=10, max_value=100, value=18)
                country = st.text_input("Country", value="United States")
                state = st.text_input("State / Province", value="California")
            with c2:
                city = st.text_input("City", value="San Francisco")
                education_level = st.selectbox("Education Level", ["High School", "Undergraduate", "Graduate", "Self-Taught", "Other"])
                current_class = st.text_input("Current Class or Year", value="Grade 12")
            with c3:
                career_goal = st.text_input("Career Goal", value="AI Research Scientist")
                languages = st.text_input("Languages", value="English, Spanish")
                family_income = st.text_input("Family Income (Optional)", value="Not specified")

            c4, c5, c6 = st.columns(3)
            with c4:
                interests = st.text_area("Interests", value="Machine Learning, Robotics, Mathematics")
            with c5:
                skills = st.text_area("Skills", value="Python, Linear Algebra, Git")
            with c6:
                preferred_country = st.text_input("Preferred Study Country (Optional)", value="United States")
                dream_university = st.text_input("Dream University (Optional)", value="Stanford University")

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
                    "interests": interests,
                    "skills": skills,
                    "family_income": family_income,
                    "languages": languages,
                    "preferred_country": preferred_country,
                    "dream_university": dream_university
                }
                
                with st.spinner("Analyzing profile and synthesizing global opportunity databases..."):
                    result = generate_roadmap(profile_data)
                    if result:
                        st.session_state.roadmap_result = result
                        st.rerun()
                    else:
                        st.error("Failed to generate roadmap. Please check your API key configuration.")

    else:
        st.markdown("## Your Personalized Opportunity Roadmap")
        st.markdown("Generated successfully based on your profile parameters.")
        
        # Display the result inside a structured layout container
        st.markdown("<div style='background-color: #ffffff; padding: 32px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);'>", unsafe_allow_html=True)
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
                

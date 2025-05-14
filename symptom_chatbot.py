import streamlit as st

# --- OpenAI Client Setup ---
from dotenv import load_dotenv
import os
from openai import OpenAI
import re

# --- Custom CSS Styling ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f8ff;
    }
    .custom-container { 
        max-width: 700px;
        margin: 0 auto;
        padding: 2rem 2rem;
    }
    .block-space {
        margin-bottom: 1.5rem;
    }
    body, .stApp {
    font-size: 16px;}
    </style>
    """,
    unsafe_allow_html=True
)

# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- SESSION STATE INIT ---
st.session_state.setdefault('page', 'start')
st.session_state.setdefault('age', None)
st.session_state.setdefault('gender', None)

# --- AI Response Function ---
def generate_ai_response(symptoms, age, gender, categories):
    prompt = f"""
You are an AI healthcare assistant. A {age}-year-old {gender} reports the following symptoms: {symptoms}.
Symptom categories: {', '.join(categories) if categories else 'N/A'}.

Your response must be informed by medical knowledge sourced from publicly available and trusted datasets like:
- healthdata.gov
- data.cdc.gov
- data.cms.gov
- open.fda.gov

Based on this, provide:
1. A possible explanation in layman's terms (non-diagnostic).
2. A recommendation (e.g., rest, monitor, consult doctor, urgent care).
3. In one line, suggest the type of doctor they should consult using this format:
   "You should consult with a [specialist type]."

Avoid giving specific diagnoses.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ An error occurred: {e}"

# --- PAGE 1: USER INFO ---
if st.session_state.page == 'start':
    st.markdown("#### Step 1 of 2: Basic Information")
    st.progress(0.5)

    st.markdown('<div class="custom-container">', unsafe_allow_html=True)

    st.title("Your Reliable Symptom Checker")
    st.markdown("Please enter your details to begin:")

    age = st.number_input("Age", min_value=0, max_value=120, step=1, key="age_input")
    st.markdown('<div class="block-space"></div>', unsafe_allow_html=True)

    gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True, key="gender_input")
    st.markdown('<div class="block-space"></div>', unsafe_allow_html=True)

    st.markdown("✅ This chatbot uses data-driven insights from publicly available health sources.")
    with st.expander("ℹ️ View Trusted Medical Sources"):
        st.markdown("""
- [healthdata.gov](https://healthdata.gov/)
- [data.gov](https://data.gov/)
- [data.cdc.gov](https://data.cdc.gov/)
- [open.fda.gov](https://open.fda.gov/)
- [data.cms.gov](https://data.cms.gov/)
- [wonder.cdc.gov](https://wonder.cdc.gov/)
- [bigcitieshealthdata.org](https://bigcitieshealthdata.org/)
        """)

    st.markdown('<div class="block-space"></div>', unsafe_allow_html=True)

    if st.button("Continue"):
        if age == 0 or gender == "":
            st.warning("⚠️ Please enter your age and select a gender to proceed.")
        else:
            st.session_state.age = age
            st.session_state.gender = gender
            st.session_state.page = 'assessment'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2: SYMPTOM CHECK ---
elif st.session_state.page == 'assessment':
    st.markdown("#### Step 2 of 2: Symptom Assessment")
    st.progress(1.0)
    # ... rest of Page 2 code ...


    st.title("🔍 Symptom Assessment")
    st.markdown(f"Hi **user** ({st.session_state.gender}, aged {st.session_state.age})")
    
    # ✅ Symptom Input
    symptoms = st.text_area("Describe your symptoms:")

    categories = st.multiselect(
        "Optional: Select symptom categories",
        ["Fever", "Cough", "Fatigue", "Pain", "Breathing issues", "Digestive issues"]
    )

    if st.button("Check Symptoms"):
        if not symptoms.strip():
            st.warning("Please describe your symptoms before proceeding.")
        else:
            red_flags = ["chest pain", "shortness of breath", "unconscious", "bleeding"]
            if any(flag in symptoms.lower() for flag in red_flags):
                st.error("⚠️ Your symptoms may be serious. Please seek urgent medical care.")

            with st.spinner("Analyzing your symptoms..."):
                ai_response = generate_ai_response(symptoms, st.session_state.age, st.session_state.gender, categories)
                st.success(ai_response)

                # ✅ Try to extract doctor type using regex
                match = re.search(r"You should consult with (?:a|an)?\s*(.+?)[\.\n]", ai_response, re.IGNORECASE)
                doctor_type = match.group(1).strip() if match else "primary care physician"
                st.session_state.doctor_type = doctor_type

                # ✅ Suggest finding the doctor type
                st.markdown(f"🩺 *You should consult with a {doctor_type}*")
                st.markdown("📍 *Find a specialist near you by clicking the checkbox below.*")

                # ✅ Data source info block
                st.markdown("✅ This assessment is based on information from trusted public health data sources.")
                with st.expander("ℹ️ View Trusted Medical Sources"):
                    st.markdown("""
- [healthdata.gov](https://healthdata.gov/)
- [data.gov](https://data.gov/)
- [data.cdc.gov](https://data.cdc.gov/)
- [open.fda.gov](https://open.fda.gov/)
- [data.cms.gov](https://data.cms.gov/)
- [wonder.cdc.gov](https://wonder.cdc.gov/)
- [bigcitieshealthdata.org](https://bigcitieshealthdata.org/)
                    """)

    # ← Back Button
    if st.button("← Back"):
        st.session_state.page = 'start'
        st.rerun()

    # ✅ Doctor Map Lookup (dynamic fallback to generic if no recommendation yet)
    st.checkbox("**Find doctors near me**", key="find_doctors")

    if st.session_state.find_doctors:
        zip_code = st.text_input("Enter ZIP code:", key="zip_code")
        if zip_code:
            # Fallback to generic if AI hasn't set a type yet
            doctor_type = st.session_state.get("doctor_type", "doctor")
            map_link = f"https://www.google.com/maps/search/{doctor_type}+near+{zip_code}"
            st.markdown(f"[🗺️ Click to view {doctor_type}s near you]({map_link})", unsafe_allow_html=True)

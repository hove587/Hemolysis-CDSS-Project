import streamlit as st
import pandas as pd
import joblib

# Load the trained model
# We use @st.cache_resource so the model only loads once, making the app faster
@st.cache_resource
def load_model():
    return joblib.load('hemolysis_rf_model.pkl')

model = load_model()

# --- App Layout ---
st.set_page_config(page_title="Hemolysis Risk CDSS", page_icon="🩸")
st.title("Preanalytical Hemolysis Risk CDSS")
st.markdown("""
This Clinical Decision Support System (CDSS) predicts the likelihood of specimen hemolysis **post-collection, pre-analysis**. 
Enter the specimen details below to receive an actionable risk assessment.
""")

# Create input form
with st.form("input_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        # Using the exact uppercase names from the training data
        age = st.number_input("Patient Age (PATIENT_AGE)", min_value=0, max_value=120, value=50)
        sex = st.selectbox("Patient Sex (PATIENT_SEX)", ["F", "M", "U"]) # F=Female, M=Male, U=Unknown
        race = st.text_input("Patient Race (PATIENT_RACE)", "White")
        nursing_unit = st.text_input("Nursing Unit (NURSING_UNIT)", "ICU")
        encounter_type = st.text_input("Encounter Type (ENCOUNTER_TYPE)", "Inpatient")
        
    with col2:
        medical_service = st.text_input("Medical Service (MEDICAL_SERVICE)", "Medicine")
        # ORDERABLE is the specific lab test ordered
        orderable = st.text_input("Orderable Test (ORDERABLE)", "CBC") 
        collector_group = st.selectbox("Collector Volume", ["high_volume", "low_volume"])
        draw_site = st.text_input("Draw Site (DRAW_SITE)", "Antecubital")
        collection_day = st.selectbox("Collection Day (COLLECTION_DAY)", 
                                      ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        collection_time = st.text_input("Collection Time (COLLECTION_TIME)", "08:30")

    submit = st.form_submit_button("Predict Hemolysis Risk")

if submit:
    # Create a dataframe from inputs using the exact column names the model expects
    input_data = pd.DataFrame({
        'PATIENT_AGE': [age],
        'PATIENT_SEX': [sex],
        'PATIENT_RACE': [race],
        'NURSING_UNIT': [nursing_unit],
        'ENCOUNTER_TYPE': [encounter_type],
        'MEDICAL_SERVICE': [medical_service],
        'ORDERABLE': [orderable],
        'collector_group': [collector_group],
        'DRAW_SITE': [draw_site],
        'COLLECTION_DAY': [collection_day],
        'COLLECTION_TIME': [collection_time]
    })
    
    # Predict
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    
    st.divider()
    
    # Display results based on prediction
    if probability > 0.10:
        st.error(f"HIGH RISK OF HEMOLYSIS DETECTED (Risk Score: {probability:.2%})")
        # This is the exact alert aligned with the timing feedback
        st.warning("""
        Action Required: Consider immediate recollection or review of collection technique prior to analyzer loading to prevent result delay.
        """)
    else:
        st.success(f"✅ **LOW RISK OF HEMOLYSIS** (Risk Score: {probability:.2%})")
        st.info("Proceed with standard analysis protocol.")
import streamlit as st
import requests

# Function to handle API prediction
def get_prediction(data):
    try:
        response = requests.post('https://patient-readmission.streamlit.app/predict', json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

# Streamlit app layout
st.title('Patient Readmission Prediction')

# Input fields
encounter_id = st.number_input('Encounter ID', min_value=0, format='%d')
gender = st.selectbox('Gender', ['Male', 'Female'])
age = st.number_input('Age', min_value=0, format='%d')
admission_type_id = st.number_input('Admission Type ID', min_value=0, format='%d')
discharge_disposition_id = st.number_input('Discharge Disposition ID', min_value=0, format='%d')
num_procedures = st.number_input('Number of Procedures', min_value=0, format='%d')
num_medications = st.number_input('Number of Medications', min_value=0, format='%d')
number_outpatient = st.number_input('Number of Outpatient Visits', min_value=0, format='%d')
number_emergency = st.number_input('Number of Emergency Visits', min_value=0, format='%d')
number_inpatient = st.number_input('Number of Inpatient Visits', min_value=0, format='%d')
diag_2 = st.text_input('Secondary Diagnosis')
nateglinide = st.selectbox('Nateglinide', ['Yes', 'No'])
pioglitazone = st.selectbox('Pioglitazone', ['Yes', 'No'])
rosiglitazone = st.selectbox('Rosiglitazone', ['Yes', 'No'])
acarbose = st.selectbox('Acarbose', ['Yes', 'No'])
miglitol = st.selectbox('Miglitol', ['Yes', 'No'])
troglitazone = st.selectbox('Troglitazone', ['Yes', 'No'])
tolazamide = st.selectbox('Tolazamide', ['Yes', 'No'])
examide = st.selectbox('Examide', ['Yes', 'No'])
citoglipton = st.selectbox('Citoglipton', ['Yes', 'No'])
glyburide_metformin = st.selectbox('Glyburide-Metformin', ['Yes', 'No'])
metformin_rosiglitazone = st.selectbox('Metformin-Rosiglitazone', ['Yes', 'No'])

# Button to trigger prediction
if st.button('Predict'):
    input_data = {
        'encounter_id': encounter_id,
        'gender': gender,
        'age': age,
        'admission_type_id': admission_type_id,
        'discharge_disposition_id': discharge_disposition_id,
        'num_procedures': num_procedures,
        'num_medications': num_medications,
        'number_outpatient': number_outpatient,
        'number_emergency': number_emergency,
        'number_inpatient': number_inpatient,
        'diag_2': diag_2,
        'nateglinide': nateglinide,
        'pioglitazone': pioglitazone,
        'rosiglitazone': rosiglitazone,
        'acarbose': acarbose,
        'miglitol': miglitol,
        'troglitazone': troglitazone,
        'tolazamide': tolazamide,
        'examide': examide,
        'citoglipton': citoglipton,
        'glyburide-metformin': glyburide_metformin,
        'metformin-rosiglitazone': metformin_rosiglitazone
    }

    # Get prediction
    prediction_response = get_prediction(input_data)
    
    if prediction_response and 'prediction' in prediction_response:
        st.success(f"The prediction (Readmission) from model is: {prediction_response['prediction']}")
    else:
        st.error("Error occurred during prediction.")

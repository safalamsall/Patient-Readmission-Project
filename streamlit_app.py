import streamlit as st
import requests

# Function to handle API prediction
def get_prediction(data):
    url = 'http://127.0.0.1:5000/predict'
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP error occurred: {e.response.text}")  # Displaying the server's response text
    except requests.exceptions.ConnectionError:
        st.error("Connection error occurred. The server may be down.")
    except requests.exceptions.Timeout:
        st.error("Timeout error occurred.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
    return None

# Streamlit app layout
st.title('Patient Readmission Prediction')

# Input fields
input_data = {
    'encounter_id': st.number_input('Encounter ID', min_value=0, format='%d', value=1),
    'gender': st.selectbox('Gender', ['Male', 'Female']),
    'age': st.number_input('Age', min_value=0, format='%d', value=1),
    'admission_type_id': st.number_input('Admission Type ID', min_value=0, format='%d', value=1),
    'discharge_disposition_id': st.number_input('Discharge Disposition ID', min_value=0, format='%d', value=1),
    'num_procedures': st.number_input('Number of Procedures', min_value=0, format='%d', value=0),
    'num_medications': st.number_input('Number of Medications', min_value=0, format='%d', value=1),
    'number_outpatient': st.number_input('Number of Outpatient Visits', min_value=0, format='%d', value=0),
    'number_emergency': st.number_input('Number of Emergency Visits', min_value=0, format='%d', value=0),
    'number_inpatient': st.number_input('Number of Inpatient Visits', min_value=0, format='%d', value=0),
    'diag_2': st.text_input('Secondary Diagnosis', value='None'),
    'nateglinide': st.selectbox('Nateglinide', ['Yes', 'No']),
    'pioglitazone': st.selectbox('Pioglitazone', ['Yes', 'No']),
    'rosiglitazone': st.selectbox('Rosiglitazone', ['Yes', 'No']),
    'acarbose': st.selectbox('Acarbose', ['Yes', 'No']),
    'miglitol': st.selectbox('Miglitol', ['Yes', 'No']),
    'troglitazone': st.selectbox('Troglitazone', ['Yes', 'No']),
    'tolazamide': st.selectbox('Tolazamide', ['Yes', 'No']),
    'examide': st.selectbox('Examide', ['Yes', 'No']),
    'citoglipton': st.selectbox('Citoglipton', ['Yes', 'No']),
    'glyburide-metformin': st.selectbox('Glyburide-Metformin', ['Yes', 'No']),
    'metformin-rosiglitazone': st.selectbox('Metformin-Rosiglitazone', ['Yes', 'No'])
}

# Button to trigger prediction
if st.button('Predict'):
    # Ensure all numeric fields have values (not empty)
    if not all(input_data.values()):
        st.error("Please ensure all fields are filled correctly.")
    else:
        prediction_response = get_prediction(input_data)
        if prediction_response and 'prediction' in prediction_response:
            st.success(f"The prediction (Readmission) from model is: {prediction_response['prediction']}")
        else:
            st.error("Error occurred during prediction.")

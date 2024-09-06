from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load your trained model
model = joblib.load('Model/model.pkl')

@app.route('/')
def home():
    logger.info("Home Page accessed")
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Attempt to receive JSON data
    data = request.get_json(force=True)
    logger.info(f"Received Data: {data}")

    # Ensure that the JSON data has the correct format for input features
    try:
        # Convert the JSON data into a DataFrame
        input_data = pd.DataFrame([data])
        logger.info(f"Input Data: {input_data}")

        # Mapping dictionary for conversion of categorical to numerical data
        mapping_dict = {
            'gender': {'Male': 0, 'Female': 1},
            'nateglinide': {'No': 0, 'Yes': 1},
            'pioglitazone': {'No': 0, 'Yes': 1},
            'rosiglitazone': {'No': 0, 'Yes': 1},
            'acarbose': {'No': 0, 'Yes': 1},
            'miglitol': {'No': 0, 'Yes': 1},
            'tolazamide': {'No': 0, 'Yes': 1},
            'examide': {'No': 0, 'Yes': 1},
            'citoglipton': {'No': 0, 'Yes': 1},
            'troglitazone': {'No': 0, 'Yes': 1},
            'glyburide-metformin': {'No': 0, 'Yes': 1},
            'metformin-rosiglitazone': {'No': 0, 'Yes': 1}
        }

        # Apply mappings to convert data
        for key, value in mapping_dict.items():
            input_data[key] = input_data[key].map(value)

    except Exception as e:
        logger.error(f"Data formatting error: {str(e)}")
        return jsonify({'error': str(e), 'message': 'Data formatting error'}), 400

    # Predict using the loaded model
    try:
        predictions = model.predict(input_data)
        predictions = predictions.tolist()  # Convert prediction to list if it is in numpy array format
        result = "No, The patient will Not be Readmitted" if predictions[0] == 0 else "Yes, The patient will be Readmitted"
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': str(e), 'message': 'Error during prediction'}), 500

    # Return the prediction in JSON format
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)

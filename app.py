from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load your trained model
model = joblib.load('Model/model.pkl')


@app.route('/')
def home():
    print("Home Page")
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Receive JSON data
    data = request.get_json(force=True)
    print("Received Data: ", data)

    # Ensure that the JSON data has the correct format for input features
    try:
        # Convert the JSON data into a DataFrame
        input_data = pd.DataFrame([data])
        print("Input Data: ", input_data)

        # Convert categorical data to numerical values
        input_data['gender'] = input_data['gender'].map({'Male': 0, 'Female': 1})
        input_data['nateglinide'] = input_data['nateglinide'].map({'No': 0, 'Yes': 1})


        input_data['pioglitazone'] = input_data['pioglitazone'].map({'No': 0, 'Yes': 1})
        input_data['rosiglitazone'] = input_data['rosiglitazone'].map({'No': 0, 'Yes': 1})
        input_data['acarbose'] = input_data['acarbose'].map({'No': 0, 'Yes': 1})
        input_data['miglitol'] = input_data['miglitol'].map({'No': 0, 'Yes': 1})
        input_data['tolazamide'] = input_data['tolazamide'].map({'No': 0, 'Yes': 1})
        input_data['examide'] = input_data['examide'].map({'No': 0, 'Yes': 1})
        input_data['citoglipton'] = input_data['citoglipton'].map({'No': 0, 'Yes': 1})
        input_data['troglitazone'] = input_data['troglitazone'].map({'No': 0, 'Yes': 1})

        input_data['glyburide-metformin'] = input_data['glyburide-metformin'].map({'No': 0, 'Yes': 1})
        input_data['metformin-rosiglitazone'] = input_data['metformin-rosiglitazone'].map({'No': 0, 'Yes': 1})


        print("Converted Input Data: ", input_data)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Data formatting error'}), 400

    # Predict using the loaded model
    try:
        predictions = model.predict(input_data)
        # Convert prediction to list if it is in numpy array format
        predictions = predictions.tolist()
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Error during prediction'}), 500
    if predictions[0] == 0:
        predictions = "No, The patient will Not be Readmitted"  # Negative class
    else:
        predictions = "Yes, The patient will be Readmitted"
    # Return the prediction in JSON format
    return jsonify({'prediction': predictions})


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Replace with your Custom Vision Service API keys and endpoint
prediction_key = "e2cfd8c522e1456e949f5df226bc02ff"
endpoint = "https://farazindu-prediction.cognitiveservices.azure.com/"

# Endpoint for the prediction API
project_id = "4969811f-5144-4cc4-9d40-b978dd8ee44b"
iteration_id = "Iteration1"
prediction_url = f"{endpoint}/customvision/v3.0/Prediction/{project_id}/classify/iterations/{iteration_id}/image"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Read the file and send it to the Custom Vision Service for prediction
        image_data = file.read()
        headers = {'Prediction-Key': prediction_key, 'Content-Type': 'application/octet-stream'}
        response = requests.post(prediction_url, headers=headers, data=image_data)

        if response.status_code == 200:
            predictions = json.loads(response.content)
            # Process the predictions as needed
            return render_template('result.html', predictions=predictions['predictions'])
        else:
            return f"Prediction failed. Please try again. Error: {response.content}"

if __name__ == '__main__':
    app.run(debug=True)

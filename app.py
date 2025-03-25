from flask import Flask, request, jsonify
import os
import joblib
import numpy as np
from utils import enhance_phishing_check  # Import the new function

app = Flask(__name__)

# Load pre-trained model and other necessary files
model = joblib.load('model/phishing_detector_model.pkl')
label_encoder = joblib.load('model/label_encoder.pkl')
feature_columns = joblib.load('model/feature_columns.pkl')

# Get VirusTotal API key from environment variable
VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY')

@app.route('/detect_phishing', methods=['POST'])
def detect_phishing():
    try:
        # Get URL from request
        url = request.json.get('url', '')
        
        # Perform initial ML prediction
        # Assuming you have a function to extract features from URL
        url_features = extract_url_features(url)
        
        # Predict probability of phishing
        ml_prediction = model.predict_proba([url_features])[0][1]
        
        # Enhance prediction with VirusTotal check
        enhanced_result = enhance_phishing_check(
            url, 
            ml_prediction, 
            virustotal_api_key=VIRUSTOTAL_API_KEY
        )
        
        return jsonify({
            'url': url,
            'phishing_probability': enhanced_result['ml_prediction'],
            'virustotal_details': enhanced_result.get('virustotal_check')
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Error in phishing detection'
        }), 500

def extract_url_features(url):
    # Implement your existing feature extraction logic here
    # This should return the same feature vector used during model training
    # Example (replace with your actual feature extraction):
    features = []
    # Add your feature extraction steps
    return features

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
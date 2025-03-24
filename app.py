from flask import Flask, render_template, request, jsonify
from utils import load_model_resources, predict_url
import os

app = Flask(__name__)

# Load model resources once when the app starts
model, label_encoder, feature_columns, ranked_domains_df = load_model_resources()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url', '')
    
    # Add http:// prefix if not present
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    
    try:
        result = predict_url(url, model, label_encoder, ranked_domains_df, feature_columns)
        return jsonify({
            'safe': result['safe'],
            'probability': f"{result['probability']*100:.1f}",
            'prediction': result['prediction']
        })
    except Exception as e:
        print(f"Error analyzing URL: {str(e)}")
        return jsonify({
            'error': 'Error analyzing URL',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
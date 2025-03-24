import re
from urllib.parse import urlparse
import tldextract
import pandas as pd
import pickle
import os

# Function to extract features from a URL
def extract_features(url):
    """Extract features from a URL"""
    features = {}

    # Parse the URL
    parsed_url = urlparse(url)
    extracted = tldextract.extract(url)
    domain = extracted.domain + '.' + extracted.suffix if extracted.suffix else extracted.domain

    # Length-based features
    features['url_length'] = len(url)
    features['domain_length'] = len(domain)

    # URL structure features
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['num_underscores'] = url.count('_')
    features['num_slashes'] = url.count('/')
    features['num_question_marks'] = url.count('?')
    features['num_equal_signs'] = url.count('=')
    features['num_at_signs'] = url.count('@')
    features['num_ampersands'] = url.count('&')
    features['num_exclamation'] = url.count('!')
    features['num_tildes'] = url.count('~')
    features['num_percent'] = url.count('%')
    features['num_plus'] = url.count('+')
    features['num_asterisks'] = url.count('*')
    features['num_hash'] = url.count('#')
    features['num_dollar_signs'] = url.count('$')

    # Domain-specific features
    features['has_ip_address'] = 1 if re.match(r'\d+\.\d+\.\d+\.\d+', domain) else 0
    features['has_https'] = 1 if parsed_url.scheme == 'https' else 0
    features['has_www'] = 1 if extracted.subdomain == 'www' else 0
    features['subdomain_length'] = len(extracted.subdomain)
    features['num_subdomains'] = len(extracted.subdomain.split('.')) if extracted.subdomain else 0

    # Path-specific features
    features['path_length'] = len(parsed_url.path)
    features['has_suspicious_words'] = 1 if re.search(r'(login|signin|verify|secure|account|password|credential|confirm)', url.lower()) else 0

    # Query parameters
    features['num_params'] = len(parsed_url.query.split('&')) if parsed_url.query else 0

    return features

# Function to predict if a URL is a phishing site
def predict_url(url, model, label_encoder, ranked_domains_df, feature_columns):
    # Extract features from the URL
    features = extract_features(url)

    # Convert to DataFrame for consistency
    features_df = pd.DataFrame([features])

    # Determine which column in ranked_domains_df contains domains
    domain_column = None
    possible_names = ['domains', 'domain', 'website', 'url', 'site']

    for col in ranked_domains_df.columns:
        if col.lower() in possible_names:
            domain_column = col
            break

    if domain_column is None:
        # If no matching column found, use the second column (index 1)
        if len(ranked_domains_df.columns) >= 2:
            domain_column = ranked_domains_df.columns[1]
        else:
            domain_column = ranked_domains_df.columns[0]

    # Add domain reputation feature
    extracted = tldextract.extract(url)
    domain = extracted.domain + '.' + extracted.suffix
    features_df['in_top_domains'] = 1 if domain in ranked_domains_df[domain_column].values else 0

    # Make sure the DataFrame has all the features used during training
    for col in feature_columns:
        if col not in features_df.columns:
            features_df[col] = 0

    # Keep only the features used during training and in the same order
    features_df = features_df[feature_columns]

    # Make prediction
    prediction = model.predict(features_df)[0]
    probability = model.predict_proba(features_df)[0][prediction]

    # Convert prediction to label
    label = label_encoder.inverse_transform([prediction])[0]

    return {
        'url': url,
        'prediction': label,
        'probability': probability,
        'safe': label == 'good'
    }

# Load model and required files
def load_model_resources():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(current_dir, 'model')
    
    # Load the model
    with open(os.path.join(model_dir, 'phishing_detector_model.pkl'), 'rb') as f:
        model = pickle.load(f)

    # Load the label encoder
    with open(os.path.join(model_dir, 'label_encoder.pkl'), 'rb') as f:
        le = pickle.load(f)

    # Load feature columns
    with open(os.path.join(model_dir, 'feature_columns.pkl'), 'rb') as f:
        feature_columns = pickle.load(f)

    # Load ranked domains
    ranked_domains_df = pd.read_csv(os.path.join(model_dir, 'ranked_domains.csv'))

    return model, le, feature_columns, ranked_domains_df
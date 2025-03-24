# Phishing URL Detector

A machine learning-powered web application that detects phishing URLs using XGBoost. The application analyzes various URL features to identify potential phishing sites, helping users stay safe online.

![Phishing URL Detector Screenshot](https://media-hosting.imagekit.io//6b8774e70322455f/Screenshot%202025-03-24%20at%202.02.29%E2%80%AFPM.png?Expires=1837413173&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=ij0izAIeeppSto3s6GC2OzJIUVJcLGg~lYVUfF7QbsodJPSY3Qe2CZTJLGqU2Lx~lCEGvIufnnadnEgTz9OuFXnrXAQbpW3Ai-xzZxmwrOkneUAj4BRrP8vFPmDQebLycm5YrueVhQyEK8cGS9PcxXhJCBTS2cdWHyR-IIrPGR~ylxb-qNU2hmOeNCX00SgwXFg93OczAf2FcAJqTujb823LtNufgP4o-Dbd7w28Ig1t6u-oK~F0O-8ha~zON4NjhpcZriwgo3G04hn87S2ObBTS0yfS78-y01nQnuRsavcm3QCNZYs1Xm2f-mCxHrycos3lIM-1wvRJSJL60Wqgxw__)

## 📋 Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Deployment](#deployment)
  - [Deploy Locally](#deploy-locally)
- [UI Versions](#ui-versions)
- [Model Performance](#model-performance)
- [Limitations](#model-performance)

## ✨ Features
- Analyzes URLs in real-time to detect phishing attempts
- Extracts 20+ features from URLs for accurate detection
- Provides confidence scores for predictions
- Simple and intuitive user interface
- High accuracy detection model
- Detailed analysis breakdown for each URL

## 🌐 Demo
Check out the live demo: [Phishing URL Detector](https://phishing-detector-pnz9.onrender.com/)

## 🛠️ Tech Stack
- **Machine Learning**: XGBoost, Scikit-learn, Pandas, NumPy
- **Backend**: Python
- **Web Interface**: 
  - Streamlit (Primary)
  - HTML/CSS/JS (Alternative)
- **Deployment**: Render, GitHub

## 📁 Project Structure
```
phishing-url-detector/
├── datasets/
├── models/
│   ├── phishing_detector_model.pkl
│   ├── label_encoder.pkl
│   └── feature_columns.pkl
├── src/
│   ├── train_model.py
│   └── feature_extraction.py
├── streamlit_app.py
├── web_ui/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── requirements.txt
├── README.md
```

## 🔍 How It Works
The Phishing URL Detector extracts multiple features from a given URL:

1. **URL Structure Features**: Length of URL, domain, and path
2. **Character Frequency**: Count of special characters like dots, hyphens, etc.
3. **Domain Features**: Presence of IP address, HTTPS, WWW, subdomains
4. **Lexical Features**: Suspicious keywords, URL shortening services
5. **Domain Reputation**: Comparison with known legitimate domains

These features are fed into an XGBoost classifier trained on a dataset of labeled URLs to predict whether a URL is legitimate or phishing.

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/phishing-url-detector.git
   cd phishing-url-detector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```


### Deploy Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/phishing-url-detector.git
   cd phishing-url-detector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

4. Access the application at `http://localhost:8501`

## 🎨 UI Versions

### Streamlit UI
The primary interface uses Streamlit for a clean, functional design focused on the URL analysis functionality.

### Website UI
An alternative HTML/CSS/JS interface is available:
- Bold, chunky elements
- High contrast colors
- "Raw" design aesthetic
- Exaggerated drop shadows
- Intentionally "unrefined" appearance



## 📊 Model Performance
The XGBoost model achieves the following performance metrics:

- **Accuracy**: 93.7%
- **Precision**: 94.2%
- **Recall**: 92.1%
- **F1 Score**: 93.1%

## ⚠️ Limitations


- **Evasion Techniques**: Attackers constantly evolve phishing techniques, which may reduce model effectiveness.
- **Dataset Bias**: The model was trained on a specific dataset; new phishing tactics may require retraining.
- **False Positives**: Some legitimate but unusual URLs might be classified as phishing





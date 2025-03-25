import requests
import os
import time

def check_url_virustotal(url, api_key):
    """
    Check URL reputation using VirusTotal API
    
    Args:
        url (str): URL to check
        api_key (str): VirusTotal API key
    
    Returns:
        dict: VirusTotal analysis results
    """
    # VirusTotal API endpoint for URL scanning
    base_url = 'https://www.virustotal.com/vtapi/v2/url/scan'
    
    headers = {
        'x-apikey': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        # First, analyze the URL
        analyze_response = requests.post(
            f'{base_url}/urls', 
            headers=headers, 
            data={'url': url}
        )
        analyze_response.raise_for_status()
        
        # Get the analysis ID
        analysis_id = analyze_response.json().get('data', {}).get('id')
        
        if not analysis_id:
            return {
                'is_malicious': False,
                'error': 'Unable to get analysis ID'
            }
        
        # Wait and get analysis results
        analysis_url = f'{base_url}/analyses/{analysis_id}'
        
        max_attempts = 10
        attempt = 0
        
        while attempt < max_attempts:
            results_response = requests.get(analysis_url, headers=headers)
            results_response.raise_for_status()
            
            status = results_response.json().get('data', {}).get('attributes', {}).get('status')
            
            if status == 'completed':
                # Analyze detection results
                stats = results_response.json().get('data', {}).get('attributes', {}).get('stats', {})
                
                # Consider URL potentially malicious if more than 3 engines flag it
                is_malicious = stats.get('malicious', 0) > 3
                
                return {
                    'is_malicious': is_malicious,
                    'detection_stats': stats
                }
            
            # Add small delay between checks
            time.sleep(3)
            attempt += 1
        
        return {
            'is_malicious': False,
            'error': 'Analysis timed out'
        }
    
    except requests.RequestException as e:
        return {
            'is_malicious': False,
            'error': str(e)
        }

def enhance_phishing_check(url, ml_prediction, virustotal_api_key=None):
    """
    Enhance phishing detection by combining ML model prediction 
    with VirusTotal API check
    
    Args:
        url (str): URL to check
        ml_prediction (float): Probability from ML model
        virustotal_api_key (str, optional): VirusTotal API key
    
    Returns:
        dict: Enhanced prediction results
    """
    # Start with ML model prediction
    result = {
        'ml_prediction': ml_prediction,
        'virustotal_check': None
    }
    
    # Only perform VirusTotal check if API key is provided
    if virustotal_api_key:
        try:
            virustotal_result = check_url_virustotal(url, virustotal_api_key)
            
            # Combine predictions
            result['virustotal_check'] = virustotal_result
            
            # Adjust ML prediction based on VirusTotal results
            if virustotal_result.get('is_malicious'):
                # If VirusTotal flags the URL, increase phishing probability
                result['ml_prediction'] = min(ml_prediction * 1.5, 0.95)  # Cap at 0.95
            elif not virustotal_result.get('is_malicious'):
                # If VirusTotal clears the URL, slightly reduce phishing probability
                result['ml_prediction'] = max(ml_prediction * 0.8, 0.05)  # Floor at 0.05
        
        except Exception as e:
            result['virustotal_error'] = str(e)
    
    return result
document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('url-input');
    const checkButton = document.getElementById('check-button');
    const checkAnotherButton = document.getElementById('check-another');
    const loader = document.getElementById('loader');
    const result = document.getElementById('result');
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const resultDescription = document.getElementById('result-description');
    const resultConfidence = document.getElementById('result-confidence');

    const API_BASE_URL = 'https://phishing-detector-pnz9.onrender.com'; // Update with your Render deployment URL

    checkButton.addEventListener('click', checkUrl);
    urlInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') checkUrl();
    });

    checkAnotherButton.addEventListener('click', function() {
        urlInput.value = '';
        result.classList.add('hidden');
        urlInput.focus();
    });

    function checkUrl() {
        const url = urlInput.value.trim();
        if (!url) {
            alert('Please enter a URL to check');
            return;
        }

        loader.classList.remove('hidden');
        result.classList.add('hidden');

        fetch(`${API_BASE_URL}/detect_phishing`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        })
        .then(response => response.json())
        .then(data => {
            loader.classList.add('hidden');
            if (data.error) return showError(data.message || 'Error analyzing URL');

            resultIcon.innerHTML = data.phishing_probability < 50 ? '✅' : '⚠️';
            resultIcon.className = data.phishing_probability < 50 ? 'safe' : 'unsafe';
            resultTitle.textContent = data.phishing_probability < 50 ? 'URL is Safe' : 'Warning: Potential Phishing';
            resultTitle.className = data.phishing_probability < 50 ? 'safe' : 'unsafe';
            resultDescription.textContent = data.phishing_probability < 50 
                ? 'This URL appears to be legitimate.' 
                : 'This URL has characteristics of phishing websites.';
            resultConfidence.textContent = `Confidence: ${data.phishing_probability.toFixed(2)}%`;
            result.classList.remove('hidden');
        })
        .catch(() => {
            loader.classList.add('hidden');
            showError('Network error: Could not connect to server');
        });
    }

    function showError(message) {
        resultIcon.innerHTML = '❌';
        resultIcon.className = 'unsafe';
        resultTitle.textContent = 'Error';
        resultTitle.className = 'unsafe';
        resultDescription.textContent = message;
        resultConfidence.textContent = '';
        result.classList.remove('hidden');
    }
});

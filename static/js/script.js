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

    checkButton.addEventListener('click', function() {
        checkUrl();
    });

    urlInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            checkUrl();
        }
    });

    checkAnotherButton.addEventListener('click', function() {
        // Clear the input and hide results
        urlInput.value = '';
        result.classList.add('hidden');
        
        // Show the form again
        urlInput.focus();
    });

    function checkUrl() {
        const url = urlInput.value.trim();
        
        if (!url) {
            alert('Please enter a URL to check');
            return;
        }
        
        // Show loader
        loader.classList.remove('hidden');
        result.classList.add('hidden');
        
        // API call to check URL
        fetch('/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            // Hide loader
            loader.classList.add('hidden');
            
            // Check for error
            if (data.error) {
                showError(data.message || 'An error occurred while analyzing the URL');
                return;
            }
            
            // Show results
            if (data.safe) {
                resultIcon.innerHTML = '✅';
                resultIcon.className = 'safe';
                resultTitle.textContent = 'URL is Safe';
                resultTitle.className = 'safe';
                resultDescription.textContent = 'This URL appears to be legitimate.';
            } else {
                resultIcon.innerHTML = '⚠️';
                resultIcon.className = 'unsafe';
                resultTitle.textContent = 'Warning: Potential Phishing';
                resultTitle.className = 'unsafe';
                resultDescription.textContent = 'This URL has characteristics of phishing websites.';
            }
            
            resultConfidence.textContent = `Confidence: ${data.probability}%`;
            result.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
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
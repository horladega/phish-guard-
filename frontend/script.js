const API_URL = 'http://localhost:5000/api';

const messageInput = document.getElementById('messageInput');
const scanBtn = document.getElementById('scanBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const keywordsContainer = document.getElementById('keywordsContainer');
const keywordsList = document.getElementById('keywordsList');
const urlsContainer = document.getElementById('urlsContainer');
const urlsList = document.getElementById('urlsList');
const noLinksMessage = document.getElementById('noLinksMessage');
const errorMessage = document.getElementById('errorMessage');

scanBtn.addEventListener('click', scanMessage);
messageInput.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        scanMessage();
    }
});

async function scanMessage() {
    const message = messageInput.value.trim();

    if (!message) {
        showError('Please enter a message to scan');
        return;
    }

    // Show loading state
    scanBtn.disabled = true;
    loadingSpinner.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    errorMessage.classList.add('hidden');

    try {
        const response = await fetch(`${API_URL}/scan`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to scan message: ${error.message}. Make sure the backend is running on http://localhost:5000`);
    } finally {
        scanBtn.disabled = false;
        loadingSpinner.classList.add('hidden');
    }
}

function displayResults(data) {
    // Clear previous results
    keywordsList.innerHTML = '';
    urlsList.innerHTML = '';
    keywordsContainer.classList.add('hidden');
    urlsContainer.classList.add('hidden');
    noLinksMessage.classList.add('hidden');
    errorMessage.classList.add('hidden');

    // Display keywords
    if (data.scam_keywords && data.scam_keywords.length > 0) {
        keywordsContainer.classList.remove('hidden');
        data.scam_keywords.forEach((keyword) => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag';
            tag.textContent = keyword;
            keywordsList.appendChild(tag);
        });
    }

    // Display URLs
    if (data.urls && data.urls.length > 0) {
        urlsContainer.classList.remove('hidden');
        data.urls.forEach((urlData) => {
            const urlItem = createUrlItem(urlData);
            urlsList.appendChild(urlItem);
        });
    } else if (!data.message) {
        noLinksMessage.classList.remove('hidden');
    }

    // Display message if no URLs found
    if (data.message) {
        noLinksMessage.classList.remove('hidden');
    }

    resultsSection.classList.remove('hidden');
}

function createUrlItem(urlData) {
    const item = document.createElement('div');
    item.className = 'url-item';

    const riskClass = `risk-${urlData.risk.toLowerCase()}`;

    const header = document.createElement('div');
    header.className = 'url-header';

    const urlText = document.createElement('div');
    urlText.className = 'url-text';
    urlText.textContent = urlData.url;

    const badge = document.createElement('span');
    badge.className = `risk-badge ${riskClass}`;
    badge.textContent = `Risk: ${urlData.risk}`;

    header.appendChild(urlText);
    header.appendChild(badge);

    const reasons = document.createElement('ul');
    reasons.className = 'url-reasons';
    urlData.reasons.forEach((reason) => {
        const li = document.createElement('li');
        li.textContent = reason;
        reasons.appendChild(li);
    });

    item.appendChild(header);
    item.appendChild(reasons);

    return item;
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    resultsSection.classList.remove('hidden');
}

# PhishGuard - Web Version

A web-based phishing detection tool that analyzes emails and messages for suspicious indicators.

## Project Structure

```
phish-guard-web/
├── backend/
│   ├── app.py                 # Flask backend server
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── index.html             # HTML structure
│   ├── style.css              # Styling
│   └── script.js              # Client-side logic
└── README.md
```

## Features

✨ **Phishing Detection**
- 🔍 Scans for common phishing keywords
- 🔗 Analyzes URLs for suspicious characteristics
- 📅 Checks domain age via WHOIS lookup
- 🏷️ Detects IP-based URLs and unusually long URLs

🎨 **User-Friendly Interface**
- Modern, responsive design
- Real-time scanning results
- Color-coded risk levels (Low, Medium, High)
- Mobile-friendly layout

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the Flask server:
   ```bash
   python app.py
   ```
   The server will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Open `index.html` in your browser or use a local server:
   ```bash
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000`

## Usage

1. Paste an email or message into the input field
2. Click "Scan for Phishing" or press Ctrl+Enter
3. Review the scan results:
   - **Suspicious Keywords**: Words commonly used in phishing attempts
   - **URL Analysis**: Risk assessment for each link found
   - **Risk Levels**: High, Medium, or Low based on multiple factors

## Detection Criteria

### Keywords Detected
- verify, urgent, claim, winner, password, account suspended, free gift, congratulations, lottery, prize, click here

### URL Risk Factors
- **High Risk:**
  - Contains suspicious keywords
  - Uses IP address instead of domain name

- **Medium Risk:**
  - Domain created less than 30 days ago
  - URL is unusually long (> 75 characters)

## API Endpoints

### POST /api/scan
Scans a message for phishing indicators.

**Request:**
```json
{
  "message": "Your message text here"
}
```

**Response:**
```json
{
  "scam_keywords": ["verify", "urgent"],
  "urls": [
    {
      "url": "https://example.com",
      "risk": "Low",
      "reasons": ["Domain is 5 years old"]
    }
  ]
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "PhishGuard API is running"
}
```

## Technologies Used

**Backend:**
- Flask - Web framework
- Flask-CORS - Cross-Origin Resource Sharing
- whois - Domain information lookup
- tldextract - Domain parsing

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript
- Responsive Design

## Deployment

### Backend Deployment (Example: Heroku)
1. Create a `Procfile` in the backend directory:
   ```
   web: python app.py
   ```

2. Deploy to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Frontend Deployment (Example: GitHub Pages)
1. Push frontend files to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Update `API_URL` in `script.js` to point to your deployed backend

## Troubleshooting

**CORS Error:** Make sure the Flask backend is running and CORS is properly configured.

**API Connection Error:** Verify the backend is running on `http://localhost:5000`

**WHOIS Lookup Fails:** Some domains may not be queryable via WHOIS. The application will handle this gracefully.

## Security Notes

- This tool is for educational and personal use
- Always verify suspicious emails through official channels
- Don't click links in suspicious messages
- Enable 2FA on important accounts

## Future Enhancements

- [ ] Database for storing scan history
- [ ] Machine learning-based detection
- [ ] Browser extension
- [ ] API key authentication
- [ ] Advanced phishing patterns recognition
- [ ] Screenshot analysis

## License

MIT License - Feel free to use and modify

## Support

For issues or feature requests, please open an issue on GitHub.

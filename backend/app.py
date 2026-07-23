from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import whois
import tldextract
from datetime import datetime

app = Flask(__name__)
CORS(app)

SCAM_WORDS = ["verify", "urgent", "claim", "winner", "password", "account suspended",
              "free gift", "congratulations", "lottery", "prize", "click here"]

def check_url(url):
    result = {"risk": "Low", "reasons": []}

    if any(word in url.lower() for word in SCAM_WORDS):
        result["risk"] = "High"
        result["reasons"].append("Contains suspicious keywords")

    if re.match(r'http[s]?://\d+\.\d+\.\d+\.\d+', url):
        result["risk"] = "High"
        result["reasons"].append("Uses IP address instead of domain name")

    try:
        domain = tldextract.extract(url).registered_domain
        w = whois.whois(domain)
        creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        if creation_date:
            age_days = (datetime.now() - creation_date).days
            if age_days < 30:
                result["risk"] = "Medium"
                result["reasons"].append(f"Domain is only {age_days} days old")
    except:
        result["reasons"].append("Could not verify domain age")

    if len(url) > 75:
        result["risk"] = "Medium" if result["risk"] == "Low" else result["risk"]
        result["reasons"].append("URL is unusually long")

    return result

@app.route('/api/scan', methods=['POST'])
def scan_message():
    data = request.get_json()
    text = data.get('message', '')
    
    if not text:
        return jsonify({"error": "No message provided"}), 400
    
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    
    scam_keywords_found = [word for word in SCAM_WORDS if word in text.lower()]
    
    results = {
        "scam_keywords": scam_keywords_found,
        "urls": []
    }
    
    if not urls:
        results["message"] = "No links found in message."
        return jsonify(results), 200
    
    for url in urls:
        scan = check_url(url)
        results["urls"].append({
            "url": url,
            "risk": scan["risk"],
            "reasons": scan["reasons"]
        })
    
    return jsonify(results), 200

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "PhishGuard API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# PhishGuard 🛡️
A Python GUI tool to detect phishing links and scam messages in Emails & WhatsApp.

### The Problem
In Nigeria, phishing scams via WhatsApp "airtime giveaway" and fake bank alerts are everywhere. Most people can't tell a real link from a fake one.

### The Solution
PhishGuard scans any message and flags:
- **Suspicious URLs** - IP addresses, long URLs, fake domains
- **New Domains** - Flags domains registered <30 days ago
- **Scam Keywords** - "verify", "claim prize", "account suspended"

### Features
- ✅ Simple GUI - Paste and Scan
- ✅ URL Risk Scoring: Low, Medium, High
- ✅ Domain Age Checker using WHOIS
- ✅ Keyword Detection for Social Engineering

### How to Run
1. Install dependencies:
   ```bash
   pip install python-whois tldextract
2. https://github.com/horladega/phish-guard-
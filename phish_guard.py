import re
import whois
import tldextract
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime, timezone

SCAM_WORDS = ["verify", "urgent", "claim", "winner", "password", "account suspended",
              "free gift", "congratulations", "lottery", "prize", "click here"]

def is_valid_url(url):
    """Validate if URL has proper format"""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return bool(re.match(url_pattern, url))

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
            # Make datetime timezone-aware for proper comparison
            if creation_date.tzinfo is None:
                creation_date = creation_date.replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - creation_date).days
            if age_days < 30:
                result["risk"] = "Medium"
                result["reasons"].append(f"Domain is only {age_days} days old")
    except (whois.parser.PywhoisError, AttributeError, TypeError, ValueError) as e:
        result["reasons"].append("Could not verify domain age")
    except Exception as e:
        # Log unexpected exceptions for debugging
        result["reasons"].append("Error checking domain details")

    if len(url) > 75:
        result["risk"] = "Medium" if result["risk"] == "Low" else result["risk"]
        result["reasons"].append("URL is unusually long")

    return result

def scan_message():
    text = input_box.get("1.0", tk.END)
    output_box.delete("1.0", tk.END)

    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

    output_box.insert(tk.END, "=== PhishGuard Scan Result ===\n\n")

    scam_keywords_found = [word for word in SCAM_WORDS if word in text.lower()]
    if scam_keywords_found:
        output_box.insert(tk.END, f"⚠️ Suspicious Keywords: {', '.join(scam_keywords_found)}\n\n")

    if not urls:
        output_box.insert(tk.END, "No links found in message.\n")
        return

    for url in urls:
        # Validate URL before scanning
        if not is_valid_url(url):
            output_box.insert(tk.END, f"Link: {url}\n")
            output_box.insert(tk.END, "Status: Invalid URL format\n")
            output_box.insert(tk.END, "-"*40 + "\n")
            continue
        
        scan = check_url(url)
        output_box.insert(tk.END, f"Link: {url}\n")
        output_box.insert(tk.END, f"Risk Level: {scan['risk']}\n")
        for reason in scan['reasons']:
            output_box.insert(tk.END, f"- {reason}\n")
        output_box.insert(tk.END, "-"*40 + "\n")

# GUI Setup
root = tk.Tk()
root.title("PhishGuard - Phishing Detector")
root.geometry("600x500")
root.resizable(True, True)  # Allow window resizing

tk.Label(root, text="Paste Email or WhatsApp Message Below:", font=("Arial", 12, "bold")).pack(pady=10)

input_box = scrolledtext.ScrolledText(root, width=70, height=10)
input_box.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

tk.Button(root, text="Scan for Phishing", command=scan_message, bg="#d32f2f", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

tk.Label(root, text="Results:", font=("Arial", 12, "bold")).pack()

output_box = scrolledtext.ScrolledText(root, width=70, height=12, bg="#f5f5f5")
output_box.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

root.mainloop()

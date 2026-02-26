import requests
from groq import Groq
import smtplib
from email.mime.text import MIMEText
import os

# -----------------------
# CONFIG
# -----------------------

GROQ_API_KEY = os.getenv("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")
EMAIL = os.getenv("gadhasuresh2003@gmail.com")
EMAIL_PASSWORD = os.getenv("pwhfcahblipdrfnj")

client = Groq(api_key=GROQ_API_KEY)

# -----------------------
# AGENT 1: Trend Collector
# -----------------------

def get_trending():
    url = "https://trends.google.com/trends/api/dailytrends?hl=en-US&geo=US"
    response = requests.get(url)
    return response.text[:500]  # simple extraction

# -----------------------
# AGENT 2: Analysis Agent
# -----------------------

def analyze_trend(trend):

    prompt = f"""
You are an intelligence analyst.

Analyze this trend:
{trend}

Explain:
- Why trending
- Emotional tone
- Importance
- Risk level (Low/Medium/High)
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content

# -----------------------
# AGENT 3: Email Agent
# -----------------------

def send_email(report):

    msg = MIMEText(report)
    msg["Subject"] = "🚨 AI Trend Intelligence Alert"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(EMAIL,EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

# -----------------------
# MAIN AGENT LOOP
# -----------------------

trend = get_trending()
report = analyze_trend(trend)
send_email(report)

print("Alert sent successfully")

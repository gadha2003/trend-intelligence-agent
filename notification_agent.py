import smtplib
import sqlite3
from email.mime.text import MIMEText

EMAIL = "gadhasuresh2003@gmail.com"
APP_PASSWORD = "quks iruj cazy zugs"

def send_email():

    conn = sqlite3.connect("trends.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic FROM trends
        ORDER BY timestamp DESC
        LIMIT 10
    """)

    trends = cursor.fetchall()

    message = "Latest Trending Topics:\n\n"

    for trend in trends:
        message += f"- {trend[0]}\n"

    msg = MIMEText(message)

    msg["Subject"] = "AI Trend Agent Alert"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(EMAIL, APP_PASSWORD)

    server.send_message(msg)

    server.quit()

    print("Email notification sent")
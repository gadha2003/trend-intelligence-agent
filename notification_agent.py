import smtplib
import os
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = os.environ.get("EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")


def send_email():

    print("Preparing email...")

    try:
        conn = sqlite3.connect("trends.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT topic, reason, timestamp
            FROM trends
            ORDER BY timestamp DESC
            LIMIT 10
        """)

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No data to send.")
            return

        body = "AI Trend Intelligence Report\n\n"

        for row in rows:
            body += f"Topic: {row[0]}\n"
            body += f"Summary: {row[1]}\n"
            body += f"Time: {row[2]}\n"
            body += "-" * 50 + "\n\n"

        message = MIMEMultipart()
        message["From"] = EMAIL
        message["To"] = EMAIL
        message["Subject"] = "AI Trend Intelligence Update"

        message.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(message)
        server.quit()

        print("Email sent successfully.")

    except Exception as e:
        print("Email error:", e)

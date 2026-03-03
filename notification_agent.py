import smtplib
import os
import sqlite3

EMAIL = os.environ.get("EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")


def send_email():

    print("Preparing email...")

    try:

        # Connect to database
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

        # Build Email Body
        body = "🔥 Top Trending Topics in India\n\n"

        for row in rows:
            topic = row[0]
            summary = row[1]
            timestamp = row[2]

            body += f"📌 {topic}\n"
            body += f"📝 Summary: {summary}\n"
            body += f"🕒 Time: {timestamp}\n"
            body += "-" * 50 + "\n\n"

        message = f"""Subject: 🔥 AI Trend Intelligence Update

{body}
"""

        print("Connecting to Gmail...")

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(EMAIL, APP_PASSWORD)

        server.sendmail(
            EMAIL,
            EMAIL,
            message
        )

        server.quit()

        print("✅ Email sent successfully.")

    except Exception as e:
        print("❌ Email error:", e)

import smtplib
import os
import sqlite3

EMAIL = os.environ.get("EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

def send_email():

    print("Preparing email...")

    try:

        conn = sqlite3.connect("trends.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT topic, source, timestamp
            FROM trends
            ORDER BY timestamp DESC
            LIMIT 10
        """)

        rows = cursor.fetchall()

        conn.close()

        if not rows:
            print("No data to send")
            return

        body = "Top Trending Topics:\n\n"

        for row in rows:

            body += f"{row[0]} ({row[1]})\n"

        message = f"""Subject: Trending Topics Update

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

        print("Email sent successfully")

    except Exception as e:

        print("Email error:", e)

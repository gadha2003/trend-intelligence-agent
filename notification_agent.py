import smtplib
import os
from database import get_trends

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_email():

    trends = get_trends()

    if not trends:
        print("No trends to email")
        return

    body = "Top Trends:\n\n"

    for t in trends:
        body += f"{t[0]} ({t[1]})\n"

    message = f"Subject: Trend Update\n\n{body}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
    server.sendmail(EMAIL, EMAIL, message)
    server.quit()

    print("Email sent")

from agents import google_trends_agent
from notification_agent import send_email

def run():

    print("Running agent...")
    google_trends_agent()

    print("Sending email...")
    send_email()

    print("Done")

if __name__ == "__main__":
    run()

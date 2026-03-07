from agents import google_trends_agent
from notification_agent import send_email


def run_agents():
    google_trends_agent()
   # send_email()


if __name__ == "__main__":
    run_agents()


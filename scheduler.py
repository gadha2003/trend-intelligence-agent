from agents import google_trends_agent
from notification_agent import send_email

def run_agents():

    print("Running Trend Agent...")

    google_trends_agent()

    send_email()

    print("Run complete.")

if __name__ == "__main__":

    run_agents()

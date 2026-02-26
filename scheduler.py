import schedule
import time
from agents import google_trends_agent
from notification_agent import send_email

def run_agents():

    print("Running Trend Agent...")

    google_trends_agent()

    send_email()

    print("Cycle complete")

schedule.every(5).hours.do(run_agents)

run_agents()

while True:

    schedule.run_pending()

    time.sleep(60)
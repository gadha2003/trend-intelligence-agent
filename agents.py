from serpapi import GoogleSearch
from database import save_trend
import os

API_KEY = os.getenv("SERPAPI_KEY")

def google_trends_agent():

    print("Fetching Google Trends via SerpAPI...")

    try:

        params = {
            "engine": "google_trends_trending_now",
            "geo": "IN",
            "api_key": API_KEY
        }

        search = GoogleSearch(params)

        results = search.get_dict()

        trends = results.get("trending_searches", [])

        if not trends:
            print("No trends found.")
            return

        for trend in trends[:10]:

            topic = trend.get("query")

            if topic:

                save_trend(topic, "Google Trends")

                print("Saved:", topic)

        print("Agent complete.")

    except Exception as e:

        print("Error:", e)

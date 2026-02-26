from serpapi import GoogleSearch
from database import save_trend

API_KEY = "6d575e03dcb46aead3ef5bdf244f44222e74ec5d95f5f22d9a3a4bb0f14f2193"

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

            # FIX: correct field name
            topic = trend.get("query")

            if topic:
                save_trend(topic, "Google Trends")
                print("Saved:", topic)

        print("Agent completed.")

    except Exception as e:

        print("Error:", e)
from serpapi import GoogleSearch
from database import save_trend
from groq import Groq
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)


# ------------------------------------------
# Generate AI Reason (Safe Version)
# ------------------------------------------
def generate_reason(topic, headlines):

    if not client:
        print("Groq API key missing. Using fallback reason.")
        return "Trending due to strong media coverage and public interest in India."

    try:
        prompt = f"""
Explain in 2-3 short lines why this topic is trending in India.

Topic: {topic}

News Headlines:
{headlines}

Give only a concise explanation.
"""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Groq error:", e)
        return "Trending due to recent news developments and public discussions."


# ------------------------------------------
# Main Google Trends Agent
# ------------------------------------------
def google_trends_agent():

    print("========== AI Trend Agent Started ==========")

    if not SERPAPI_KEY:
        print("ERROR: SERPAPI_KEY is missing.")
        return

    try:

        params = {
            "engine": "google_trends_trending_now",
            "geo": "IN",
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        print("FULL SERPAPI RESPONSE:")
        print(results)

        # ---- Handle API Errors ----
        if "error" in results:
            print("SerpAPI ERROR:", results["error"])
            return

        # ---- Handle Different Possible Structures ----
        trends = []

        if "trending_searches" in results:
            trends = results["trending_searches"]

        elif "real_time_trends" in results:
            trends = results["real_time_trends"]

        elif "daily_searches" in results:
            trends = results["daily_searches"]

        else:
            print("No recognizable trends key found in response.")
            print("Available keys:", results.keys())
            return

        print("TRENDS FOUND:", trends)

        if not trends:
            print("No trends found.")
            return

        # ---- Process Trends ----
        for trend in trends[:10]:

            # Handle different response formats safely
            if isinstance(trend, dict):
                topic = trend.get("query") or trend.get("title")
            else:
                topic = str(trend)

            if not topic:
                continue

            print("Processing:", topic)

            # Fetch related news
            news_params = {
                "engine": "google_news",
                "q": topic,
                "api_key": SERPAPI_KEY
            }

            news_search = GoogleSearch(news_params)
            news_results = news_search.get_dict()

            articles = news_results.get("news_results", [])[:3]

            headlines = "\n".join(
                [article["title"] for article in articles if "title" in article]
            )

            if headlines.strip() == "":
                headlines = "No major news found."

            # Generate explanation
            reason = generate_reason(topic, headlines)

            # Save to DB
            save_trend(topic, "Google Trends", reason)

            print("Saved:", topic)

        print("========== Agent Completed Successfully ==========")

    except Exception as e:
        print("Agent crash:", e)

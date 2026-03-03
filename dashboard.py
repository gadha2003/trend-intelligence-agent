from serpapi import GoogleSearch
from database import save_trend
from groq import Groq
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)


def generate_summary(topic):

    if not client:
        print("Groq client not initialized")
        return f"{topic} is currently being widely discussed."

    try:
        prompt = f"""
Explain clearly and factually what the following topic is about.
Do NOT explain why it is trending.
Just explain what it is in 2-3 simple sentences.

Topic: {topic}
"""

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # ✅ CURRENT WORKING MODEL
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        result = response.choices[0].message.content.strip()

        print("Groq summary generated successfully")
        return result

    except Exception as e:
        print("Groq error:", e)
        return f"{topic} is currently being widely discussed."


def google_trends_agent():

    print("========== AI Trend Agent Started ==========")

    if not SERPAPI_KEY:
        print("ERROR: SERPAPI_KEY missing.")
        return

    try:
        params = {
            "engine": "google_trends_trending_now",
            "geo": "IN",
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        trends = results.get("trending_searches", [])

        if not trends:
            print("No trends found.")
            return

        for trend in trends[:10]:

            topic = trend.get("query")

            if not topic:
                continue

            print("Processing:", topic)

            summary = generate_summary(topic)

            save_trend(topic, "Google Trends", summary)

            print("Saved:", topic)

        print("========== Agent Completed Successfully ==========")

    except Exception as e:
        print("Agent crash:", e)

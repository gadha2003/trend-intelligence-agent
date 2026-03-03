from serpapi import GoogleSearch
from database import save_trend
from groq import Groq
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)


# --------------------------------------------------
# Generate Topic Summary (NOT why trending)
# --------------------------------------------------
def generate_summary(topic):

    if not client:
        return f"{topic} is a currently popular search topic in India."

    try:
        prompt = f"""
You are an AI knowledge assistant.

Give a short and clear summary explaining what this topic is about.
Do NOT explain why it is trending.
Just explain what it is.

Topic: {topic}

Answer in 2-3 simple sentences.
"""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Groq error:", e)
        return f"{topic} is a widely discussed topic currently."


# --------------------------------------------------
# Google Trends Agent
# --------------------------------------------------
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

        if "error" in results:
            print("SerpAPI Error:", results["error"])
            return

        trends = results.get("trending_searches", [])

        if not trends:
            print("No trends found.")
            return

        for trend in trends[:10]:

            topic = trend.get("query")

            if not topic:
                continue

            print("Processing:", topic)

            # Generate summary (NOT explanation)
            summary = generate_summary(topic)

            # Save to database
            save_trend(topic, "Google Trends", summary)

            print("Saved:", topic)

        print("========== Agent Completed Successfully ==========")

    except Exception as e:
        print("Agent crash:", e)

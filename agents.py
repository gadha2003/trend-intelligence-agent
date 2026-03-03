from serpapi import GoogleSearch
from database import save_trend
from groq import Groq
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


# ===============================
# Generate AI Summary
# ===============================
def generate_reason(topic, headlines):

    try:
        prompt = f"""
Explain clearly in 2-3 short lines why this topic is trending in India.

Topic: {topic}

Related News:
{headlines}

Give factual explanation only.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )

        summary = response.choices[0].message.content.strip()

        print("Groq summary generated successfully")
        return summary

    except Exception as e:
        print("Groq error:", e)
        return "Live news coverage is driving public interest in this topic."


# ===============================
# Google Trends Agent
# ===============================
def google_trends_agent():

    print("========== AI Trend Agent Started ==========")

    try:

        params = {
            "engine": "google_trends_trending_now",
            "geo": "IN",
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        trends = results.get("trending_searches", [])

        for trend in trends[:10]:

            topic = trend.get("query")

            if topic:

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

                if not headlines.strip():
                    headlines = "General public discussion and online activity."

                # Generate AI explanation
                reason = generate_reason(topic, headlines)

                # Save
                save_trend(topic, "Google Trends", reason)

                print("Saved:", topic)

        print("========== Agent Completed Successfully ==========")

    except Exception as e:
        print("Critical Error:", e)

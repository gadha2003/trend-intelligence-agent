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
Summarize in 2–3 short lines what this topic is about and why it is trending in India.

Topic: {topic}

News Headlines:
{headlines}

Give only a clear factual explanation.
"""

        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        summary = response.choices[0].message.content.strip()

        print("Groq summary generated successfully")
        return summary

    except Exception as e:
        print("Groq error:", e)
        return "Summary unavailable."


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

                # --------------------------
                # Fetch Related News
                # --------------------------
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
                    headlines = "No major news coverage found."

                # --------------------------
                # Generate AI Summary
                # --------------------------
                reason = generate_reason(topic, headlines)

                # --------------------------
                # Save to Database
                # --------------------------
                save_trend(topic, "Google Trends", reason)

                print("Saved:", topic)

        print("========== Agent Completed Successfully ==========")

    except Exception as e:
        print("Critical Error:", e)

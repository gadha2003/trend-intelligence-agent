from serpapi import GoogleSearch
from database import save_trend
from groq import Groq
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def generate_reason(topic, headlines):

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


def google_trends_agent():

    print("Fetching Google Trends...")

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

                if headlines.strip() == "":
                    headlines = "No major news found."

                # Generate AI explanation
                reason = generate_reason(topic, headlines)

                # Save to database
                save_trend(topic, "Google Trends", reason)

                print("Saved:", topic)

        print("Agent completed.")

    except Exception as e:
        print("Error:", e)

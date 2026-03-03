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
# Generate Smart AI Explanation
# --------------------------------------------------
def generate_reason(topic, headlines):

    # Fallback if Groq key missing
    if not client:
        return f"{topic} is trending in India due to increased online searches and public attention."

    try:
        prompt = f"""
You are an AI trend intelligence analyst.

Explain clearly and specifically WHY this topic is trending in India.
Do NOT give generic reasons.
Use the news headlines to infer the actual cause.

Topic: {topic}

Related News Headlines:
{headlines}

Explain:
- What happened?
- Why are people searching it?
- What triggered the spike?

Answer in 2-4 concise sentences.
"""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )

        explanation = response.choices[0].message.content.strip()

        # Extra safety: Avoid generic output
        if "recent news developments" in explanation.lower():
            return f"{topic} is trending due to specific ongoing events and heightened public interest in India."

        return explanation

    except Exception as e:
        print("Groq error:", e)
        return f"{topic} is trending due to major public attention and related developments."


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

        print("Full SerpAPI Response:")
        print(results)

        # Handle API errors
        if "error" in results:
            print("SerpAPI Error:", results["error"])
            return

        # Handle multiple possible structures
        trends = []

        if "trending_searches" in results:
            trends = results["trending_searches"]

        elif "real_time_trends" in results:
            trends = results["real_time_trends"]

        elif "daily_searches" in results:
            trends = results["daily_searches"]

        else:
            print("No recognized trends key found.")
            print("Available keys:", results.keys())
            return

        if not trends:
            print("No trends found.")
            return

        # --------------------------------------------------
        # Process Top 10 Trends
        # --------------------------------------------------
        for trend in trends[:10]:

            # Support different response formats
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
                headlines = "No major news articles found."

            # Generate AI explanation
            reason = generate_reason(topic, headlines)

            # Save to database
            save_trend(topic, "Google Trends", reason)

            print("Saved:", topic)

        print("========== Agent Completed Successfully ==========")

    except Exception as e:
        print("Agent crash:", e)

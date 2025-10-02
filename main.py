from fastapi import FastAPI, Query
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Load API keys
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

@app.get("/trending")
def get_trending_news(category: str = Query(..., description="Category to filter news")):
    results = []

    # 1. NewsAPI
    newsapi_url = "https://newsapi.org/v2/top-headlines"
    newsapi_params = {
        "apiKey": NEWSAPI_KEY,
        "category": category,
        "language": "en",
        "pageSize": 5
    }
    try:
        newsapi_resp = requests.get(newsapi_url, params=newsapi_params)
        newsapi_data = newsapi_resp.json()
        for article in newsapi_data.get("articles", []):
            results.append({
                "source": "NewsAPI",
                "title": article["title"],
                "url": article["url"],
                "description": article.get("description")
            })
    except Exception as e:
        results.append({"source": "NewsAPI", "error": str(e)})

    # 2. Reddit (via subreddit search)
    reddit_url = f"https://www.reddit.com/r/{category}/hot.json"
    headers = {"User-Agent": "news-aggregator"}
    try:
        reddit_resp = requests.get(reddit_url, headers=headers)
        reddit_data = reddit_resp.json()
        for post in reddit_data.get("data", {}).get("children", [])[:5]:
            post_data = post["data"]
            results.append({
                "source": "Reddit",
                "title": post_data["title"],
                "url": f"https://www.reddit.com{post_data['permalink']}",
                "description": post_data.get("selftext", "")
            })
    except Exception as e:
        results.append({"source": "Reddit", "error": str(e)})

    # 3. Hacker News (via Algolia API)
    hn_url = "https://hn.algolia.com/api/v1/search"
    hn_params = {
        "query": category,
        "tags": "story",
        "hitsPerPage": 5
    }
    try:
        hn_resp = requests.get(hn_url, params=hn_params)
        hn_data = hn_resp.json()
        for item in hn_data.get("hits", []):
            results.append({
                "source": "Hacker News",
                "title": item["title"],
                "url": item["url"],
                "description": item.get("story_text", "")
            })
    except Exception as e:
        results.append({"source": "Hacker News", "error": str(e)})

    return {"articles": results}






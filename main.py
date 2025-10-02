from fastapi import FastAPI
from dotenv import load_dotenv
import requests, os
from datetime import datetime

load_dotenv()
app = FastAPI()

def get_newsdata_global():
    try:
        url = f"https://newsdata.io/api/1/news?apikey={os.getenv('NEWSDATA_KEY')}&language=en"
        res = requests.get(url).json()

        results = res.get("results", [])
        articles = []
        for a in results:
            if isinstance(a, dict):
                articles.append({
                    "title": a.get("title", "No title"),
                    "source": a.get("source_id", "Unknown"),
                    "url": a.get("link", ""),
                    "publishedAt": a.get("pubDate", "")
                })
            if len(articles) >= 10:
                break
        return articles
    except Exception as e:
        print(f"NewsData.io error: {e}")
        return []

@app.get("/trending")
def get_trending():
    articles = get_newsdata_global()
    return {"source": "NewsData.io", "articles": articles}

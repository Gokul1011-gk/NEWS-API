from fastapi import FastAPI, Query
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("NEWSDATA_KEY")
BASE_URL = "https://newsdata.io/api/1/news"

@app.get("/trending")
def get_filtered_news(
    category: str = Query(None, description="News category"),
    country: str = Query(None, description="Country code (e.g., 'in', 'us')"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Max articles to return")
):
    params = {
        "apikey": API_KEY,
        "language": "en",
        "page": page,
        "category": category,
        "country": country
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("results", [])[:limit]
        return {"articles": articles}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}




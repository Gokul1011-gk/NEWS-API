from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Optional: Allow public access from any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your NewsData.io API key from environment
API_KEY = os.getenv("NEWSDATA_KEY")
BASE_URL = "https://newsdata.io/api/1/news"

@app.get("/trending")
def get_trending(
    category: str = Query(None),
    country: str = Query(None),
    page: int = Query(1),
    limit: int = Query(10)
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

        # Limit the number of articles returned
        articles = data.get("results", [])[:limit]
        return {"articles": articles}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

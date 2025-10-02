from fastapi import FastAPI
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

API_KEY = os.getenv("NEWSDATA_KEY")
BASE_URL = "https://newsdata.io/api/1/news"

@app.get("/trending")
def get_global_news():
    params = {
        "apikey": API_KEY,
        "language": "en"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("results", [])
        return {"articles": articles}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}



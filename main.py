from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

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





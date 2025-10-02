 News Aggregator API
A FastAPI backend that fetches global news using NewsData.io with filters for category, country, pagination, and limit.

Setup Instructions
1. Clone the repository
bash
git clone https://github.com/your-username/news-aggregator
cd news-aggregator
Replace your-username with your actual GitHub username.

2. Create a virtual environment (optional but recommended)
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Add your NewsData.io API key
Create a .env file in the root folder:

env
NEWSDATA_KEY=your_actual_api_key
You can get a free API key from NewsData.io.

5. Run the server locally
bash
python -m uvicorn main:app --reload
Visit:

Code
http://localhost:8000/trending

Example Endpoints
/trending → All global news

/trending?category=technology&country=in → Tech news from India

/trending?category=sports&country=us&page=2 → Sports news from US, page 2

/trending?category=business&limit=5 → Business news, limit 5

Supported Categories
Code
business, entertainment, environment, food, health,
politics, science, sports, technology, top, world

Tech Stack
Python
FastAPI
NewsData.io
Uvicorn
Dotenv
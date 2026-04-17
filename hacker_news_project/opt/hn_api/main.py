from fastapi import FastAPI
from scraper import fetch_top_news

app = FastAPI(
    title="Hacker News API",
    description="An API that serves the top stories from Hacker News.",
    version="1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Hacker news API! Visit /api/news to get the data."}

@app.get("/api/news")
def get_news():
    print("Received a request for news. Fetching data...")
    data = fetch_top_news()
    
    return {
        "status": "success",
        "total_articles": len(data),
        "data": data
    }

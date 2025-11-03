"""
Simple News API Server for Testing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import feedparser
import uvicorn

app = FastAPI(title="Simple News API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Simple News API is running", "endpoints": ["/api/v1/news/health", "/api/v1/news/football-news"]}

@app.get("/api/v1/news/health")
def news_health():
    """News API health check"""
    return {"status": "ok", "service": "news", "endpoints": ["football-news"]}

@app.get("/api/v1/news/football-news")
def get_football_news():
    """Get football-specific news"""
    # Use NewsAPI with the provided key
    newsapi_key = "2543e26dac41497fa587ca31d6d9ecd8"
    
    try:
        # Try NewsAPI first
        newsapi_url = "https://newsapi.org/v2/everything"
        params = {
            "q": "football OR soccer OR Premier League",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 20,
            "apiKey": newsapi_key
        }
        
        response = requests.get(newsapi_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"NewsAPI returned status {response.status_code}")
    except Exception as e:
        print(f"NewsAPI error: {e}")
    
    # Fallback to RSS feeds
    try:
        feed = feedparser.parse("http://feeds.skysports.com/feeds/11095")
        articles = []
        
        for entry in feed.entries[:10]:
            article = {
                "title": entry.title,
                "description": entry.get('summary', ''),
                "url": entry.link,
                "publishedAt": entry.get('published', ''),
                "source": {"name": "Sky Sports Football"}
            }
            articles.append(article)
        
        return {
            "status": "ok",
            "totalResults": len(articles),
            "articles": articles
        }
    except Exception as e:
        print(f"RSS error: {e}")
        return {
            "status": "error",
            "message": "Unable to fetch news",
            "articles": []
        }

if __name__ == "__main__":
    print("🚀 Starting Simple News API Server...")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()
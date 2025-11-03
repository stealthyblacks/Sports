import requests
import feedparser
import os
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "2543e26dac41497fa587ca31d6d9ecd8")
NEWS_BASE_URL = "https://newsapi.org/v2/everything"

# RSS Feeds as fallback
RSS_FEEDS = [
    "https://feeds.bbci.co.uk/sport/rss.xml",
    "https://www.skysports.com/rss/12040", 
    "https://www.espn.com/espn/rss/news"
]

def clean_description(description: str, max_length: int = 150) -> str:
    """Clean and truncate description for better display."""
    if not description:
        return ""
    
    # Remove HTML tags and clean text
    import re
    clean_text = re.sub(r'<[^>]+>', '', description)
    clean_text = clean_text.strip()
    
    if len(clean_text) > max_length:
        clean_text = clean_text[:max_length] + "..."
    
    return clean_text

def format_publish_date(date_str: str) -> str:
    """Format publish date for consistent display."""
    try:
        from datetime import datetime
        if not date_str:
            return ""
        
        # Try parsing different date formats
        dt = None
        for fmt in ['%Y-%m-%dT%H:%M:%SZ', '%a, %d %b %Y %H:%M:%S %Z', '%Y-%m-%d %H:%M:%S']:
            try:
                dt = datetime.strptime(date_str, fmt)
                break
            except:
                continue
        
        if dt:
            return dt.strftime('%Y-%m-%d %H:%M')
        return date_str
    except:
        return date_str

@router.get("/sports-news")
async def get_sports_news(query: str = "football", limit: int = 8) -> Dict[str, Any]:
    """
    Fetch sports news from NewsAPI with RSS fallback.
    Focuses on football/soccer related content.
    """
    try:
        logger.info(f"Fetching sports news with query: {query}")
        
        # Try NewsAPI first if API key is available
        if NEWS_API_KEY and NEWS_API_KEY != "your_newsapi_key_here":
            try:
                # Enhanced query for better football content
                football_queries = f"{query} OR soccer OR premier league OR champions league OR football transfer"
                
                params = {
                    "q": football_queries,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": limit,
                    "apiKey": NEWS_API_KEY
                }
                
                response = requests.get(NEWS_BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if "articles" in data and len(data["articles"]) > 0:
                    articles = []
                    for article in data["articles"][:limit]:
                        # Filter out articles without proper content
                        if not article.get("title") or article.get("title") == "[Removed]":
                            continue
                            
                        articles.append({
                            "title": article["title"],
                            "description": clean_description(article.get("description", "")),
                            "url": article["url"],
                            "image": article.get("urlToImage", ""),
                            "source": article["source"]["name"],
                            "publishedAt": format_publish_date(article["publishedAt"]),
                            "category": "football"
                        })
                    
                    if articles:
                        logger.info(f"Successfully fetched {len(articles)} articles from NewsAPI")
                        return {
                            "source": "newsapi",
                            "articles": articles,
                            "total": len(articles),
                            "query": query
                        }

            except Exception as e:
                logger.warning(f"NewsAPI failed: {e}")

        # Fallback to RSS feeds
        logger.info("Falling back to RSS feeds")
        articles = []
        
        for feed_url in RSS_FEEDS:
            try:
                logger.info(f"Parsing RSS feed: {feed_url}")
                parsed_feed = feedparser.parse(feed_url)
                
                # Get feed info
                feed_title = parsed_feed.feed.get("title", "Sports News")
                
                for entry in parsed_feed.entries[:3]:  # Limit per feed
                    # Filter football-related content
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    
                    if any(keyword in (title + summary).lower() for keyword in 
                           ["football", "soccer", "premier", "champions", "uefa", "fifa"]):
                        
                        articles.append({
                            "title": title,
                            "description": clean_description(summary),
                            "url": entry.get("link", ""),
                            "image": "",  # RSS feeds typically don't have images
                            "source": feed_title,
                            "publishedAt": format_publish_date(entry.get("published", "")),
                            "category": "football"
                        })
                        
                if len(articles) >= limit:
                    break
                    
            except Exception as e:
                logger.warning(f"RSS feed {feed_url} failed: {e}")
                continue

        # Sort by publication date (newest first)
        articles = sorted(articles, key=lambda x: x.get("publishedAt", ""), reverse=True)
        articles = articles[:limit]
        
        logger.info(f"Successfully fetched {len(articles)} articles from RSS feeds")
        return {
            "source": "rss",
            "articles": articles,
            "total": len(articles),
            "query": query
        }

    except Exception as e:
        logger.error(f"Error fetching sports news: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch sports news: {str(e)}")

@router.get("/football-news") 
async def get_football_news(limit: int = 6) -> Dict[str, Any]:
    """Get specifically football-focused news."""
    return await get_sports_news(query="football premier league", limit=limit)

@router.get("/news/health")
async def news_health_check():
    """Health check endpoint for news service."""
    return {
        "status": "healthy",
        "newsapi_configured": NEWS_API_KEY != "your_newsapi_key_here",
        "rss_feeds_count": len(RSS_FEEDS)
    }
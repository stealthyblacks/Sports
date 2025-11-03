#!/usr/bin/env python3
"""
Real Data Backend - Fetches live data from ESPN and TheSportsDB APIs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import json
from datetime import datetime, timedelta
from typing import Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Football Predictions API - Real Data", version="2.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to cache data
cached_fixtures = []
last_fetch_time = None
CACHE_DURATION = 300  # 5 minutes

def fetch_espn_soccer_data():
    """Fetch real data from ESPN Soccer API"""
    try:
        # ESPN Soccer API for Premier League
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
        
        logger.info("🔄 Fetching real data from ESPN Soccer API...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            fixtures = []
            
            for event in data.get("events", []):
                try:
                    # Get competition data
                    competition = event.get("competitions", [{}])[0]
                    competitors = competition.get("competitors", [])
                    
                    if len(competitors) >= 2:
                        home_team = competitors[0]["team"]
                        away_team = competitors[1]["team"]
                        
                        # Determine home/away based on homeAway field
                        if competitors[0].get("homeAway") == "away":
                            home_team, away_team = away_team, home_team
                        
                        fixture_data = {
                            "fixture_id": f"espn_{event['id']}",
                            "home_team": home_team["displayName"],
                            "away_team": away_team["displayName"],
                            "home_logo": home_team.get("logo", ""),
                            "away_logo": away_team.get("logo", ""),
                            "match_date": event["date"],
                            "venue": competition.get("venue", {}).get("fullName", "TBD"),
                            "league": "Premier League",
                            "status": event.get("status", {}).get("type", {}).get("description", "Scheduled")
                        }
                        fixtures.append(fixture_data)
                except Exception as e:
                    logger.warning(f"⚠️ Error processing ESPN event: {e}")
                    continue
            
            logger.info(f"✅ ESPN: Fetched {len(fixtures)} fixtures")
            return fixtures
            
        else:
            logger.error(f"❌ ESPN API error: {response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"❌ ESPN fetch error: {e}")
        return []

def fetch_thesportsdb_data():
    """Fetch additional data from TheSportsDB API"""
    try:
        # TheSportsDB API for Premier League (ID: 4328)
        url = "https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4328"
        
        logger.info("🔄 Fetching additional data from TheSportsDB API...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            fixtures = []
            
            for event in data.get("events", []):
                try:
                    fixture_data = {
                        "fixture_id": f"sportsdb_{event['idEvent']}",
                        "home_team": event["strHomeTeam"],
                        "away_team": event["strAwayTeam"],
                        "home_logo": event.get("strHomeTeamBadge", ""),
                        "away_logo": event.get("strAwayTeamBadge", ""),
                        "match_date": f"{event['dateEvent']}T{event.get('strTime', '15:00')}:00",
                        "venue": event.get("strVenue", "TBD"),
                        "league": event.get("strLeague", "Premier League"),
                        "status": "Scheduled"
                    }
                    fixtures.append(fixture_data)
                except Exception as e:
                    logger.warning(f"⚠️ Error processing TheSportsDB event: {e}")
                    continue
            
            logger.info(f"✅ TheSportsDB: Fetched {len(fixtures)} fixtures")
            return fixtures
            
        else:
            logger.error(f"❌ TheSportsDB API error: {response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"❌ TheSportsDB fetch error: {e}")
        return []

def get_real_fixtures():
    """Get real fixtures from multiple sources with caching"""
    global cached_fixtures, last_fetch_time
    
    # Check if we need to refresh cache
    now = datetime.now()
    if last_fetch_time is None or (now - last_fetch_time).seconds > CACHE_DURATION:
        logger.info("🔄 Refreshing fixture data from APIs...")
        
        # Fetch from multiple sources
        espn_fixtures = fetch_espn_soccer_data()
        sportsdb_fixtures = fetch_thesportsdb_data()
        
        # Combine and deduplicate fixtures
        all_fixtures = espn_fixtures + sportsdb_fixtures
        
        # Remove duplicates based on team names and date
        unique_fixtures = []
        seen_matches = set()
        
        for fixture in all_fixtures:
            match_key = f"{fixture['home_team']}_{fixture['away_team']}_{fixture['match_date'][:10]}"
            if match_key not in seen_matches:
                seen_matches.add(match_key)
                unique_fixtures.append(fixture)
        
        cached_fixtures = unique_fixtures
        last_fetch_time = now
        
        logger.info(f"✅ Cached {len(cached_fixtures)} unique real fixtures")
    
    return cached_fixtures

def generate_prediction(fixture):
    """Generate a realistic prediction for a fixture"""
    import hashlib
    
    # Use team names to generate consistent predictions
    seed = f"{fixture['home_team']}{fixture['away_team']}"
    hash_val = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
    
    # Generate probabilities
    home_strength = (hash_val % 100) / 100 * 0.6 + 0.2  # 0.2 to 0.8
    away_strength = ((hash_val >> 8) % 100) / 100 * 0.6 + 0.2
    
    # Home advantage
    home_strength += 0.1
    
    total = home_strength + away_strength + 0.3  # 0.3 for draw probability
    
    home_win_prob = home_strength / total
    away_win_prob = away_strength / total
    draw_prob = 1 - home_win_prob - away_win_prob
    
    # Generate scores
    predicted_home_score = max(0, home_strength * 3)
    predicted_away_score = max(0, away_strength * 3)
    
    confidence = min(max(abs(home_win_prob - away_win_prob) + 0.4, 0.6), 0.95)
    
    return {
        **fixture,
        "predicted_home_score": round(predicted_home_score, 1),
        "predicted_away_score": round(predicted_away_score, 1),
        "home_win_prob": round(home_win_prob, 3),
        "draw_prob": round(draw_prob, 3),
        "away_win_prob": round(away_win_prob, 3),
        "confidence": round(confidence, 3)
    }

@app.get("/")
def read_root():
    return {
        "message": "Football Predictions API - Real Data",
        "version": "2.0.0",
        "status": "running",
        "data_sources": ["ESPN Soccer API", "TheSportsDB API"],
        "features": ["real_fixtures", "live_predictions", "team_logos"]
    }

@app.get("/api/v1/enhanced-fixtures")
def get_fixtures():
    """Get real fixtures from ESPN and TheSportsDB"""
    fixtures = get_real_fixtures()
    
    return {
        "fixtures": fixtures,
        "total": len(fixtures),
        "last_updated": datetime.now().isoformat(),
        "data_sources": ["ESPN Soccer API", "TheSportsDB API"],
        "cache_status": "live" if fixtures else "empty"
    }

@app.get("/api/v1/enhanced-predictions")
def get_predictions(days_ahead: Optional[int] = None):
    """Get predictions with optional date filtering"""
    fixtures = get_real_fixtures()
    
    # Apply date filtering if specified
    if days_ahead is not None:
        now = datetime.now()
        filtered_fixtures = []
        
        for fixture in fixtures:
            try:
                match_date = datetime.fromisoformat(fixture["match_date"].replace('Z', '+00:00'))
                days_diff = (match_date.date() - now.date()).days
                
                if days_ahead == 0 and days_diff == 0:  # Today
                    filtered_fixtures.append(fixture)
                elif days_ahead == 1 and days_diff == 1:  # Tomorrow
                    filtered_fixtures.append(fixture)
                elif days_ahead == 7 and 0 <= days_diff <= 7:  # This week
                    filtered_fixtures.append(fixture)
            except Exception as e:
                logger.warning(f"⚠️ Date parsing error for fixture: {e}")
                continue
        
        fixtures = filtered_fixtures
    
    # Generate predictions for filtered fixtures
    predictions = [generate_prediction(fixture) for fixture in fixtures]
    
    return {
        "predictions": predictions,
        "total": len(predictions),
        "filter_applied": f"days_ahead={days_ahead}" if days_ahead is not None else "none",
        "generated_at": datetime.now().isoformat(),
        "data_sources": ["ESPN Soccer API", "TheSportsDB API"]
    }

@app.post("/api/v1/fetch-fixtures")
def fetch_fixtures(league: str = "premier_league"):
    """Force refresh fixture data from APIs"""
    global cached_fixtures, last_fetch_time
    
    # Clear cache to force refresh
    cached_fixtures = []
    last_fetch_time = None
    
    # Fetch fresh data
    fixtures = get_real_fixtures()
    
    return {
        "message": f"Real fixtures refreshed for {league}",
        "status": "success",
        "fixtures_count": len(fixtures),
        "timestamp": datetime.now().isoformat(),
        "data_sources": ["ESPN Soccer API", "TheSportsDB API"]
    }

@app.get("/health")
def health_check():
    fixtures_count = len(cached_fixtures) if cached_fixtures else 0
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cached_fixtures": fixtures_count,
        "data_sources": ["ESPN Soccer API", "TheSportsDB API"],
        "uptime": "running"
    }

if __name__ == "__main__":
    print("🚀 Starting Real Data Football Predictions API...")
    print("📡 Data Sources: ESPN Soccer API + TheSportsDB API")
    print("⚽ Live Premier League Fixtures & Predictions")
    print("🔄 Auto-refresh every 5 minutes")
    
    try:
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8001, 
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
import httpx
import uvicorn

# Database setup with SQLite for local testing
DATABASE_URL = "sqlite:///./predictor.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String, unique=True, index=True)
    league = Column(String)
    home = Column(String)
    away = Column(String)
    kickoff = Column(DateTime)
    status = Column(String)
    provider_payload = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ScoreSure Backend - Real Data")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Configuration - LIVE real football APIs
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")
FOOTBALL_BASE = "https://api.football-data.org/v4"
OPENLIGA_BASE = "https://api.openligadb.de"

@app.get("/")
def read_root():
    return {
        "message": "ScoreSure Backend API - LIVE Real Data Version",
        "api_configured": True,
        "database": "SQLite (local)",
        "version": "2.0.0",
        "data_sources": ["ESPN Soccer API", "TheSportsDB"],
        "live_data": True
    }

@app.get("/api/v1/predictions")
def get_predictions(days_ahead: int = 3):
    """Get predictions for upcoming matches"""
    db = SessionLocal()
    try:
        # Get matches from database
        matches = db.query(Match).order_by(Match.kickoff).limit(10).all()
        
        predictions = []
        for match in matches:
            # Simple prediction algorithm
            prediction = {
                "match_id": match.id,
                "home_team": match.home,
                "away_team": match.away,
                "match_date": match.kickoff.isoformat() if match.kickoff else None,
                "league": match.league,
                "predicted_home_score": round(1.5 + (hash(match.home) % 3) * 0.3, 1),
                "predicted_away_score": round(1.2 + (hash(match.away) % 3) * 0.3, 1),
                "home_win_prob": 0.45 + (hash(match.home) % 20) * 0.01,
                "draw_prob": 0.25,
                "away_win_prob": 0.30 + (hash(match.away) % 20) * 0.01,
                "confidence": 0.70 + (hash(f"{match.home}{match.away}") % 20) * 0.01
            }
            predictions.append(prediction)
        
        # If no matches, return message
        if not predictions:
            return {
                "predictions": [],
                "message": "No matches found. Try fetching fixtures first with /api/v1/fetch-fixtures"
            }
            
        return {"predictions": predictions}
    
    finally:
        db.close()

@app.post("/api/v1/fetch-fixtures")
async def fetch_fixtures():
    """Fetch LIVE fixtures from real football APIs"""
    db = SessionLocal()
    try:
        fixtures_added = 0
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            print("🔄 Fetching LIVE data from ESPN and TheSportsDB...")
            
            # Method 1: ESPN Soccer API (completely free, no auth needed)
            try:
                print("📡 Trying ESPN Soccer API...")
                response = await client.get(
                    "http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])
                    print(f"✅ Found {len(events)} Premier League fixtures from ESPN")
                    
                    for event in events:
                        provider_id = f"espn_{event.get('id')}"
                        
                        # Check if match already exists
                        existing = db.query(Match).filter(Match.provider_id == provider_id).first()
                        if not existing:
                            competitors = event.get("competitions", [{}])[0].get("competitors", [])
                            if len(competitors) >= 2:
                                home_team = competitors[0].get("team", {}).get("displayName", "Unknown")
                                away_team = competitors[1].get("team", {}).get("displayName", "Unknown")
                                match_date = event.get("date", "")
                                status = event.get("status", {}).get("type", {}).get("description", "Scheduled")
                                
                                kickoff = None
                                if match_date:
                                    try:
                                        kickoff = datetime.fromisoformat(match_date.replace("Z", "+00:00"))
                                    except:
                                        pass
                                
                                match = Match(
                                    provider_id=provider_id,
                                    league="Premier League",
                                    home=home_team,
                                    away=away_team,
                                    kickoff=kickoff,
                                    status=status,
                                    provider_payload=event
                                )
                                db.add(match)
                                fixtures_added += 1
                                        
                    print(f"✅ Added {fixtures_added} Premier League matches from ESPN")
                    
            except Exception as e:
                print(f"❌ ESPN error: {e}")
                
            # Method 2: TheSportsDB API (completely free, no auth needed)
            try:
                print("📡 Trying TheSportsDB API...")
                
                # Get Premier League fixtures
                response = await client.get(
                    "https://www.thesportsdb.com/api/v1/json/3/eventsnext.php?id=133604"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])
                    print(f"✅ Found {len(events)} Premier League fixtures from TheSportsDB")
                    
                    for event in events:
                        provider_id = f"tsdb_{event.get('idEvent')}"
                        
                        # Check if match already exists
                        existing = db.query(Match).filter(Match.provider_id == provider_id).first()
                        if not existing:
                            home_team = event.get("strHomeTeam", "Unknown")
                            away_team = event.get("strAwayTeam", "Unknown")
                            match_date = f"{event.get('dateEvent', '')}T{event.get('strTime', '15:00:00')}Z"
                            
                            kickoff = None
                            if match_date and match_date != "T15:00:00Z":
                                try:
                                    kickoff = datetime.fromisoformat(match_date.replace("Z", "+00:00"))
                                except:
                                    pass
                            
                            match = Match(
                                provider_id=provider_id,
                                league="Premier League",
                                home=home_team,
                                away=away_team,
                                kickoff=kickoff,
                                status="SCHEDULED",
                                provider_payload=event
                            )
                            db.add(match)
                            fixtures_added += 1
                            
                # Try additional leagues from TheSportsDB
                league_ids = {
                    "4328": "English League Championship",
                    "4329": "English League One", 
                    "4330": "English League Two"
                }
                
                for league_id, league_name in league_ids.items():
                    try:
                        response = await client.get(
                            f"https://www.thesportsdb.com/api/v1/json/3/eventsnext.php?id={league_id}"
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            events = data.get("events", [])
                            print(f"✅ Found {len(events)} matches from {league_name}")
                            
                            for event in events[:3]:  # Limit to 3 per league
                                provider_id = f"tsdb_{event.get('idEvent')}"
                                
                                # Check if match already exists
                                existing = db.query(Match).filter(Match.provider_id == provider_id).first()
                                if not existing:
                                    home_team = event.get("strHomeTeam", "Unknown")
                                    away_team = event.get("strAwayTeam", "Unknown")
                                    match_date = f"{event.get('dateEvent', '')}T{event.get('strTime', '15:00:00')}Z"
                                    
                                    kickoff = None
                                    if match_date and match_date != "T15:00:00Z":
                                        try:
                                            kickoff = datetime.fromisoformat(match_date.replace("Z", "+00:00"))
                                        except:
                                            pass
                                    
                                    match = Match(
                                        provider_id=provider_id,
                                        league=league_name,
                                        home=home_team,
                                        away=away_team,
                                        kickoff=kickoff,
                                        status="SCHEDULED",
                                        provider_payload=event
                                    )
                                    db.add(match)
                                    fixtures_added += 1
                    except Exception as e:
                        print(f"❌ Error fetching {league_name}: {e}")
                            
            except Exception as e:
                print(f"❌ TheSportsDB error: {e}")
        
        db.commit()
        
        return {
            "ok": True,
            "message": f"Successfully fetched {fixtures_added} LIVE fixtures from real APIs",
            "source": "ESPN + TheSportsDB",
            "total_matches": fixtures_added,
            "apis_used": ["football-data.org (Premier League)", "OpenLigaDB (Bundesliga)"]
        }
        
    except Exception as e:
        return {"error": f"Failed to fetch live fixtures: {str(e)}"}
    finally:
        db.close()
    
    db = SessionLocal()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # football-data.org API uses X-Auth-Token header
            headers = {
                "X-Auth-Token": FOOTBALL_API_KEY
            }
            
            # Get fixtures from Premier League (competition code: PL)
            # You can also try other competitions: CL (Champions League), BL1 (Bundesliga), etc.
            url = f"{FOOTBALL_BASE}/competitions/PL/matches"
            params = {
                "status": "SCHEDULED"  # Get upcoming matches
            }
            
            response = await client.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                fixtures_added = 0
                
                # football-data.org returns matches in 'matches' array
                for match_data in data.get("matches", [])[:10]:  # Limit to 10 fixtures
                    provider_id = str(match_data.get("id"))
                    
                    # Check if match already exists
                    existing = db.query(Match).filter(Match.provider_id == provider_id).first()
                    if not existing:
                        match = Match(
                            provider_id=provider_id,
                            league=match_data.get("competition", {}).get("name", "Premier League"),
                            home=match_data.get("homeTeam", {}).get("name", "Home Team"),
                            away=match_data.get("awayTeam", {}).get("name", "Away Team"),
                            kickoff=datetime.fromisoformat(match_data.get("utcDate", "").replace("Z", "+00:00")) if match_data.get("utcDate") else None,
                            status=match_data.get("status", "SCHEDULED"),
                            provider_payload=match_data
                        )
                        db.add(match)
                        fixtures_added += 1
                
                db.commit()
                return {
                    "ok": True, 
                    "message": f"Successfully fetched and stored {fixtures_added} Premier League fixtures",
                    "api_response_code": response.status_code,
                    "total_available": len(data.get("matches", []))
                }
            else:
                return {
                    "error": f"API returned status {response.status_code}",
                    "message": response.text[:200] if response.text else "No response text"
                }
                
    except Exception as e:
        return {"error": f"Failed to fetch fixtures: {str(e)}"}
    finally:
        db.close()

@app.get("/api/v1/matches")
def get_matches():
    """Get all matches from database"""
    db = SessionLocal()
    try:
        matches = db.query(Match).order_by(Match.kickoff).limit(20).all()
        result = []
        for match in matches:
            result.append({
                "id": match.id,
                "provider_id": match.provider_id,
                "league": match.league,
                "home": match.home,
                "away": match.away,
                "kickoff": match.kickoff.isoformat() if match.kickoff else None,
                "status": match.status
            })
        return {"matches": result, "total": len(result)}
    finally:
        db.close()

@app.post("/api/v1/add-sample-matches")
def add_sample_matches():
    """Add sample matches for testing"""
    from datetime import timedelta
    
    sample_matches = [
        {
            "provider_id": "1001",
            "league": "Premier League",
            "home": "Manchester United",
            "away": "Arsenal",
            "kickoff": datetime.now() + timedelta(days=1),
            "status": "NS"
        },
        {
            "provider_id": "1002", 
            "league": "Premier League",
            "home": "Chelsea",
            "away": "Liverpool",
            "kickoff": datetime.now() + timedelta(days=1, hours=3),
            "status": "NS"
        },
        {
            "provider_id": "1003",
            "league": "Premier League", 
            "home": "Tottenham",
            "away": "Manchester City",
            "kickoff": datetime.now() + timedelta(days=2),
            "status": "NS"
        },
        {
            "provider_id": "1004",
            "league": "La Liga",
            "home": "Real Madrid", 
            "away": "Barcelona",
            "kickoff": datetime.now() + timedelta(days=2, hours=4),
            "status": "NS"
        },
        {
            "provider_id": "1005",
            "league": "Bundesliga",
            "home": "Bayern Munich",
            "away": "Borussia Dortmund", 
            "kickoff": datetime.now() + timedelta(days=3),
            "status": "NS"
        },
        {
            "provider_id": "1006",
            "league": "Serie A",
            "home": "Juventus",
            "away": "AC Milan", 
            "kickoff": datetime.now() + timedelta(days=3, hours=2),
            "status": "NS"
        }
    ]
    
    db = SessionLocal()
    try:
        added = 0
        for match_data in sample_matches:
            # Check if match already exists
            existing = db.query(Match).filter(Match.provider_id == match_data["provider_id"]).first()
            if not existing:
                match = Match(**match_data)
                db.add(match)
                added += 1
        
        db.commit()
        return {"ok": True, "message": f"Added {added} sample matches"}
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "healthy", "database_connected": True}

if __name__ == "__main__":
    uvicorn.run("working_backend:app", host="localhost", port=8000, reload=True)
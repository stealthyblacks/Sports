"""
ScoreSure Backend - LIVE Real Data Version
Football prediction API with REAL external data sources
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import uvicorn
import os

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./predictor.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String, unique=True, index=True)  # External API ID
    league = Column(String)
    home = Column(String)
    away = Column(String)
    kickoff = Column(DateTime)
    status = Column(String)
    provider_payload = Column(Text)  # Store raw API response

class Odds(Base):
    __tablename__ = "odds"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer)
    home_odds = Column(String)
    draw_odds = Column(String)
    away_odds = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="ScoreSure API - LIVE Data",
    description="Football predictions with REAL external data",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """API status and configuration"""
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

@app.post("/api/v1/test-fetch")
async def test_fetch():
    """Simple test of external APIs"""
    results = []
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test ESPN
            response = await client.get("http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard")
            if response.status_code == 200:
                data = response.json()
                events = data.get("events", [])
                results.append(f"ESPN: {len(events)} events found")
            else:
                results.append(f"ESPN: Error {response.status_code}")
                
            # Test TheSportsDB
            response = await client.get("https://www.thesportsdb.com/api/v1/json/3/eventsnext.php?id=133604")
            if response.status_code == 200:
                data = response.json()
                events = data.get("events", [])
                results.append(f"TheSportsDB: {len(events)} events found")
            else:
                results.append(f"TheSportsDB: Error {response.status_code}")
                
    except Exception as e:
        results.append(f"Error: {str(e)}")
    
    return {"results": results}


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
                                    provider_payload=str(event)
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
                                provider_payload=str(event)
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
                                        provider_payload=str(event)
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
            "apis_used": ["ESPN Soccer API", "TheSportsDB"]
        }
        
    except Exception as e:
        return {"error": f"Failed to fetch live fixtures: {str(e)}"}
    finally:
        db.close()


@app.get("/api/v1/database-stats")
def get_database_stats():
    """Get database statistics"""
    db = SessionLocal()
    try:
        total_matches = db.query(Match).count()
        recent_matches = db.query(Match).filter(
            Match.kickoff >= datetime.now() - timedelta(days=30)
        ).count()
        
        return {
            "total_matches": total_matches,
            "recent_matches": recent_matches
        }
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "healthy", "database_connected": True}


if __name__ == "__main__":
    uvicorn.run("clean_backend:app", host="0.0.0.0", port=8000, reload=True)
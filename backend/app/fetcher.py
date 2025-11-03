import os, httpx, logging
from datetime import datetime
from db import SessionLocal
from models import Match, Odds

FOOTBALL_KEY = os.getenv("FOOTBALL_API_KEY")
ODDS_KEY = os.getenv("ODDS_API_KEY")
FOOTBALL_BASE = os.getenv("FOOTBALL_BASE", "https://api-football.example")

async def fetch_fixtures():
    # using httpx for async
    async with httpx.AsyncClient(timeout=30) as client:
        # example endpoint; replace with your API's path
        r = await client.get(f"{FOOTBALL_BASE}/fixtures?date=today", headers={"x-apisports-key":FOOTBALL_KEY})
        r.raise_for_status()
        data = r.json()
        # store into DB (simplified)
        db = SessionLocal()
        try:
            for f in data.get("response", []):
                pid = str(f.get("fixture", {}).get("id") or f.get("id"))
                kickoff = f.get("fixture", {}).get("date")
                m = db.query(Match).filter(Match.provider_id == pid).first()
                if not m:
                    m = Match(provider_id=pid, league=f.get("league", {}).get("name"), home=f.get("teams", {}).get("home", {}).get("name"),
                              away=f.get("teams", {}).get("away", {}).get("name"), kickoff=kickoff, status=f.get("fixture", {}).get("status", {}).get("short"),
                              provider_payload=f)
                    db.add(m)
                else:
                    m.provider_payload = f
            db.commit()
        finally:
            db.close()
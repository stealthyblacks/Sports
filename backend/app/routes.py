from fastapi import APIRouter, Depends
from db import SessionLocal
from models import Match
from fetcher import fetch_fixtures
from predictions import run_prediction_job
from fastapi import BackgroundTasks

router = APIRouter()

@router.get("/api/today")
def api_today():
    db = SessionLocal()
    try:
        rows = db.query(Match).order_by(Match.kickoff).limit(200).all()
        out = []
        for m in rows:
            out.append({
                "id": m.id,
                "match_id": m.provider_id,
                "league": m.league,
                "home": m.home,
                "away": m.away,
                "kickoff": m.kickoff.isoformat() if m.kickoff else None
            })
        return out
    finally:
        db.close()

@router.post("/api/fetchMatches")
async def api_fetch_matches(background: BackgroundTasks):
    # schedule fetch in background to return quickly
    background.add_task(fetch_fixtures)
    return {"ok": True}
"""
Quick script to add sample data to the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_backend import SessionLocal, Match
from datetime import datetime, timedelta

def add_sample_data():
    db = SessionLocal()
    try:
        # Sample matches
        sample_matches = [
            {
                "provider_id": "sample_001",
                "league": "Premier League",
                "home": "Manchester City",
                "away": "Liverpool", 
                "kickoff": datetime.now() + timedelta(days=2),
                "status": "SCHEDULED",
                "provider_payload": "Sample data"
            },
            {
                "provider_id": "sample_002",
                "league": "Premier League", 
                "home": "Arsenal",
                "away": "Chelsea",
                "kickoff": datetime.now() + timedelta(days=3),
                "status": "SCHEDULED",
                "provider_payload": "Sample data"
            },
            {
                "provider_id": "sample_003",
                "league": "Premier League",
                "home": "Manchester United", 
                "away": "Tottenham",
                "kickoff": datetime.now() + timedelta(days=4),
                "status": "SCHEDULED",
                "provider_payload": "Sample data"
            },
            {
                "provider_id": "sample_004",
                "league": "Premier League",
                "home": "Newcastle United",
                "away": "Brighton",
                "kickoff": datetime.now() + timedelta(days=5),
                "status": "SCHEDULED", 
                "provider_payload": "Sample data"
            },
            {
                "provider_id": "sample_005",
                "league": "Premier League",
                "home": "West Ham",
                "away": "Everton",
                "kickoff": datetime.now() + timedelta(days=6),
                "status": "SCHEDULED",
                "provider_payload": "Sample data"
            }
        ]
        
        added = 0
        for match_data in sample_matches:
            # Check if match already exists
            existing = db.query(Match).filter(Match.provider_id == match_data["provider_id"]).first()
            if not existing:
                match = Match(**match_data)
                db.add(match)
                added += 1
        
        db.commit()
        print(f"Successfully added {added} sample matches to database")
        return True
        
    except Exception as e:
        print(f"Error adding sample data: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()
from db import SessionLocal
from models import Match
import math

def compute_simple_pick(home_elo=1500, away_elo=1500, home_adv=50):
    eh = home_elo + home_adv
    ea = away_elo
    ph = math.exp(eh/400)
    pa = math.exp(ea/400)
    p_home = ph/(ph+pa)
    p_away = pa/(ph+pa)
    p_draw = max(0.05, 1 - (p_home + p_away))
    return {"p_home": p_home, "p_draw": p_draw, "p_away": p_away}

def run_prediction_job():
    db = SessionLocal()
    try:
        matches = db.query(Match).filter(Match.status == 'SCHEDULED').all()
        results = []
        for m in matches:
            # placeholder: use team names to get elo from a lookup (omitted)
            pick = compute_simple_pick()
            best = max(("home", pick["p_home"]), ("draw", pick["p_draw"]), ("away", pick["p_away"]), key=lambda x: x[1])
            results.append({"match_id": m.id, "pick": best[0], "confidence": int(best[1]*100)})
        return results
    finally:
        db.close()
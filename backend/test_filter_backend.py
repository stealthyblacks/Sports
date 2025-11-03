from fastapi import FastAPI
import uvicorn
from datetime import datetime, timedelta

app = FastAPI()

# Sample data for testing filters
sample_predictions = [
    {
        "fixture_id": "test_1",
        "home_team": "Test Team 1",
        "away_team": "Test Team 2", 
        "match_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),  # Today
        "home_win_prob": 0.6,
        "draw_prob": 0.2,
        "away_win_prob": 0.2,
        "confidence": 0.8
    },
    {
        "fixture_id": "test_2", 
        "home_team": "Test Team 3",
        "away_team": "Test Team 4",
        "match_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),  # Tomorrow
        "home_win_prob": 0.4,
        "draw_prob": 0.3,
        "away_win_prob": 0.3,
        "confidence": 0.7
    },
    {
        "fixture_id": "test_3",
        "home_team": "Test Team 5", 
        "away_team": "Test Team 6",
        "match_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S"),  # This week
        "home_win_prob": 0.5,
        "draw_prob": 0.3, 
        "away_win_prob": 0.2,
        "confidence": 0.9
    }
]

@app.get("/api/v1/enhanced-predictions")
def get_test_predictions(days_ahead: int = None):
    """Test endpoint for filter functionality"""
    
    predictions = sample_predictions.copy()
    
    if days_ahead is not None:
        now = datetime.now()
        filtered_predictions = []
        
        for pred in predictions:
            match_date = datetime.fromisoformat(pred["match_date"])
            days_diff = (match_date.date() - now.date()).days
            
            if days_ahead == 0 and days_diff == 0:  # Today
                filtered_predictions.append(pred)
            elif days_ahead == 1 and days_diff == 1:  # Tomorrow  
                filtered_predictions.append(pred)
            elif days_ahead == 7 and 0 <= days_diff <= 7:  # This week
                filtered_predictions.append(pred)
        
        predictions = filtered_predictions
    
    return {
        "predictions": predictions,
        "total": len(predictions),
        "filter_applied": f"days_ahead={days_ahead}" if days_ahead is not None else "none"
    }

if __name__ == "__main__":
    print("🧪 Starting Test Filter Backend on port 8002...")
    uvicorn.run(app, host="127.0.0.1", port=8002, reload=False)
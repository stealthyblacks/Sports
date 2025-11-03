from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="ScoreSure Backend")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ScoreSure Backend API"}

@app.get("/api/v1/predictions")
def get_predictions(days_ahead: int = 3):
    # Mock data for testing
    mock_predictions = [
        {
            "match_id": 1,
            "home_team": "Manchester United",
            "away_team": "Arsenal",
            "match_date": "2025-10-15T15:00:00Z",
            "predicted_home_score": 2.1,
            "predicted_away_score": 1.3,
            "home_win_prob": 0.65,
            "draw_prob": 0.20,
            "away_win_prob": 0.15,
            "confidence": 0.82
        },
        {
            "match_id": 2,
            "home_team": "Chelsea",
            "away_team": "Liverpool",
            "match_date": "2025-10-15T17:30:00Z",
            "predicted_home_score": 1.8,
            "predicted_away_score": 2.2,
            "home_win_prob": 0.35,
            "draw_prob": 0.25,
            "away_win_prob": 0.40,
            "confidence": 0.78
        },
        {
            "match_id": 3,
            "home_team": "Tottenham",
            "away_team": "Manchester City",
            "match_date": "2025-10-16T14:00:00Z",
            "predicted_home_score": 1.2,
            "predicted_away_score": 2.8,
            "home_win_prob": 0.25,
            "draw_prob": 0.20,
            "away_win_prob": 0.55,
            "confidence": 0.85
        },
        {
            "match_id": 4,
            "home_team": "Newcastle",
            "away_team": "Brighton",
            "match_date": "2025-10-16T16:30:00Z",
            "predicted_home_score": 2.3,
            "predicted_away_score": 1.1,
            "home_win_prob": 0.70,
            "draw_prob": 0.18,
            "away_win_prob": 0.12,
            "confidence": 0.79
        },
        {
            "match_id": 5,
            "home_team": "Wolves",
            "away_team": "Crystal Palace",
            "match_date": "2025-10-17T20:00:00Z",
            "predicted_home_score": 1.5,
            "predicted_away_score": 1.5,
            "home_win_prob": 0.40,
            "draw_prob": 0.35,
            "away_win_prob": 0.25,
            "confidence": 0.72
        },
        {
            "match_id": 6,
            "home_team": "Aston Villa",
            "away_team": "West Ham",
            "match_date": "2025-10-17T15:00:00Z",
            "predicted_home_score": 2.0,
            "predicted_away_score": 1.4,
            "home_win_prob": 0.58,
            "draw_prob": 0.23,
            "away_win_prob": 0.19,
            "confidence": 0.76
        }
    ]
    
    return {"predictions": mock_predictions}

if __name__ == "__main__":
    uvicorn.run("simple_main:app", host="localhost", port=8000, reload=True)
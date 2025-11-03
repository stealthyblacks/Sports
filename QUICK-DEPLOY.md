# ScoreSure Quick Deployment Guide

## 🚀 Local Development

### Prerequisites
- Docker and Docker Compose
- Node.js 18+
- Git

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/predictor.git
cd predictor

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Start backend services
cd infra
docker-compose up --build

# Start frontend (new terminal)
cd ../frontend
npm install
npm run dev

# Visit application
open http://localhost:3000
```

## ☁️ Production Deployment

### Option 1: Vercel + Railway (Recommended)

#### Deploy Frontend to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel

# Set environment variables in Vercel dashboard:
# BACKEND_URL=https://your-backend.railway.app
```

#### Deploy Backend to Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
cd backend
railway deploy

# Set environment variables in Railway dashboard:
# DATABASE_URL=postgresql://postgres:password@host:5432/railway
# FOOTBALL_API_KEY=your_api_key
# ODDS_API_KEY=your_odds_key
```

### Option 2: Vercel + Render

#### Deploy Backend to Render
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create new "Web Service"
4. Configure:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     ```
     DATABASE_URL=postgresql://user:pass@host:5432/database
     FOOTBALL_API_KEY=your_api_key
     ODDS_API_KEY=your_odds_key
     ```

#### Deploy Database
1. Create PostgreSQL database in Render
2. Copy "Internal Database URL"
3. Set as `DATABASE_URL` in your web service

## 🔄 Automation Setup

### Vercel Cron Jobs
Create `vercel.json` in frontend root:
```json
{
  "crons": [
    {
      "path": "/api/proxy?path=fetchMatches",
      "schedule": "0 6 * * *"
    }
  ]
}
```

### External Cron (cron-job.org)
1. Go to [cron-job.org](https://cron-job.org)
2. Create free account
3. Add new cron job:
   - **URL:** `https://your-backend.com/api/fetchMatches`
   - **Method:** POST
   - **Schedule:** Daily at 06:00
   - **Headers:** `Content-Type: application/json`

### VPS/Server Cron
```bash
# Edit crontab
crontab -e

# Add daily fixture fetch
0 6 * * * curl -s -X POST https://your-backend.com/api/fetchMatches >/tmp/fetch_matches.log 2>&1

# Add daily predictions
5 2 * * * /usr/bin/python3 /srv/predictor/backend/scripts/run_predictions.py >> /srv/predictor/logs/predictions.log 2>&1
```

## 🗄️ Database Setup

### Local Development
```bash
# Start PostgreSQL via Docker Compose
cd infra
docker-compose up db -d

# Connect to database
psql postgresql://postgres:postgres@localhost:5432/predictor

# Create tables (automatic via SQLAlchemy)
```

### Production
```bash
# Railway/Render provide managed PostgreSQL
# Tables are created automatically on first app startup

# Manual table creation if needed:
python -c "
from app.db import engine, Base
from app.models import Match, Odds
Base.metadata.create_all(bind=engine)
print('Tables created successfully!')
"
```

## 🔐 Security Checklist

### Environment Variables
- [ ] Never commit `.env` files to Git
- [ ] Use different API keys for dev/staging/production
- [ ] Rotate API keys regularly
- [ ] Set strong database passwords

### HTTPS & CDN
- [ ] Enable HTTPS (automatic on Vercel/Railway/Render)
- [ ] Configure Cloudflare for CDN and WAF
- [ ] Set proper CORS headers
- [ ] Enable security headers

### Rate Limiting
```python
# Add to backend for API protection
from fastapi import HTTPException
import time

# Simple rate limiting
last_request = {}

@router.post("/api/fetchMatches")
def fetch_matches():
    client_ip = request.client.host
    now = time.time()
    
    if client_ip in last_request and now - last_request[client_ip] < 300:  # 5 minutes
        raise HTTPException(429, "Rate limit exceeded")
    
    last_request[client_ip] = now
    # ... rest of function
```

## 📊 Monitoring & Logging

### Application Monitoring
```python
# Add to backend/app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.3f}s")
    return response
```

### Health Checks
```python
# Add to backend routes
@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "database": "connected"  # Add DB check if needed
    }
```

## 🔄 One-Click Automation

### Daily Data Fetch
```bash
# HTTP Request (for cron services)
POST https://your-backend.com/api/fetchMatches
Content-Type: application/json
Body: {}

# Response
{
  "ok": true,
  "message": "Fixture fetch scheduled"
}
```

### Testing the Automation
```bash
# Test locally
curl -X POST http://localhost:8000/api/fetchMatches

# Test production
curl -X POST https://your-backend.com/api/fetchMatches

# Check logs
# Railway: railway logs
# Render: Check dashboard logs
# Local: docker-compose logs backend
```

## 🚨 Troubleshooting

### Common Issues

**Database Connection Errors:**
```bash
# Check DATABASE_URL format
# Railway: postgresql://postgres:password@host:5432/railway
# Render: postgresql://user:password@host:5432/database_name
```

**Build Failures:**
```bash
# Check Python version (3.11)
# Verify requirements.txt
# Check Docker build logs
```

**API Rate Limits:**
```bash
# Monitor API usage
# Implement exponential backoff
# Use multiple API keys if needed
```

**CORS Issues:**
```python
# Add CORS middleware if needed
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📱 Mobile Optimization

### PWA Setup (Optional)
```json
// frontend/public/manifest.json
{
  "name": "ScoreSure",
  "short_name": "ScoreSure",
  "description": "AI Football Predictions",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3b82f6",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

### Responsive Design
- All pages use Tailwind CSS responsive classes
- Mobile-first design approach
- Touch-friendly interface elements
- Optimized loading for mobile networks

---

## 🎯 Quick Reference Commands

```bash
# Local development
docker-compose up --build    # Start all services
npm run dev                  # Start frontend only

# Deployment
vercel --prod               # Deploy frontend
railway deploy              # Deploy backend

# Database
psql $DATABASE_URL          # Connect to database
python scripts/fetch_fixtures.py  # Fetch match data

# Monitoring
railway logs --follow       # View live logs
curl /health                # Check service status
```

This guide provides everything needed to deploy ScoreSure from development to production! 🚀
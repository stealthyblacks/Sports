# ScoreSure Automation & Scheduling

This document outlines various options for automating data fetching and predictions in the ScoreSure application.

## Scripts Overview

### fetch_fixtures.py
```bash
cd backend
python scripts/fetch_fixtures.py
```
- Fetches latest fixtures from external APIs
- Stores match data in PostgreSQL database
- Async implementation for better performance

### run_predictions.py
```bash
cd backend
python scripts/run_predictions.py
```
- Generates predictions for scheduled matches
- Uses ELO-based algorithm with home advantage
- Outputs prediction results to console

## Automation Options

### 1. Vercel Cron Jobs (Recommended for Frontend)

Configure in `vercel.json`:
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

**Benefits:**
- Integrated with your Vercel deployment
- Free for hobby projects
- Automatic retries and monitoring
- No external dependencies

**Setup:**
1. Add `vercel.json` to your frontend root
2. Deploy to Vercel
3. Cron will automatically trigger daily at 6:00 AM UTC

### 2. External Cron Services

#### cron-job.org (Free Option)
- Website: https://cron-job.org
- Create account and add job
- Target URL: `https://your-backend.com/api/fetchMatches`
- Schedule: `0 6 * * *` (6:00 AM daily)
- Method: POST

**Benefits:**
- Free up to 25 jobs
- Web interface
- Email notifications on failure
- Multiple timezone support

#### EasyCron (Paid Option)
- Website: https://www.easycron.com
- More reliable than free services
- Better monitoring and analytics
- API for dynamic job management

### 3. Linux VPS Cron (Production)

Edit crontab:
```bash
crontab -e
```

Add these lines:
```bash
# Fetch fixtures daily at 6:00 AM
0 6 * * * curl -s -X POST https://your-backend.com/api/fetchMatches >/tmp/fetch_matches.log 2>&1

# Run predictions daily at 2:05 AM
5 2 * * * /usr/bin/python3 /srv/predictor/backend/scripts/run_predictions.py >> /srv/predictor/logs/predictions.log 2>&1

# Clean old logs weekly
0 0 * * 0 find /srv/predictor/logs -name "*.log" -mtime +7 -delete
```

**Directory Structure for VPS:**
```
/srv/predictor/
├── backend/
│   ├── scripts/
│   │   ├── fetch_fixtures.py
│   │   └── run_predictions.py
│   └── app/
├── logs/
│   ├── predictions.log
│   └── fetch_matches.log
└── venv/
```

**Setup Commands:**
```bash
# Create directories
sudo mkdir -p /srv/predictor/logs
sudo chown $USER:$USER /srv/predictor

# Install Python dependencies
cd /srv/predictor
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Set environment variables
echo "DATABASE_URL=postgresql://user:pass@localhost:5432/predictor" >> .env
echo "FOOTBALL_API_KEY=your_key_here" >> .env
```

### 4. Docker-based Scheduling

Create `docker-compose.scheduler.yml`:
```yaml
version: '3.8'
services:
  scheduler:
    image: mcuadros/ofelia:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./ofelia.ini:/etc/ofelia/config.ini
    depends_on:
      - backend

  backend:
    # your existing backend service
```

Create `ofelia.ini`:
```ini
[job-exec "fetch-fixtures"]
schedule = @daily
container = predictor_backend
command = python scripts/fetch_fixtures.py

[job-exec "run-predictions"]
schedule = 0 2 * * *
container = predictor_backend
command = python scripts/run_predictions.py
```

### 5. GitHub Actions (CI/CD Integration)

Create `.github/workflows/daily-update.yml`:
```yaml
name: Daily Data Update
on:
  schedule:
    - cron: '0 6 * * *'  # 6:00 AM UTC daily
  workflow_dispatch:  # Manual trigger

jobs:
  update-data:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Data Fetch
        run: |
          curl -X POST ${{ secrets.BACKEND_URL }}/api/fetchMatches
```

## Environment Variables for Automation

Ensure these are set in your deployment environment:

```bash
# Required
DATABASE_URL=postgresql://user:pass@host:5432/predictor
FOOTBALL_API_KEY=your_football_api_key

# Optional
ODDS_API_KEY=your_odds_api_key
FOOTBALL_BASE=https://api-football-v1.p.rapidapi.com/v3
LOG_LEVEL=INFO
```

## Monitoring & Alerting

### Health Check Endpoint
Add to your backend routes:
```python
@router.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

### Log Monitoring
```bash
# Monitor prediction logs
tail -f /srv/predictor/logs/predictions.log

# Check for errors
grep -i error /srv/predictor/logs/*.log
```

### Uptime Monitoring
Use services like:
- UptimeRobot (free)
- Pingdom
- StatusCake

Monitor these endpoints:
- `https://your-backend.com/api/health`
- `https://your-frontend.com/api/proxy?path=today`

## Error Handling

### Script Error Recovery
```python
# Add to scripts for better error handling
import sys
import traceback

try:
    # your script logic
    pass
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)  # Non-zero exit for cron failure detection
```

### Database Connection Issues
```python
# Add retry logic
import time
from sqlalchemy.exc import OperationalError

def get_db_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            return SessionLocal()
        except OperationalError:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            raise
```

## Best Practices

1. **Timing**: Space out different jobs to avoid resource conflicts
2. **Logging**: Always log to files for debugging
3. **Monitoring**: Set up alerts for job failures
4. **Backup**: Keep logs for at least 7 days
5. **Testing**: Test scripts manually before scheduling
6. **Environment**: Use consistent environments across dev/prod
7. **Secrets**: Never hardcode API keys in scripts

## Quick Setup Commands

### Local Development
```bash
# Test scripts manually
cd backend
python scripts/fetch_fixtures.py
python scripts/run_predictions.py
```

### Production Deployment
```bash
# Set up systemd timer (alternative to cron)
sudo systemctl enable --now predictor-fetch.timer
sudo systemctl enable --now predictor-predict.timer
```

Choose the automation method that best fits your infrastructure and requirements!
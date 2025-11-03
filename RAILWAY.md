# ScoreSure Railway Deployment Guide

## Quick Railway Setup

### 1. Connect GitHub Repository
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `predictor` repository
5. Select `backend` folder as root directory

### 2. Environment Variables
Add these in Railway dashboard:
```bash
DATABASE_URL=postgresql://postgres:password@host:5432/railway
FOOTBALL_API_KEY=your_api_key_here
ODDS_API_KEY=your_odds_key_here
PORT=8000
```

### 3. Database Setup
1. Click "Add Service" → "Database" → "PostgreSQL"
2. Railway automatically provides `DATABASE_URL`
3. Your backend will connect automatically

### 4. Custom Domain (Optional)
1. Go to Settings → Domains
2. Add your custom domain
3. Configure DNS settings

## GitHub Actions Integration

### Option 1: Automatic Deployment
Railway automatically deploys when you push to `main` branch. No additional setup needed!

### Option 2: Manual Deployment with Actions
Use the provided `.github/workflows/deploy-railway.yml`:

**Required Secrets:**
- `RAILWAY_TOKEN`: Get from Railway Account Settings
- `DATABASE_URL`: Optional, Railway provides this
- `FOOTBALL_API_KEY`: Your football API key
- `ODDS_API_KEY`: Your odds API key

**Setup Steps:**
1. Go to GitHub repo → Settings → Secrets
2. Add the secrets above
3. Push to main branch to trigger deployment

### Railway CLI Commands
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link existing project
railway link

# Deploy manually
railway deploy

# View logs
railway logs

# Open in browser
railway open
```

## Railway Configuration Files

### railway.json (Optional)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/today",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Procfile (Alternative)
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Database Management

### Connect to Railway PostgreSQL
```bash
# Using Railway CLI
railway run psql $DATABASE_URL

# Or get connection details
railway variables
```

### Run Migrations
```bash
# Connect to Railway database
railway run python -c "
from app.db import engine, Base
from app.models import Match, Odds
Base.metadata.create_all(bind=engine)
print('Tables created successfully!')
"
```

### Backup Database
```bash
# Export data
railway run pg_dump $DATABASE_URL > backup.sql

# Import data
railway run psql $DATABASE_URL < backup.sql
```

## Monitoring & Debugging

### View Application Logs
```bash
# Real-time logs
railway logs --follow

# Recent logs
railway logs --tail 100
```

### Health Checks
Railway automatically monitors your application health:
- HTTP endpoint: `/api/today`
- Response time monitoring
- Automatic restarts on failure

### Performance Metrics
Check Railway dashboard for:
- CPU usage
- Memory consumption
- Request/response times
- Error rates

## Scaling & Optimization

### Vertical Scaling
1. Go to Settings → Resources
2. Adjust CPU and Memory limits
3. Changes apply immediately

### Environment Management
```bash
# Set environment variables
railway variables set FOOTBALL_API_KEY=new_key

# View all variables
railway variables

# Delete variable
railway variables delete OLD_VARIABLE
```

### Cost Optimization
- **Starter Plan**: $5/month usage included
- **Pro Plan**: Pay-as-you-go pricing
- **Resource Limits**: Set memory/CPU limits to control costs
- **Sleep Mode**: Applications sleep when inactive (Starter plan)

## Custom Deployment Scripts

### Pre-deployment Hook
```bash
#!/bin/bash
# run-before-deploy.sh
echo "Running pre-deployment tasks..."
cd backend
python -c "from app.db import engine; print(f'Database connection: {engine.url}')"
```

### Post-deployment Hook
```bash
#!/bin/bash
# run-after-deploy.sh
echo "Running post-deployment tasks..."
curl -X POST $RAILWAY_PUBLIC_DOMAIN/api/fetchMatches
echo "Initial data fetch completed"
```

## Troubleshooting

### Common Issues

**Build Failures:**
```bash
# Check build logs
railway logs --deployment

# Rebuild from scratch
railway redeploy
```

**Database Connection Issues:**
```bash
# Verify DATABASE_URL
railway variables | grep DATABASE_URL

# Test connection
railway run python -c "
import os
from sqlalchemy import create_engine
engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    print('Database connection successful!')
"
```

**Application Not Starting:**
```bash
# Check startup logs
railway logs --tail 50

# Verify start command
railway variables | grep PORT
```

### Debug Mode
Add debug environment variable:
```bash
railway variables set DEBUG=true
```

Then update your app:
```python
import os
if os.getenv("DEBUG"):
    import logging
    logging.basicConfig(level=logging.DEBUG)
```

## Production Checklist

- [ ] Environment variables configured
- [ ] Database connected and tables created
- [ ] Health check endpoint working
- [ ] Custom domain configured (if needed)
- [ ] Monitoring alerts set up
- [ ] Backup strategy implemented
- [ ] Resource limits appropriate
- [ ] Security headers configured

Railway makes deployment simple while providing enterprise-grade infrastructure!
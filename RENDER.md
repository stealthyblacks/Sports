# ScoreSure Render Deployment Guide

## Quick Render Setup

### 1. Connect GitHub Repository
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select your `predictor` repository
5. Configure build settings

### 2. Build Configuration
**Root Directory:** `backend`
**Build Command:** `pip install -r requirements.txt`
**Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@host:5432/database
FOOTBALL_API_KEY=your_api_key_here
ODDS_API_KEY=your_odds_key_here
PYTHON_VERSION=3.11
```

### 4. Database Setup
1. Create new PostgreSQL database in Render
2. Copy the "Internal Database URL"
3. Add as `DATABASE_URL` environment variable
4. Tables will be created automatically by SQLAlchemy

## GitHub Actions Integration

### Automatic Deployment
Render automatically deploys when you push to your main branch.

### Manual Deployment with Actions
Use the provided `.github/workflows/deploy-render.yml`:

**Required Secrets:**
- `RENDER_SERVICE_ID`: Get from your service URL
- `RENDER_API_KEY`: Create in Account Settings
- Other environment variables

**Setup Steps:**
1. Go to GitHub repo → Settings → Secrets and Variables → Actions
2. Add the required secrets
3. Push to main branch to trigger deployment

## Render Configuration

### render.yaml (Infrastructure as Code)
```yaml
services:
  - type: web
    name: scoresure-backend
    env: python
    region: oregon
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: FOOTBALL_API_KEY
        fromDatabase:
          name: scoresure-secrets
          property: football_api_key
      - key: DATABASE_URL
        fromDatabase:
          name: scoresure-db
          property: connectionString

databases:
  - name: scoresure-db
    databaseName: scoresure
    user: scoresure_user
    region: oregon
    plan: starter
```

### Deploy from Dashboard
1. **Name:** scoresure-backend
2. **Region:** Choose closest to your users
3. **Branch:** main
4. **Root Directory:** backend
5. **Runtime:** Python 3.11
6. **Build Command:** `pip install -r requirements.txt`
7. **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Database Management

### Connect to Render PostgreSQL
Get connection details from your database dashboard:
```bash
# Using psql
psql postgresql://user:pass@host:5432/database

# Using Python
python -c "
import os
from sqlalchemy import create_engine
engine = create_engine(os.getenv('DATABASE_URL'))
print('Connected to:', engine.url)
"
```

### Initialize Tables
```bash
# From your local machine
python -c "
from app.db import engine, Base
from app.models import Match, Odds
Base.metadata.create_all(bind=engine)
print('Tables created successfully!')
"
```

### Database Migrations
```bash
# Install alembic locally
pip install alembic

# Initialize alembic
cd backend
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial tables"

# Apply migration
alembic upgrade head
```

## Monitoring & Debugging

### View Logs
1. Go to your service dashboard
2. Click "Logs" tab
3. Filter by log level (Info, Warning, Error)

### Health Checks
Render automatically monitors:
- HTTP response codes
- Response times
- Application availability

### Performance Monitoring
Available metrics:
- CPU usage
- Memory consumption
- Request volume
- Response times

## Scaling & Configuration

### Service Plans
- **Starter:** $7/month, 0.5 CPU, 512MB RAM
- **Standard:** $25/month, 1 CPU, 2GB RAM
- **Pro:** $85/month, 2 CPU, 4GB RAM

### Auto-scaling
```yaml
# In render.yaml
autoDeploy: true
scaling:
  minInstances: 1
  maxInstances: 3
  targetCPU: 70
  targetMemory: 80
```

### Custom Domains
1. Go to Settings → Custom Domains
2. Add your domain name
3. Configure DNS records:
   ```
   CNAME: your-domain.com → app-name.onrender.com
   ```

## Environment Management

### Development Environment
```bash
# Local development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/predictor
FOOTBALL_API_KEY=dev_key
DEBUG=true
```

### Production Environment
```bash
# Render production
DATABASE_URL=postgresql://user:pass@render-host:5432/database
FOOTBALL_API_KEY=prod_key
DEBUG=false
ENVIRONMENT=production
```

## Deployment Strategies

### Blue-Green Deployment
1. Create new service with updated code
2. Test thoroughly
3. Switch traffic using load balancer
4. Decommission old service

### Rolling Updates
```yaml
# render.yaml
deploymentStrategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
```

## Security Best Practices

### Environment Variables
- Never commit secrets to Git
- Use Render's environment variable UI
- Rotate API keys regularly

### Network Security
```yaml
# render.yaml
networkPolicy:
  ingress:
    - from: []
      ports:
        - protocol: TCP
          port: 8000
```

### HTTPS Configuration
Render provides free SSL certificates:
- Automatic certificate generation
- Auto-renewal
- Force HTTPS redirects

## Backup & Disaster Recovery

### Database Backups
```bash
# Manual backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Automated backup script
#!/bin/bash
BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S).sql"
pg_dump $DATABASE_URL > $BACKUP_NAME
echo "Backup created: $BACKUP_NAME"
```

### Application Backups
- Code is backed up in Git
- Environment variables backed up manually
- Database backups stored externally

## Cost Optimization

### Free Tier Limitations
- 750 hours/month free compute
- Spins down after 15 minutes of inactivity
- Limited to 1 service

### Optimization Tips
1. **Right-size your service plan**
2. **Use efficient database queries**
3. **Implement caching**
4. **Monitor resource usage**

## Troubleshooting

### Common Build Issues
```bash
# Python version mismatch
RuntimeError: Python version not supported

# Solution: Set PYTHON_VERSION=3.11 in environment
```

### Database Connection Errors
```bash
# Connection refused
sqlalchemy.exc.OperationalError: connection refused

# Check:
# 1. DATABASE_URL format
# 2. Database service status
# 3. Network connectivity
```

### Application Startup Issues
```bash
# Port binding error
OSError: [Errno 98] Address already in use

# Solution: Use $PORT environment variable
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Memory Issues
```bash
# Out of memory
MemoryError: Unable to allocate memory

# Solutions:
# 1. Upgrade service plan
# 2. Optimize memory usage
# 3. Implement connection pooling
```

## Production Checklist

- [ ] Service configured with correct build/start commands
- [ ] Environment variables set
- [ ] Database created and connected
- [ ] Custom domain configured (if needed)
- [ ] SSL certificate active
- [ ] Health checks passing
- [ ] Logs monitoring set up
- [ ] Backup strategy implemented
- [ ] Performance monitoring active

Render provides a robust platform with excellent GitHub integration and automatic deployments!
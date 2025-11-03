# ScoreSure Deployment Guide

This guide covers deploying the ScoreSure application to various cloud platforms.

## GitHub Actions CI/CD

The `.github/workflows/ci.yml` provides basic continuous integration:

- **Triggers**: Runs on every push to any branch
- **Python Setup**: Uses Python 3.11
- **Dependency Install**: Installs backend requirements
- **Testing**: Placeholder for future tests

### Extending the CI Pipeline

Add testing step:
```yaml
- name: Run tests
  run: |
    cd backend
    python -m pytest tests/
```

Add linting:
```yaml
- name: Lint code
  run: |
    pip install flake8
    flake8 backend/app --max-line-length=88
```

## Backend Deployment Options

### 1. Railway (Recommended)

**Automatic GitHub Integration:**
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub account
3. Select your repository
4. Choose the `backend` folder as root
5. Railway auto-detects Python and uses your Dockerfile

**Environment Variables:**
```bash
DATABASE_URL=postgresql://postgres:password@host:5432/railway
FOOTBALL_API_KEY=your_api_key
ODDS_API_KEY=your_odds_key
PORT=8000
```

**railway.json (optional):**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "backend/Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/today",
    "healthcheckTimeout": 100
  }
}
```

**Database Setup:**
1. Add PostgreSQL service in Railway
2. Connect to your backend service
3. Use the provided `DATABASE_URL`

### 2. Render

**GitHub Integration:**
1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Create new "Web Service"
4. Select your repository and `backend` folder

**Build Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Python Version**: 3.11

**Environment Variables:**
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
FOOTBALL_API_KEY=your_api_key
ODDS_API_KEY=your_odds_key
PYTHON_VERSION=3.11
```

**Database Setup:**
1. Create PostgreSQL instance in Render
2. Copy the internal connection string
3. Add to your web service environment

### 3. Heroku

**Deploy with Git:**
```bash
# Install Heroku CLI
heroku create scoresure-backend
heroku addons:create heroku-postgresql:mini
heroku config:set FOOTBALL_API_KEY=your_key
git push heroku main
```

**Procfile:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4. DigitalOcean App Platform

**app.yaml:**
```yaml
name: scoresure-backend
services:
- name: backend
  source_dir: backend
  github:
    repo: yourusername/predictor
    branch: main
  run_command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: FOOTBALL_API_KEY
    value: your_api_key
    type: SECRET

databases:
- name: predictor-db
  engine: PG
  version: "15"
```

## Frontend Deployment (Vercel)

**Automatic GitHub Integration:**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Select `frontend` as root directory
4. Vercel auto-detects Next.js

**Environment Variables:**
```bash
BACKEND_URL=https://your-backend.railway.app
NEXT_PUBLIC_API_URL=https://your-frontend.vercel.app/api/proxy
```

**vercel.json:**
```json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/.next",
  "framework": "nextjs",
  "crons": [
    {
      "path": "/api/proxy?path=fetchMatches",
      "schedule": "0 6 * * *"
    }
  ]
}
```

## Advanced CI/CD Workflows

### Multi-Environment Deployment

```yaml
name: Deploy
on:
  push:
    branches: [main, staging]

jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Staging
        run: |
          # Deploy to staging environment
          echo "Deploying to staging..."

  deploy-production:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Production
        run: |
          # Deploy to production environment
          echo "Deploying to production..."
```

### Database Migrations

```yaml
- name: Run Database Migrations
  run: |
    cd backend
    python -c "
    from app.db import engine, Base
    Base.metadata.create_all(bind=engine)
    print('Database tables created successfully!')
    "
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Security Scanning

```yaml
- name: Security Scan
  run: |
    pip install safety bandit
    safety check -r backend/requirements.txt
    bandit -r backend/app/
```

## Environment Management

### Development
```bash
# Local development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/predictor
FOOTBALL_API_KEY=dev_key
```

### Staging
```bash
# Staging environment
DATABASE_URL=postgresql://user:pass@staging-db:5432/predictor_staging
FOOTBALL_API_KEY=staging_key
```

### Production
```bash
# Production environment
DATABASE_URL=postgresql://user:pass@prod-db:5432/predictor_prod
FOOTBALL_API_KEY=prod_key
```

## Monitoring & Logging

### Health Checks
Add to your backend routes:
```python
@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### Application Monitoring
- **Railway**: Built-in monitoring dashboard
- **Render**: Automatic health checks
- **Heroku**: Heroku Metrics
- **External**: DataDog, New Relic, Sentry

### Log Aggregation
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

## Cost Optimization

### Free Tiers
- **Railway**: $5/month free usage
- **Render**: Free tier with limitations
- **Heroku**: Free tier discontinued
- **Vercel**: Generous free tier for frontend

### Resource Scaling
- Start with smallest instances
- Scale based on actual usage
- Use connection pooling for databases
- Implement caching where appropriate

## Quick Deployment Commands

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway deploy
```

### Render
```bash
# Deploy via Git
git push origin main
# Render automatically deploys
```

### Manual Docker Deploy
```bash
# Build and push to registry
docker build -t scoresure-backend ./backend
docker tag scoresure-backend registry.com/scoresure-backend
docker push registry.com/scoresure-backend
```

Choose the deployment platform that best fits your needs and budget!
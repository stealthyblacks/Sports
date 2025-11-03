# Football Predictor

An AI-powered football match prediction application built with FastAPI backend and Next.js frontend.

## Features

- **AI-Powered Predictions**: Advanced algorithms analyze team form, head-to-head records, and historical data
- **Real-time Data**: Fetch live fixtures from external football APIs
- **Interactive UI**: Modern, responsive web interface built with Next.js and Tailwind CSS
- **Comprehensive Analytics**: Detailed match analysis including team form and confidence scores
- **RESTful API**: Well-documented FastAPI backend with automatic OpenAPI documentation

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Robust relational database
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pandas & NumPy**: Data manipulation and analysis
- **Scikit-learn**: Machine learning capabilities

### Frontend
- **Next.js**: React framework for production
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls

### Infrastructure
- **Docker**: Containerization for easy deployment
- **Docker Compose**: Multi-container orchestration

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone and setup**:
   ```bash
   cd predictor
   cp .env.example .env
   ```

2. **Configure environment**:
   - Edit `.env` file
   - Add your Football API key from [football-data.org](https://www.football-data.org/)

3. **Start all services**:
   ```bash
   cd infra
   docker-compose up -d
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example .env
# Edit .env with your database and API settings

# Run the server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### Database Setup
```bash
# Start PostgreSQL (if not using Docker)
# Create database and user as specified in .env

# The application will automatically create tables on startup
```

## API Endpoints

### Matches
- `GET /api/v1/matches` - Get upcoming matches
- `GET /api/v1/matches/{id}` - Get specific match details

### Predictions
- `GET /api/v1/predictions` - Get predictions for upcoming matches
- `GET /api/v1/predictions/{match_id}` - Get prediction for specific match
- `POST /api/v1/predictions/{match_id}` - Generate new prediction

### Teams
- `GET /api/v1/teams` - Get all teams
- `GET /api/v1/leagues` - Get available leagues

### Data Management
- `POST /api/v1/fetch-fixtures` - Fetch new fixtures from external API

## Data Sources

The application fetches data from:
- [Football-Data.org](https://www.football-data.org/) - Match fixtures and results
- Internal prediction algorithms based on:
  - Team recent form (last 5 matches)
  - Head-to-head records
  - Goals scored/conceded averages
  - Home advantage factors

## Prediction Algorithm

The current model uses a combination of:

1. **Team Form Analysis**:
   - Points per game in last 5 matches
   - Goals for/against ratios
   - Win/draw/loss streaks

2. **Head-to-Head Records**:
   - Historical match results between teams
   - Weighted by recency

3. **Home Advantage**:
   - Statistical home field advantage
   - League-specific adjustments

4. **Confidence Scoring**:
   - Based on data availability
   - Historical prediction accuracy

## Scripts

### Backend Scripts
```bash
# Fetch latest fixtures
python backend/scripts/fetch_fixtures.py

# Generate predictions for upcoming matches
python backend/scripts/run_predictions.py
```

## Project Structure

```
predictor/
├─ frontend/                # Next.js + Tailwind site
│  ├─ package.json
│  ├─ tailwind.config.js
│  ├─ postcss.config.js
│  ├─ next.config.js
│  ├─ pages/
│  │  ├─ index.js
│  │  ├─ api/
│  │  │  └─ proxy.js
│  │  └─ match/[id].js
│  ├─ public/
│  └─ components/
│     └─ Header.js
├─ backend/                 # FastAPI service
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ fetcher.py
│  │  ├─ predictions.py
│  │  ├─ db.py
│  │  ├─ models.py
│  │  └─ routes.py
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ scripts/
│     ├─ fetch_fixtures.py
│     └─ run_predictions.py
├─ infra/
│  ├─ docker-compose.yml
│  └─ postgres-init.sql
├─ .env.example
└─ README.md
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

- `DATABASE_URL`: PostgreSQL connection string
- `FOOTBALL_API_KEY`: API key from football-data.org
- `PORT`: Backend server port (default: 8000)
- `BACKEND_URL`: Backend URL for frontend proxy

### Database Configuration

The application uses PostgreSQL with the following default settings:
- Database: `predictor_db`
- User: `predictor`
- Password: `password`
- Port: `5432`

## Development

### Adding New Features

1. **Backend**: Add new routes in `backend/app/routes.py`
2. **Frontend**: Create new pages in `frontend/pages/`
3. **Models**: Update database models in `backend/app/models.py`
4. **Predictions**: Enhance algorithms in `backend/app/predictions.py`

### Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

### Production Deployment

1. **Update environment variables** for production
2. **Build and deploy with Docker**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Environment-Specific Configurations

- Development: Use Docker Compose with hot reloading
- Production: Build optimized images and use environment-specific configs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check the API documentation at `/docs`
- Review the database schema in `models.py`
- Check logs in Docker containers

## Future Enhancements

- [ ] Advanced ML models (XGBoost, Neural Networks)
- [ ] Real-time match tracking
- [ ] User authentication and favorites
- [ ] Betting odds integration
- [ ] Mobile app
- [ ] Historical prediction accuracy tracking
- [ ] More leagues and competitions
- [ ] Player-level statistics
- [ ] Weather and pitch condition factors
import asyncio
from app.fetcher import fetch_fixtures

if __name__ == "__main__":
    asyncio.run(fetch_fixtures())
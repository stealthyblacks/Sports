from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, Text
from sqlalchemy.sql import func
from db import Base

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String, unique=True, index=True)  # id from API
    league = Column(String)
    home = Column(String)
    away = Column(String)
    kickoff = Column(DateTime)
    status = Column(String)
    provider_payload = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

class Odds(Base):
    __tablename__ = "odds"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, index=True)
    provider = Column(String)
    market = Column(String)
    selection = Column(String)
    odd = Column(Float)
    retrieved_at = Column(DateTime, server_default=func.now())
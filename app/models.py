from sqlalchemy import Column, String, Float, DateTime, Integer, JSON
from app.core.database import Base
from datetime import datetime


class PollingJobConfig(Base):
    __tablename__ = "polling_job_configs"
    
    job_id = Column(String, primary_key=True, index=True)
    symbols = Column(JSON, nullable=False)
    interval = Column(Integer, nullable=False)
    provider = Column(String, nullable=False)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class RawMarketData(Base):
    __tablename__ = "raw_market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    provider = Column(String)

class SymbolAverage(Base):
    __tablename__ = "symbol_averages"
    
    symbol = Column(String, primary_key=True)
    average = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

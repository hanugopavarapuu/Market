from fastapi import APIRouter, HTTPException, Query, Depends, Body
from sqlalchemy.orm import Session
from app.services.provider_yfinance import YahooFinanceProvider
from app.core.database import get_db
from app.models import RawMarketData, PollingJobConfig
from datetime import datetime
from typing import List, Dict, Any, Optional
import yfinance as yf
import uuid
import logging
from app.services.kafka_producer import KafkaPriceProducer

router = APIRouter(prefix="/prices")
logger = logging.getLogger(__name__)

# Initialize services
yfinance_provider = YahooFinanceProvider()
kafka_producer = KafkaPriceProducer()

@router.get("/latest")
async def get_latest_price(symbol: str, db: Session = Depends(get_db)):
    """
    Get the latest price for a symbol.
    
    Args:
        symbol: The stock symbol to fetch price for
        db: Database session
        
    Returns:
        Dict containing:
            - symbol: str
            - price: float
            - timestamp: str (ISO format)
            - provider: str
    """
    try:
        # Get price from provider
        price_data = yfinance_provider.get_latest_price(symbol)
        
        # Convert datetime to ISO format string
        response_data = {
            "symbol": price_data["symbol"],
            "price": price_data["price"],
            "timestamp": price_data["timestamp"].isoformat(),
            "provider": price_data["provider"]
        }
        
        # Store raw market data
        raw_data = RawMarketData(
            symbol=price_data["symbol"],
            price=price_data["price"],
            timestamp=price_data["timestamp"],  # Ensure this is a datetime object
            provider=price_data["provider"]
        )
        db.add(raw_data)
        db.commit()
        
        # Publish to Kafka
        kafka_producer.publish_price_update(response_data)
        
        # Return response
        return response_data
        
    except Exception as e:
        logger.error(f"Error getting latest price: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/poll")
async def create_polling_job(
    request: dict = Body(...),
    db: Session = Depends(get_db)
):
    """
    Create a new polling job for multiple symbols.
    
    Args:
        request: Dict containing:
            - symbols: List of stock symbols to poll
            - interval: Polling interval in seconds
        db: Database session
        
    Returns:
        Dict containing job details
    """
    try:
        symbols = request.get("symbols", [])
        interval = request.get("interval")
        
        if not symbols or not interval:
            raise HTTPException(status_code=400, detail="Both symbols and interval are required")
            
        # Generate unique job ID
        job_id = f"poll_{uuid.uuid4().hex[:8]}"
        
        # Create job config
        job_config = PollingJobConfig(
            job_id=job_id,
            symbols=symbols,
            interval=interval,
            provider="yfinance",
            status="accepted"
        )
        
        # Save to database
        db.add(job_config)
        db.commit()
        
        # Return response
        return {
            "job_id": job_id,
            "status": "accepted",
            "config": {
                "symbols": symbols,
                "interval": interval
            }
        }
        
    except Exception as e:
        logger.error(f"Error creating polling job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

class YahooFinanceProvider:
    async def get_latest_price(self, symbol: str):
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if data.empty:
            raise ValueError(f"No data found for symbol: {symbol}")
        latest_price = data['Close'].iloc[-1]
        timestamp = datetime.now()
        return {
            "symbol": symbol,
            "price": float(latest_price),
            "timestamp": timestamp.isoformat(),
            "provider": "yfinance"
        }

class AlphaVantageProvider:
    async def get_latest_price(self, symbol: str):
        # Implement your Alpha Vantage API logic here
        pass

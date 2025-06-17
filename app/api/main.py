from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models import PollingJobConfig, RawMarketData, SymbolAverage
from app.core.config import settings
from app.api.routes import prices
import asyncio
from app.services.kafka_consumer import KafkaPriceConsumer
import threading
from sqlalchemy import text

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
def init_db():
    # Drop existing tables with CASCADE
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.commit()
    
    # Create new tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

# Initialize database
init_db()

# Include routers
app.include_router(prices.router, prefix=settings.API_V1_STR)

def run_kafka_consumer():
    consumer = KafkaPriceConsumer()
    consumer.start_consuming()

@app.on_event("startup")
async def startup_event():
    print("Starting Market Data Service...")
    # Start Kafka consumer in a separate thread
    consumer_thread = threading.Thread(target=run_kafka_consumer, daemon=True)
    consumer_thread.start()
    print("Kafka consumer started...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down Market Data Service...")

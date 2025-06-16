from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models import PollingJobConfig, RawMarketData
from app.core.config import settings
from app.api.routes import prices

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
Base.metadata.drop_all(bind=engine)  # Drop existing tables
Base.metadata.create_all(bind=engine)  # Create new tables

# Include routers
app.include_router(prices.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    print("Starting Market Data Service...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down Market Data Service...")

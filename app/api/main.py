from fastapi import FastAPI
from app.api.routes import prices

app = FastAPI(title="Market Data Service", version="0.1.0")

app.include_router(prices.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

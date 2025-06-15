from fastapi import APIRouter, Query
from app.schemas.price import PriceResponse, PollRequest, PollResponse
from app.services.price_service import get_latest_price, poll_prices

router = APIRouter()

@router.get("/prices/latest", response_model=PriceResponse)
def get_price(symbol: str = Query(...), provider: str = "yfinance"):
    return get_latest_price(symbol, provider)

@router.post("/prices/poll", response_model=PollResponse, status_code=202)
def poll(request: PollRequest):
    return poll_prices(request)

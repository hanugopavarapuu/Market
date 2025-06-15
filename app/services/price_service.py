from app.services.market_provider import fetch_price_yfinance
from app.schemas.price import PriceResponse, PollRequest, PollResponse
import uuid

def get_latest_price(symbol: str, provider: str = "yfinance") -> PriceResponse:
    if provider == "yfinance":
        data = fetch_price_yfinance(symbol)
    else:
        raise ValueError(f"Provider {provider} not supported yet")
    return PriceResponse(**data)

def poll_prices(request: PollRequest) -> PollResponse:
    job_id = f"poll_{uuid.uuid4().hex[:8]}"
    # Placeholder: Normally you'd store this in a DB
    return PollResponse(
        job_id=job_id,
        status="accepted",
        config=request
    )

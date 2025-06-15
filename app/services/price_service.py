import uuid
from app.schemas.price import PriceResponse, PollRequest, PollResponse
from app.services.market_provider import fetch_price_yfinance
from app.core.kafka_producer import send_polling_job

def get_latest_price(symbol: str, provider: str = "yfinance") -> PriceResponse:
    if provider == "yfinance":
        data = fetch_price_yfinance(symbol)
    else:
        raise ValueError(f"Provider {provider} not supported yet")
    return PriceResponse(**data)

def poll_prices(request: PollRequest) -> PollResponse:
    job_id = f"poll_{uuid.uuid4().hex[:8]}"
    
    job = {
        "job_id": job_id,
        "symbols": request.symbols,
        "interval": request.interval,
        "provider": request.provider
    }

    # Send polling job to Kafka
    send_polling_job(job)

    return PollResponse(
        job_id=job_id,
        status="accepted",
        config=request
    )

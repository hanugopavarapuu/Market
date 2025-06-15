import yfinance as yf
from datetime import datetime

def fetch_price_yfinance(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    price = ticker.info.get("regularMarketPrice")
    return {
        "symbol": symbol,
        "price": price,
        "timestamp": datetime.utcnow().isoformat(),
        "provider": "yfinance"
    }

import aiohttp
from datetime import datetime
from typing import Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AlphaVantageProvider:
    def __init__(self):
        self.api_key = settings.ALPHA_VANTAGE_API_KEY
        if not self.api_key:
            raise ValueError("Alpha Vantage API key not found in environment variables")
        
        self.base_url = "https://www.alphavantage.co/query"
    
    async def get_latest_price(self, symbol: str) -> Dict[str, Any]:
        try:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        raise Exception(f"Alpha Vantage API returned status code {response.status}")
                    
                    data = await response.json()
                    
                    if "Error Message" in data:
                        raise Exception(data["Error Message"])
                    
                    if "Global Quote" not in data or not data["Global Quote"]:
                        raise ValueError(f"No data found for symbol: {symbol}")
                    
                    quote = data["Global Quote"]
                    price = float(quote["05. price"])
                    timestamp = datetime.now()
                    
                    price_data = {
                        "symbol": symbol,
                        "price": price,
                        "timestamp": timestamp.isoformat(),
                        "provider": "alpha_vantage"
                    }

                    raw_data = RawMarketData(
                        symbol=symbol,
                        price=price,
                        timestamp=datetime.fromisoformat(data['timestamp']),
                        provider=data.get('source', 'yfinance')
                    )
                    self.db.add(raw_data)
                    self.db.commit()

                    if average is not None:
                        # Upsert to symbol_averages
                        self.update_symbol_average(symbol, average)

                    return price_data
        except Exception as e:
            raise Exception(f"Error fetching data from Alpha Vantage: {str(e)}")

    def calculate_moving_average(self, symbol: str) -> float:
        if len(self.price_history[symbol]) < 5:
            logger.debug(f"Not enough data points for {symbol}. Current points: {len(self.price_history[symbol])}")
            return None

    def update_symbol_average(self, symbol: str, average: float) -> None:
        if len(self.price_history[symbol]) < 5:
            logger.debug(f"Not enough data points for {symbol}. Current points: {len(self.price_history[symbol])}")
            return None

        if symbol_avg:
            logger.info(f"Updated existing moving average for {symbol}: {average}")
        else:
            logger.info(f"Created new moving average for {symbol}: {average}")

        logger.info(f"Committed moving average for {symbol}: {average}") 
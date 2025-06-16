import yfinance as yf
import logging
from datetime import datetime
from typing import Dict, Any
from .provider_interface import PriceProvider

logger = logging.getLogger(__name__)

class YahooFinanceProvider(PriceProvider):
    def __init__(self):
        self.provider_name = "yfinance"
    
    def get_provider_name(self) -> str:
        return self.provider_name
    
    def get_latest_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get the latest price for a given symbol using Yahoo Finance.
        
        Args:
            symbol: The stock symbol to fetch price for
            
        Returns:
            Dict containing price data with the following fields:
                - symbol: str
                - price: float
                - timestamp: datetime
                - provider: str
                - raw_response_id: str
                
        Raises:
            Exception: If price cannot be fetched
        """
        try:
            logger.info(f"Fetching latest price for {symbol} from Yahoo Finance")
            
            # Validate symbol
            if not symbol or not isinstance(symbol, str):
                raise ValueError("Invalid symbol provided")
            
            # Get ticker data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d')
            
            if data.empty:
                logger.error(f"No price data found for symbol: {symbol}")
                raise Exception(f"No price data found for symbol: {symbol}")
            
            # Get the latest price
            latest_price = data['Close'].iloc[-1]
            timestamp = datetime.utcnow()
            
            logger.info(f"Successfully fetched price for {symbol}: {latest_price}")
            
            return {
                "symbol": symbol,
                "price": float(latest_price),
                "timestamp": timestamp,
                "provider": self.provider_name,
                "raw_response_id": f"yf_{symbol}_{timestamp.strftime('%Y%m%d%H%M%S')}"
            }
            
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {str(e)}")
            raise Exception(f"Failed to fetch price for {symbol}: {str(e)}") 
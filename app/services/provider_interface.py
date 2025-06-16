from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional

class PriceProvider(ABC):
    """Base class for all price providers."""
    
    @abstractmethod
    def get_latest_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get the latest price for a given symbol.
        
        Args:
            symbol: The stock symbol to fetch price for
            
        Returns:
            Dict containing:
                - symbol: str
                - price: float
                - timestamp: datetime
                - provider: str
                - raw_response_id: str (optional)
                
        Raises:
            Exception: If price cannot be fetched
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of this provider."""
        pass 
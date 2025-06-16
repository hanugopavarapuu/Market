from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class MarketDataProvider(ABC):
    @abstractmethod
    async def get_latest_price(self, symbol: str) -> Optional[dict]:
        pass

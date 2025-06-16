# app/services/provider_yfinance.py

import yfinance as yf
from datetime import datetime
import asyncio

class YahooFinanceProvider:
    async def get_latest_price(self, symbol: str) -> dict:
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, lambda: yf.Ticker(symbol).history(period="1d"))

        if data.empty:
            raise ValueError(f"No data found for symbol {symbol}")

        last_row = data.tail(1).iloc[0]
        price = float(last_row['Close'])
        timestamp = last_row.name.to_pydatetime().isoformat() + "Z"

        return {
            "symbol": symbol,
            "price": price,
            "timestamp": timestamp,
            "provider": "yfinance"
        }

import ccxt
from app import config

class MarketData:
    def __init__(self):
        exchange_class = getattr(ccxt, config.EXCHANGE_ID)
        self.exchange = exchange_class({
            "enableRateLimit": True,
            "timeout": 20000,
            "options": {"defaultType": "spot"}
        })
        self.exchange.load_markets()

    def has_symbol(self, symbol: str) -> bool:
        return symbol in self.exchange.markets

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int):
        if not self.has_symbol(symbol):
            matches = [s for s in self.exchange.symbols if s.replace("/", "").upper() == symbol.replace("/", "").upper()]
            hint = ", ".join(matches[:8]) if matches else "no matching listed symbol"
            raise ValueError(f"{symbol} is not listed on {config.EXCHANGE_ID}; possible matches: {hint}")
        rows = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        import pandas as pd
        df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df = df.set_index("timestamp")
        return df.astype(float)

import os
from dotenv import load_dotenv

load_dotenv()

def csv_env(name, default):
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
EXCHANGE_ID = os.getenv("EXCHANGE_ID", "binance").strip().lower()
CRYPTO_WATCHLIST = csv_env("CRYPTO_WATCHLIST", "BTC/USDT,ETH/USDT")
GOLD_SYMBOL = os.getenv("GOLD_SYMBOL", "XAU/USDT").strip()
TIMEFRAMES = csv_env("TIMEFRAMES", "5m,15m,1h,4h")
PRIMARY_TIMEFRAME = os.getenv("PRIMARY_TIMEFRAME", "15m").strip()
SCAN_INTERVAL_SECONDS = int(os.getenv("SCAN_INTERVAL_SECONDS", "300"))
CANDLE_LIMIT = int(os.getenv("CANDLE_LIMIT", "250"))
MIN_SIGNAL_SCORE = int(os.getenv("MIN_SIGNAL_SCORE", "4"))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8000"))

def validate():
    if not BOT_TOKEN or "PASTE_" in BOT_TOKEN:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN in .env")
    if not CHAT_ID or "PASTE_" in CHAT_ID:
        raise RuntimeError("Set TELEGRAM_CHAT_ID in .env")
    if EXCHANGE_ID not in {"binance", "bybit", "okx"}:
        raise RuntimeError("EXCHANGE_ID must be binance, bybit, or okx")

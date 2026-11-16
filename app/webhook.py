import hmac
from fastapi import FastAPI, HTTPException, Request
from telegram import Bot
from app import config

app = FastAPI(title="Smart Trading TradingView Webhook")

@app.post("/tradingview")
async def tradingview(payload: dict, request: Request):
    supplied_secret = request.query_params.get("secret", "")
    if not config.WEBHOOK_SECRET or not hmac.compare_digest(supplied_secret, config.WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Unauthorized")
    text = (
        "📡 TRADINGVIEW ALERT\n"
        f"Symbol: {payload.get('symbol', 'unknown')}\n"
        f"Timeframe: {payload.get('timeframe', 'unknown')}\n"
        f"Event: {payload.get('event', 'alert')}\n"
        f"Price: {payload.get('price', 'n/a')}\n"
        f"Details: {payload.get('message', '')}"
    )
    bot = Bot(config.BOT_TOKEN)
    await bot.send_message(chat_id=config.CHAT_ID, text=text)
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.webhook:app", host=config.WEBHOOK_HOST, port=config.WEBHOOK_PORT)

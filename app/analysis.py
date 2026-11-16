import numpy as np
from app.indicators import add_indicators

def _confirmed_pivots(df, left=3, right=3):
    # A pivot at i is only used once `right` later candles have closed.
    highs, lows = [], []
    h, l = df["high"].to_numpy(), df["low"].to_numpy()
    for i in range(left, len(df) - right):
        if h[i] >= np.max(h[i-left:i+right+1]):
            highs.append((i, float(h[i])))
        if l[i] <= np.min(l[i-left:i+right+1]):
            lows.append((i, float(l[i])))
    return highs, lows

def analyze(df):
    x = add_indicators(df).dropna()
    if len(x) < 60:
        raise ValueError("Not enough candles to analyze (need at least 60 valid candles)")
    row, prev = x.iloc[-1], x.iloc[-2]
    price = float(row.close)
    atr = float(row.atr)
    if not np.isfinite(atr) or atr <= 0:
        atr = max(price * 0.001, 1e-8)

    score = 0
    reasons = []
    if row.ema9 > row.ema21:
        score += 1; reasons.append("EMA9 > EMA21")
    else:
        score -= 1; reasons.append("EMA9 < EMA21")
    if row.close > row.ema50:
        score += 1; reasons.append("Giá trên EMA50")
    else:
        score -= 1; reasons.append("Giá dưới EMA50")
    if row.macd_hist > 0:
        score += 1; reasons.append("MACD histogram dương")
    else:
        score -= 1; reasons.append("MACD histogram âm")
    if 52 <= row.rsi <= 68:
        score += 1; reasons.append("RSI ủng hộ đà tăng")
    elif 32 <= row.rsi <= 48:
        score -= 1; reasons.append("RSI ủng hộ đà giảm")
    elif row.rsi >= 70:
        reasons.append("RSI quá mua – tránh đuổi giá")
    elif row.rsi <= 30:
        reasons.append("RSI quá bán – chờ xác nhận")
    if row.volume_ratio >= 1.5:
        reasons.append(f"Volume cao {row.volume_ratio:.2f}x trung bình 20 nến")

    highs, lows = _confirmed_pivots(x)
    resistance = highs[-1][1] if highs else float(x.high.tail(30).max())
    support = lows[-1][1] if lows else float(x.low.tail(30).min())

    bos_up = price > resistance
    bos_down = price < support
    if bos_up:
        reasons.append("Đóng nến vượt pivot high đã xác nhận (BOS tăng)")
        score += 1
    elif bos_down:
        reasons.append("Đóng nến thủng pivot low đã xác nhận (BOS giảm)")
        score -= 1

    if score >= 3:
        bias = "BUY BIAS"
    elif score <= -3:
        bias = "SELL BIAS"
    else:
        bias = "SIDEWAY / CHỜ XÁC NHẬN"

    # Conditional levels, not guaranteed targets.
    if bias == "BUY BIAS":
        entry_low, entry_high = price - 0.25*atr, price + 0.10*atr
        sl = min(support, price - 1.2*atr)
        risk = max(price - sl, 0.8*atr)
        tp1, tp2 = price + risk, price + 2*risk
    elif bias == "SELL BIAS":
        entry_low, entry_high = price - 0.10*atr, price + 0.25*atr
        sl = max(resistance, price + 1.2*atr)
        risk = max(sl - price, 0.8*atr)
        tp1, tp2 = price - risk, price - 2*risk
    else:
        entry_low, entry_high = support, resistance
        sl = tp1 = tp2 = None

    # Three conditional forward paths for chart visualization.
    forecast = {
        "bull": [price + atr*0.5, price + atr*1.0, price + atr*1.5],
        "bear": [price - atr*0.5, price - atr*1.0, price - atr*1.5],
        "side": [price, price + atr*0.15, price - atr*0.10],
    }
    candle = x.iloc[-1]
    prev_candle = x.iloc[-2]
    bullish_engulf = (candle.close > candle.open and prev_candle.close < prev_candle.open
                      and candle.close >= prev_candle.open and candle.open <= prev_candle.close)
    bearish_engulf = (candle.close < candle.open and prev_candle.close > prev_candle.open
                      and candle.close <= prev_candle.open and candle.open >= prev_candle.close)
    patterns = []
    if bullish_engulf: patterns.append("Bullish Engulfing")
    if bearish_engulf: patterns.append("Bearish Engulfing")

    # Three-candle fair value gaps; only latest visible unfilled candidate is reported.
    fvg = None
    if len(x) >= 3:
        a, c = x.iloc[-3], x.iloc[-1]
        if c.low > a.high:
            fvg = ("Bullish FVG", float(a.high), float(c.low))
        elif c.high < a.low:
            fvg = ("Bearish FVG", float(c.high), float(a.low))

    return {
        "price": price, "atr": atr, "rsi": float(row.rsi),
        "ema9": float(row.ema9), "ema21": float(row.ema21),
        "ema50": float(row.ema50), "ema200": float(row.ema200),
        "macd_hist": float(row.macd_hist),
        "volume_ratio": float(row.volume_ratio) if np.isfinite(row.volume_ratio) else 0,
        "support": support, "resistance": resistance,
        "bias": bias, "score": score, "reasons": reasons,
        "entry_low": entry_low, "entry_high": entry_high,
        "sl": sl, "tp1": tp1, "tp2": tp2,
        "forecast": forecast, "patterns": patterns, "fvg": fvg,
        "data": x
    }

def fmt(v):
    if v is None:
        return "N/A"
    return f"{v:,.6f}".rstrip("0").rstrip(".")

def make_report(symbol, timeframe, r):
    lines = [
        f"📊 {symbol} | {timeframe}",
        f"Giá đóng nến: {fmt(r['price'])}",
        f"Thiên hướng: {r['bias']} (score {r['score']})",
        "",
        "CHỈ BÁO",
        f"RSI14: {r['rsi']:.1f}",
        f"EMA9/21/50/200: {fmt(r['ema9'])} / {fmt(r['ema21'])} / {fmt(r['ema50'])} / {fmt(r['ema200'])}",
        f"MACD histogram: {fmt(r['macd_hist'])}",
        f"Volume / SMA20: {r['volume_ratio']:.2f}x",
        f"ATR14: {fmt(r['atr'])}",
        "",
        "VÙNG GIÁ",
        f"Hỗ trợ gần: {fmt(r['support'])}",
        f"Kháng cự gần: {fmt(r['resistance'])}",
        f"Vùng theo dõi: {fmt(r['entry_low'])} – {fmt(r['entry_high'])}",
    ]
    if r["sl"] is not None:
        lines += [f"SL tham chiếu: {fmt(r['sl'])}", f"TP1: {fmt(r['tp1'])}", f"TP2: {fmt(r['tp2'])}"]
    lines += ["", "LÝ DO"]
    lines += [f"• {x}" for x in r["reasons"]]
    if r["patterns"]:
        lines += ["", "MÔ HÌNH NẾN: " + ", ".join(r["patterns"])]
    if r["fvg"]:
        lines += ["FVG gần nhất: " + r["fvg"][0] + f" ({fmt(r['fvg'][1])} – {fmt(r['fvg'][2])})"]
    lines += [
        "", "KỊCH BẢN",
        f"BUY: theo dõi xác nhận vượt {fmt(r['resistance'])}, ưu tiên retest.",
        f"SELL: theo dõi xác nhận thủng {fmt(r['support'])}, ưu tiên retest.",
        "SIDEWAY: nếu giá còn nằm giữa hỗ trợ/kháng cự, chờ phá vỡ có xác nhận.",
        "",
        "⚠️ Phân tích tham khảo, không phải lệnh chắc thắng. Chờ nến đóng; tự kiểm tra spread, thanh khoản và rủi ro."
    ]
    return "\n".join(lines)

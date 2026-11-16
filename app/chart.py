import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplfinance as mpf
from pathlib import Path

def render_chart(df, result, symbol, timeframe, output="chart.png"):
    data = df.tail(120).copy()
    ap = [
        mpf.make_addplot(data["ema9"], color="#00C2A8", width=0.9),
        mpf.make_addplot(data["ema21"], color="#F5A623", width=0.9),
        mpf.make_addplot(data["ema50"], color="#4C8DFF", width=1.0),
    ]
    fig, axes = mpf.plot(
        data, type="candle", style="charles", volume=True, addplot=ap,
        title=f"{symbol} | {timeframe} | {result['bias']}",
        hlines=dict(hlines=[result["support"], result["resistance"]],
                    colors=["#16A36A", "#D94B4B"], linestyle="--", linewidths=1),
        returnfig=True, figsize=(14, 8), tight_layout=True
    )
    ax = axes[0]
    ax.text(0.01, 0.98,
            f"RSI {result['rsi']:.1f} | Score {result['score']} | ATR {result['atr']:.5g}",
            transform=ax.transAxes, va="top", fontsize=9,
            bbox=dict(facecolor="white", alpha=0.75, edgecolor="none"))
    # Illustrative conditional paths projected to the right of the last candle.
    x0 = len(data) - 1
    for key, color, label in [
        ("bull", "#16A36A", "BUY scenario"),
        ("bear", "#D94B4B", "SELL scenario"),
        ("side", "#777777", "SIDEWAY scenario")
    ]:
        vals = result["forecast"][key]
        ax.plot([x0, x0+1, x0+2, x0+3],
                [result["price"], *vals], linestyle=":", marker="o",
                color=color, linewidth=1.4, label=label)
    ax.legend(loc="upper left", fontsize=8)
    fig.savefig(output, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return str(Path(output).resolve())

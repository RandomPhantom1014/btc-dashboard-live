import numpy as np
from datetime import datetime, timedelta

def generate_signals_for_timeframe(df, tf_minutes):
    latest = df.iloc[-1]
    price = latest['close']
    rsi = latest.get('rsi', 50)
    macd = latest.get('macd', 0)
    signal_line = latest.get('signal', 0)
    volume = latest.get('volume', 0)

    signal = "Wait"
    confidence = 50

    # Short-term or long-term thresholds
    if tf_minutes in [5, 10, 15]:
        target_move = 0.01  # 1 cent
        strong_move = 0.02  # 2 cents
    elif tf_minutes in [60, 360]:
        target_move = 0.05  # 5 cents
        strong_move = 0.10  # 10 cents
    else:
        target_move = 0.01
        strong_move = 0.02

    # Decision logic
    if rsi > 55 and macd > signal_line:
        signal = "Go Long"
        confidence = 60 + (rsi - 55) * 2
    elif rsi < 45 and macd < signal_line:
        signal = "Go Short"
        confidence = 60 + (45 - rsi) * 2
    else:
        signal = "Wait"
        confidence = 40 + abs(rsi - 50)

    # Cap confidence
    confidence = max(10, min(99, round(confidence)))

    return {
        "signal": signal,
        "confidence": f"{confidence}%",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "countdown": str(timedelta(minutes=tf_minutes))
    }

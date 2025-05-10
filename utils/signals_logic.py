# utils/signals_logic.py

def generate_signals(df, timeframe):
    if df is None or df.empty:
        return "Wait", 0, "Weak"

    # Convert timeframe to row count
    tf_map = {"5m": 5, "10m": 10, "15m": 15, "1h": 60, "6h": 360, "12h": 720, "24h": 1440}
    rows = tf_map.get(timeframe, 5)
    if len(df) < rows:
        return "Wait", 0, "Weak"

    recent = df.tail(rows)
    close_prices = recent["close"]

    # RSI
    delta = close_prices.diff().dropna()
    gain = delta.where(delta > 0, 0).mean()
    loss = -delta.where(delta < 0, 0).mean()
    rs = gain / loss if loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))

    # MACD
    ema12 = close_prices.ewm(span=12, adjust=False).mean()
    ema26 = close_prices.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal_line = macd.ewm(span=9, adjust=False).mean()
    macd_recent = macd.iloc[-1]
    signal_recent = signal_line.iloc[-1]

    # Volume Spike
    avg_vol = df["volume"].rolling(window=rows).mean().iloc[-1]
    latest_vol = df["volume"].iloc[-1]
    vol_spike = latest_vol > avg_vol * 1.3

    # Scoring
    score = 0
    if rsi < 30: score += 1
    elif rsi > 70: score -= 1
    if macd_recent > signal_recent: score += 1
    else: score -= 1
    if vol_spike: score += 1

    # Signal Output
    if score >= 2:
        return "Go Long", 80 + score * 5, "Strong"
    elif score <= -2:
        return "Go Short", 80 + abs(score) * 5, "Strong"
    else:
        return "Wait", 50 + score * 5, "Moderate" if abs(score) == 1 else "Weak"

# components/signals_logic.py

def generate_signal(df, timeframe):
    if df is None or df.empty:
        return "Wait", 0, "Weak"

    # Use last N rows based on timeframe
    if timeframe == "5m":
        window = 5
    elif timeframe == "10m":
        window = 10
    elif timeframe == "15m":
        window = 15
    else:
        return "Wait", 0, "Weak"

    data = df.tail(window)

    # Extract latest values
    latest_rsi = data["rsi"].iloc[-1]
    latest_macd = data["macd"].iloc[-1]
    latest_close = data["close"].iloc[-1]
    prev_close = data["close"].iloc[0]

    price_change = latest_close - prev_close

    # Decision logic
    if latest_rsi < 30 and latest_macd > 0 and price_change > 0:
        return "Go Long", 92, "Strong"
    elif latest_rsi > 70 and latest_macd < 0 and price_change < 0:
        return "Go Short", 89, "Strong"
    elif abs(price_change) < 15:
        return "Wait", 60, "Weak"
    else:
        return "Wait", 70, "Moderate"


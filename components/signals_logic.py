# components/signals_logic.py

def generate_signal(df, timeframe_label):
    if df is None or df.empty:
        return "Wait", "0%", "Low"

    # Use the most recent row
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest

    signal = "Wait"
    confidence = 0
    strength = "Low"

    # RSI logic
    rsi = latest["RSI"]
    if rsi < 30:
        signal = "Go Long"
        confidence += 30
    elif rsi > 70:
        signal = "Go Short"
        confidence += 30
    else:
        confidence += 10

    # MACD crossover logic
    if latest["MACD"] > latest["Signal"] and prev["MACD"] <= prev["Signal"]:
        signal = "Go Long"
        confidence += 30
    elif latest["MACD"] < latest["Signal"] and prev["MACD"] >= prev["Signal"]:
        signal = "Go Short"
        confidence += 30

    # Volume spike
    avg_vol = df["volume"].rolling(window=10).mean().iloc[-1]
    if latest["volume"] > avg_vol * 1.5:
        confidence += 20

    # Final strength level
    if confidence >= 70:
        strength = "High"
    elif confidence >= 40:
        strength = "Medium"

    return signal, f"{confidence}%", strength


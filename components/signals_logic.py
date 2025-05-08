# components/signals_logic.py

def get_signal(df, minutes=5):
    """
    Calculate the signal for the given timeframe (in minutes).
    Assumes 1 row per minute.
    """
    if df is None or len(df) < minutes + 1:
        return "Wait", 0, 0

    recent = df.tail(minutes + 1)
    price_now = recent['close'].iloc[-1]
    price_then = recent['close'].iloc[0]
    delta = price_now - price_then

    # Example thresholds — customize for real-world use
    threshold = 30  # Adjust based on volatility preference

    if delta >= threshold:
        signal = "Go Long"
        confidence = round(min(100, abs(delta) * 2), 1)
        strength = min(10, int(abs(delta) / 10))
    elif delta <= -threshold:
        signal = "Go Short"
        confidence = round(min(100, abs(delta) * 2), 1)
        strength = min(10, int(abs(delta) / 10))
    else:
        signal = "Wait"
        confidence = 50
        strength = 5

    return signal, confidence, strength

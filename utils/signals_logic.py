import numpy as np

def generate_signals_for_timeframe(prices, rsi_values, timeframe, is_short_term=True):
    if len(prices) < 2 or len(prices) != len(rsi_values):
        return "Wait", 0

    recent_price = prices[-1]
    previous_price = prices[-2]
    price_change = recent_price - previous_price

    recent_rsi = rsi_values[-1]

    if is_short_term:
        # Short-term signal logic: 1–2 cents
        movement_required = 0.01 if abs(price_change) >= 0.01 else 0.02
    else:
        # Long-term signal logic: 5–10 cents
        movement_required = 0.05 if abs(price_change) >= 0.05 else 0.10

    # Signal confidence is proportional to how far RSI is from thresholds
    if recent_rsi > 55 and price_change >= movement_required:
        confidence = min(100, int((recent_rsi - 55) * 4 + (price_change / movement_required) * 50))
        return "Go Long", confidence
    elif recent_rsi < 45 and price_change <= -movement_required:
        confidence = min(100, int((45 - recent_rsi) * 4 + (-price_change / movement_required) * 50))
        return "Go Short", confidence
    else:
        return "Wait", 0

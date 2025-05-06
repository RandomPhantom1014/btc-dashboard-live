# components/signal_logic.py

import pandas as pd
from .indicators import calculate_rsi, calculate_macd, calculate_volume_trend

def generate_trade_signal(df):
    """
    Core logic for generating 'Go Long', 'Go Short', or 'Wait' signals based on indicators.
    """
    if df is None or df.empty or len(df) < 35:
        return "Wait", 0

    rsi = calculate_rsi(df)['rsi'].iloc[-1]
    macd_data = calculate_macd(df).iloc[-1]
    volume_trend = calculate_volume_trend(df).iloc[-1]

    signal = "Wait"
    confidence = 50  # Neutral baseline

    # Sample logic
    if rsi < 30 and macd_data['macd'] > macd_data['signal']:
        signal = "Go Long"
        confidence += 25
    elif rsi > 70 and macd_data['macd'] < macd_data['signal']:
        signal = "Go Short"
        confidence += 25
    else:
        signal = "Wait"

    # Adjust based on volume
    if signal != "Wait":
        if df['volume'].iloc[-1] > volume_trend:
            confidence += 5
        else:
            confidence -= 5

    confidence = max(0, min(100, confidence))  # Clamp between 0 and 100
    return signal, confidence

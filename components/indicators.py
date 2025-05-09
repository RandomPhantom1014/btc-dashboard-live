# utils/indicators.py

import pandas as pd

def calculate_rsi(close_prices, period=14):
    delta = close_prices.diff().dropna()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss.replace(0, 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(0).tolist()

def calculate_macd(close_prices, span_fast=12, span_slow=26, signal_span=9):
    ema_fast = close_prices.ewm(span=span_fast, adjust=False).mean()
    ema_slow = close_prices.ewm(span=span_slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=signal_span, adjust=False).mean()
    histogram = macd - signal
    return macd.fillna(0).tolist(), signal.fillna(0).tolist()

def calculate_volume(volume_data):
    return volume_data.fillna(0).tolist()


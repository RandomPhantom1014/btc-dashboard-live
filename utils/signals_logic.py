import pandas as pd
import numpy as np

def generate_signals(df, timeframe):
    df = df.copy()
    df['RSI'] = compute_rsi(df['close'], 14)
    df['MACD'] = compute_macd(df['close'])

    recent = df.iloc[-1]
    rsi = recent['RSI']
    macd = recent['MACD']
    volume = recent['volume']

    signal = "Wait"
    confidence = 50
    strength_class = "neutral"

    if rsi < 30 and macd > 0:
        signal = "Go Long"
        confidence = 80
        strength_class = "strong-long"
    elif rsi > 70 and macd < 0:
        signal = "Go Short"
        confidence = 80
        strength_class = "strong-short"
    elif 45 < rsi < 55:
        signal = "Wait"
        confidence = 55
        strength_class = "neutral"
    else:
        signal = "Wait"
        confidence = 50
        strength_class = "neutral"

    return {
        'signal': signal,
        'confidence': confidence,
        'strength_class': strength_class
    }

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_macd(series, fast=12, slow=26, signal=9):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    return macd - macd.ewm(span=signal, adjust=False).mean()

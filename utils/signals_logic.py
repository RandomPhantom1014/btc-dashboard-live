import pandas as pd
import numpy as np

def generate_signals(df, timeframe):
    df = df.copy()

    # Indicators
    df['RSI'] = compute_rsi(df['close'], 14)
    df['MACD'] = compute_macd(df['close'])
    df['momentum'] = df['close'] - df['close'].shift(5)
    df['avg_volume'] = df['volume'].rolling(window=20).mean()
    df['volume_spike'] = df['volume'] > 1.5 * df['avg_volume']
    df['price_delta'] = df['close'] - df['close'].shift(5)

    recent = df.iloc[-1]
    rsi = recent['RSI']
    macd = recent['MACD']
    momentum = recent['momentum']
    volume_spike = recent['volume_spike']
    price_delta = recent['price_delta']

    signal = "Wait"
    confidence = 50
    strength_class = "neutral"

    if rsi > 58 and macd > 0 and momentum > 0:
        signal = "Go Long"
        confidence = 85 if volume_spike else 75
        strength_class = "strong-long"
    elif rsi < 45 and macd < 0 and momentum < 0:
        signal = "Go Short"
        confidence = 85 if volume_spike else 75
        strength_class = "strong-short"
    elif rsi > 65 and price_delta < -100:
        signal = "Go Short"
        confidence = 70
        strength_class = "weak-short"
    elif rsi < 40 and price_delta > 100:
        signal = "Go Long"
        confidence = 70
        strength_class = "weak-long"
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
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line - signal_line

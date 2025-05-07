# components/indicators.py

import pandas as pd

def calculate_rsi(df, period=14):
    if 'close' not in df:
        return [0] * len(df)
    
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss.replace(to_replace=0, method='ffill')
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(0)

def calculate_macd(df, fast=12, slow=26, signal=9):
    if 'close' not in df:
        return [0] * len(df), [0] * len(df)

    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()

    return macd_line.fillna(0), signal_line.fillna(0)

def calculate_volume(df):
    if 'volume' not in df:
        return [0] * len(df)
    return df['volume'].fillna(0)


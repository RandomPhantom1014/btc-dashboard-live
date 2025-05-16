import pandas as pd
import requests
import datetime as dt
import time
import numpy as np

def get_latest_price():
    url = "https://api.pro.coinbase.com/products/XRP-USD/ticker"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data["price"])
    except Exception:
        return 0.0

def get_indicator_data():
    url = "https://api.pro.coinbase.com/products/XRP-USD/candles?granularity=60"
    try:
        response = requests.get(url, timeout=5)
        raw = response.json()
        df = pd.DataFrame(raw, columns=["time", "low", "high", "open", "close", "volume"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.sort_values("time", inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Indicators
        df["rsi"] = compute_rsi(df["close"], 14)
        df["macd"], df["signal"] = compute_macd(df["close"])
        df["volume_ma"] = df["volume"].rolling(window=5).mean()

        return df
    except Exception:
        return pd.DataFrame()

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def compute_macd(series, short=12, long=26, signal=9):
    exp1 = series.ewm(span=short, adjust=False).mean()
    exp2 = series.ewm(span=long, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

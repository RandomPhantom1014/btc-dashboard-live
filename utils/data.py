# utils/data.py

import requests
import pandas as pd
import numpy as np

BACKTEST_PATH = "data/backtest_btc.csv"

def fetch_live_btc_data():
    try:
        url = "https://api.pro.coinbase.com/products/BTC-USD/candles?granularity=60"
        response = requests.get(url)
        response.raise_for_status()

        raw_data = response.json()

        df = pd.DataFrame(raw_data, columns=[
            "timestamp", "low", "high", "open", "close", "volume"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")
        return df.reset_index(drop=True)

    except Exception as e:
        print("Error fetching live data:", e)
        return pd.DataFrame()

def fetch_backtest_data():
    try:
        df = pd.read_csv(BACKTEST_PATH)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception as e:
        print("Error loading backtest data:", e)
        return pd.DataFrame()

def calculate_indicators(df):
    if df.empty:
        return df

    df["RSI"] = compute_rsi(df["close"], 14)
    df["EMA12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["EMA26"] = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return pd.Series(rsi).fillna(50)

def get_btc_data(mode="live"):
    if mode == "backtest":
        df = fetch_backtest_data()
    else:
        df = fetch_live_btc_data()

    if df.empty:
        return df

    return calculate_indicators(df)

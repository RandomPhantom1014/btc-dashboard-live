# utils/data.py

import pandas as pd
import os
import csv
from datetime import datetime

LOG_FILE = "logs/signal_log.csv"
BACKTEST_FILE = "data/backtest_btc.csv"

def ensure_log_file_exists():
    os.makedirs("logs", exist_ok=True)
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "timeframe", "signal", "confidence", "strength", "price"])

def append_log(timeframe, signal, confidence, strength, price):
    ensure_log_file_exists()
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            timeframe,
            signal,
            confidence,
            strength,
            price
        ])

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(0)

def calculate_macd(series, fast=12, slow=26):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    return (exp1 - exp2).fillna(0)

def get_btc_data(mode="live"):
    try:
        df = pd.read_csv(BACKTEST_FILE)
        df.rename(columns=lambda col: col.lower(), inplace=True)

        if "timestamp" not in df.columns:
            raise ValueError("CSV must have a 'timestamp' column.")

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["rsi"] = calculate_rsi(df["close"])
        df["macd"] = calculate_macd(df["close"])
        return df
    except Exception as e:
        print("Error loading BTC data:", e)
        return pd.DataFrame()

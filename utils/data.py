# utils/data.py

import os
import csv
import requests
import pandas as pd
from datetime import datetime

LOG_FILE = "logs/signal_log.csv"
BACKTEST_FILE = "data/backtest_btc.csv"

# Ensure logs directory exists
def ensure_log_file_exists():
    os.makedirs("logs", exist_ok=True)
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "timeframe", "signal", "confidence", "strength", "price"])

# Append new signal row to log
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

# Load Coinbase BTC-USD candlestick data (past 100 minutes)
def get_live_data():
    try:
        url = "https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=60"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        raw_data = response.json()

        # Format to DataFrame: [time, low, high, open, close, volume]
        df = pd.DataFrame(raw_data, columns=["timestamp", "low", "high", "open", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df.sort_values("timestamp", inplace=True)

        # Convert to float just in case
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

        return df.reset_index(drop=True)

    except Exception as e:
        print(f"Error fetching live data: {e}")
        return pd.DataFrame()

# Load backtest data from CSV
def get_backtest_data():
    try:
        df = pd.read_csv(BACKTEST_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception as e:
        print(f"Error loading backtest data: {e}")
        return pd.DataFrame()

# Unified function based on mode
def get_btc_data(mode="live"):
    if mode == "live":
        return get_live_data()
    else:
        return get_backtest_data()

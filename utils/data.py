import os
import pandas as pd
import requests
from datetime import datetime
import csv

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

def get_btc_data(mode="live"):
    if mode == "backtest":
        if os.path.exists(BACKTEST_FILE):
            df = pd.read_csv(BACKTEST_FILE)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            return df
        else:
            print("Backtest file not found.")
            return pd.DataFrame()

    try:
        url = "https://api.pro.coinbase.com/products/BTC-USD/candles?granularity=60"
        response = requests.get(url)
        candles = response.json()
        df = pd.DataFrame(candles, columns=["time", "low", "high", "open", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("timestamp", inplace=True)
        df = df.sort_index()
        return df[["open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"Error fetching live BTC data: {e}")
        return pd.DataFrame()

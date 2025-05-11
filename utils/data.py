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
        # Fetch 1-minute candles up to 1440 rows (for 24h)
        url = "https://api.pro.coinbase.com/products/BTC-USD/candles"
        all_candles = []
        for _ in range(6):  # 6x300 = ~1800 candles
            params = {"granularity": 60, "limit": 300}
            if all_candles:
                params["end"] = all_candles[-1][0] - 1
            response = requests.get(url, params=params)
            candles = response.json()
            if not isinstance(candles, list) or len(candles) == 0:
                break
            all_candles.extend(candles)
            if len(all_candles) >= 1440:
                break

        df = pd.DataFrame(all_candles, columns=["time", "low", "high", "open", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("timestamp", inplace=True)
        df = df.sort_index()
        return df[["open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"Error fetching live BTC data: {e}")
        return pd.DataFrame()

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
        # Fetch 1440 1-minute candles (approx. 24h)
        url = "https://api.pro.coinbase.com/products/BTC-USD/candles?granularity=60"
        df_list = []

        # Coinbase only returns 300 rows per call, so we iterate
        now = int(datetime.utcnow().timestamp())
        seconds_per_chunk = 60 * 300  # 5 hours
        for i in range(5):  # Up to 1500 candles = 25 hours
            end = now - (i * seconds_per_chunk)
            start = end - seconds_per_chunk
            chunk_url = f"{url}&start={start}&end={end}"
            response = requests.get(chunk_url)
            if response.status_code != 200:
                continue
            candles = response.json()
            df_chunk = pd.DataFrame(candles, columns=["time", "low", "high", "open", "close", "volume"])
            df_list.append(df_chunk)

        if not df_list:
            print("No data returned from Coinbase.")
            return pd.DataFrame()

        df = pd.concat(df_list, ignore_index=True)
        df["timestamp"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("timestamp", inplace=True)
        df = df.sort_index()
        return df[["open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"Error fetching live BTC data: {e}")
        return pd.DataFrame()


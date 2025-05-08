import csv
import os
from datetime import datetime

import pandas as pd
import requests

# ====== LOGGING FUNCTIONS ======
LOG_FILE = "logs/signal_log.csv"

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

# ====== BTC DATA FETCH FUNCTION ======
def get_btc_data():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1m",  # 1-minute candles
        "limit": 100       # Get last 100 minutes of data
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
        ])

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        df = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df

    except Exception as e:
        print(f"Error fetching BTC data: {e}")
        return pd.DataFrame()


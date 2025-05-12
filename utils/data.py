import pandas as pd
import requests

def fetch_live_data():
    url = "https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=60"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df = df.sort_values("time")
        return df
    except Exception as e:
        print(f"[ERROR - fetch_live_data]: {e}")
        return pd.DataFrame()

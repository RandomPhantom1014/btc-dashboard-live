import pandas as pd
import requests

def fetch_live_data():
    try:
        url = "https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=60"
        response = requests.get(url, headers={"User-Agent": "BTC-Dashboard"})
        response.raise_for_status()
        data = response.json()

        if not data or not isinstance(data, list):
            raise ValueError("Empty or malformed data returned from Coinbase")

        df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.sort_values('time', inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    except Exception as e:
        print(f"[ERROR - fetch_live_data] {e}")
        return pd.DataFrame()  # return empty DataFrame to avoid full crash

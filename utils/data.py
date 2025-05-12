import pandas as pd
import requests

def fetch_live_data():
    url = "https://api.pro.coinbase.com/products/BTC-USD/candles?granularity=60"
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.sort_values('time', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

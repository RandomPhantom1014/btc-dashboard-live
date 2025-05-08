import pandas as pd
import os

def get_btc_data(mode='live'):
    if mode == 'backtest':
        path = os.path.join("data", "backtest_btc.csv")
        if not os.path.exists(path):
            print("Backtest file not found.")
            return pd.DataFrame()
        df = pd.read_csv(path, parse_dates=['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    else:
        # fallback for live mode
        return pd.DataFrame()  # live mode handled elsewhere


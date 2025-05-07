# components/utils.py

import requests
import random

def fetch_binance_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return float(response.json()['price'])
        else:
            print("Binance API error:", response.status_code)
            return None
    except Exception as e:
        print("Error fetching Binance price:", e)
        return None

def simulate_signals():
    signals = {}
    for tf in ["5m", "10m", "15m"]:
        signals[tf] = {
            "signal": random.choice(["Long", "Short", "Hold"]),
            "confidence": random.randint(65, 99)
        }
    return signals

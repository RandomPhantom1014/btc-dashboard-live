# components/utils.py

import requests
import random

def fetch_binance_price():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        if response.status_code == 200:
            return float(response.json()['price'])
        else:
            return None
    except Exception as e:
        print("Error fetching price:", e)
        return None

def simulate_signals():
    return {
        "5m": {
            "signal": random.choice(["Long", "Short", "Hold"]),
            "confidence": random.randint(70, 99)
        },
        "10m": {
            "signal": random.choice(["Long", "Short", "Hold"]),
            "confidence": random.randint(70, 99)
        },
        "15m": {
            "signal": random.choice(["Long", "Short", "Hold"]),
            "confidence": random.randint(70, 99)
        }
    }

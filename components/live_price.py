# components/live_price.py

import requests

def fetch_live_btc_price():
    try:
        url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Extract price from response
        return float(data["data"]["amount"])

    except Exception as e:
        print(f"Error fetching live BTC price: {e}")
        return None

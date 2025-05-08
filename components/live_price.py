# components/live_price.py

import requests

def fetch_live_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        price = data.get("bitcoin", {}).get("usd")
        if price is None:
            raise ValueError("BTC price not found in API response")
        return float(price)
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

# components/live_price.py

import requests

def fetch_live_btc_price():
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "bitcoin", "vs_currencies": "usd"},
            timeout=5
        )
        data = response.json()
        return f"${data['bitcoin']['usd']:,}"
    except Exception as e:
        return "Price unavailable"

import requests

def fetch_live_btc_price():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["data"]["amount"])
    except Exception as e:
        print("Error fetching price:", e)
        return None

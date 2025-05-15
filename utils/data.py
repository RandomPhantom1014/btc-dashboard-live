import requests

def get_latest_price():
    try:
        url = "https://api.coinbase.com/v2/prices/XRP-USD/spot"
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        return float(data["data"]["amount"])
    except Exception:
        return None

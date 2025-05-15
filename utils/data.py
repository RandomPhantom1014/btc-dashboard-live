import requests

def get_latest_price():
    """Fetch the latest XRP price from Coinbase."""
    url = "https://api.coinbase.com/v2/prices/XRP-USD/spot"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return float(data["data"]["amount"])
    else:
        return 0.0

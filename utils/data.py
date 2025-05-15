import requests

def get_coinbase_price(symbol="XRP-USD"):
    url = f"https://api.coinbase.com/v2/prices/{symbol}/spot"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data["data"]["amount"])
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None

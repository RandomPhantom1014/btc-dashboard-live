import requests

def get_live_price():
    url = "https://api.coinbase.com/v2/prices/XRP-USD/spot"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        price = float(data['data']['amount'])
        return round(price, 4)
    except Exception as e:
        print(f"[ERROR] Failed to fetch XRP price: {e}")
        return 0.0

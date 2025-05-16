import requests

def get_live_price():
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/XRP-USD/spot", timeout=5)
        data = response.json()
        return round(float(data['data']['amount']), 4)
    except Exception as e:
        print(f"[ERROR] Price fetch failed: {e}")
        return 0.0

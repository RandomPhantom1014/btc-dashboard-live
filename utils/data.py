import requests

def get_latest_price():
    url = "https://api.pro.coinbase.com/products/XRP-USD/ticker"
    response = requests.get(url)
    if response.status_code == 200:
        return float(response.json()["price"])
    return "N/A"

def get_indicator_data():
    return {
        "rsi": 52,
        "macd": 0.001,
        "volume": 1200000
    }

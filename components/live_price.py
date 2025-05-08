import requests

def fetch_live_btc_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        data = response.json()
        if "bitcoin" in data and "usd" in data["bitcoin"]:
            return data["bitcoin"]["usd"]
        else:
            print("BTC price not found in API response:", data)
            return None
    except Exception as e:
        print("Error fetching price:", e)
        return None

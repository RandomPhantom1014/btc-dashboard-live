# binance_ws.py
import websocket
import threading
import json

# Global variable to store the latest price
latest_price = {"BTCUSDT": None}

def on_message(ws, message):
    data = json.loads(message)
    if "p" in data:
        latest_price["BTCUSDT"] = float(data["p"])

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    payload = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@trade"],
        "id": 1
    }
    ws.send(json.dumps(payload))

def start_socket():
    ws = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws/btcusdt@trade",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

# Start the WebSocket connection on import
start_socket()

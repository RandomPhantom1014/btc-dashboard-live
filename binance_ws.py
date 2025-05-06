# binance_ws.py

import websocket
import json
from threading import Thread
from datetime import datetime

btc_prices = []

# Store only last 60 candles
MAX_CANDLES = 60


def on_message(ws, message):
    data = json.loads(message)
    kline = data['k']
    candle = {
        'timestamp': datetime.fromtimestamp(kline['t'] / 1000),
        'open': float(kline['o']),
        'high': float(kline['h']),
        'low': float(kline['l']),
        'close': float(kline['c'])
    }

    if kline['x']:  # if candle is closed
        btc_prices.append(candle)
        if len(btc_prices) > MAX_CANDLES:
            btc_prices.pop(0)


def on_error(ws, error):
    print("WebSocket Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")


def on_open(ws):
    print("WebSocket connection opened")
    payload = {
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@kline_1m"
        ],
        "id": 1
    }
    ws.send(json.dumps(payload))


def start_ws():
    ws = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws/btcusdt@kline_1m",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()


# Launch in background thread
ws_thread = Thread(target=start_ws)
ws_thread.daemon = True
ws_thread.start()

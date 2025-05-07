# components/callbacks.py

from dash import Output, Input
import requests
import random

def fetch_mock_signals():
    signals = ["Go Long", "Go Short", "Wait"]
    confidence = round(random.uniform(50, 99), 2)
    strength = random.choice(["Strong", "Moderate", "Weak"])
    return random.choice(signals), f"Confidence: {confidence}%", strength

def register_callbacks(app):
    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_price(n):
        try:
            response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
            price = float(response.json()["price"])
            return f"${price:,.2f}"
        except:
            return "Error fetching price"

    for timeframe in ["5m", "10m", "15m"]:
        @app.callback(
            Output(f"signal-{timeframe}", "children"),
            Output(f"confidence-{timeframe}", "children"),
            Output(f"strength-{timeframe}", "className"),
            Input("interval-component", "n_intervals")
        )
        def update_signals(n, timeframe=timeframe):
            signal, confidence, strength = fetch_mock_signals()
            return signal, confidence, f"pill-{strength.lower()}"

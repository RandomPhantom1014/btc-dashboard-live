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
    # Live BTC price updater
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

    # Individual callbacks per timeframe — must be separate
    @app.callback(
        Output("signal-5m", "children"),
        Output("confidence-5m", "children"),
        Output("strength-5m", "className"),
        Input("interval-component", "n_intervals")
    )
    def update_5m(n):
        signal, confidence, strength = fetch_mock_signals()
        return signal, confidence, f"pill-{strength.lower()}"

    @app.callback(
        Output("signal-10m", "children"),
        Output("confidence-10m", "children"),
        Output("strength-10m", "className"),
        Input("interval-component", "n_intervals")
    )
    def update_10m(n):
        signal, confidence, strength = fetch_mock_signals()
        return signal, confidence, f"pill-{strength.lower()}"

    @app.callback(
        Output("signal-15m", "children"),
        Output("confidence-15m", "children"),
        Output("strength-15m", "className"),
        Input("interval-component", "n_intervals")
    )
    def update_15m(n):
        signal, confidence, strength = fetch_mock_signals()
        return signal, confidence, f"pill-{strength.lower()}"


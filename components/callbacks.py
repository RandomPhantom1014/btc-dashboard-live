# components/callbacks.py

from dash import Output, Input, State
import requests
import random
from components.theme import DARK_THEME, LIGHT_THEME

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
            Input("interval-component", "n_intervals"),
            State("signal-mode", "value")
        )
        def update_signals(n, mode="live", timeframe=timeframe):
            signal, confidence, strength = fetch_mock_signals()  # You could swap with actual logic based on mode
            return signal, confidence, f"pill-{strength.lower()}"

    @app.callback(
        Output("main-container", "style"),
        Input("theme-toggle", "value")
    )
    def update_theme(selected_theme):
        theme = DARK_THEME if selected_theme == "dark" else LIGHT_THEME
        return {
            "backgroundColor": theme["backgroundColor"],
            "color": theme["textColor"],
            "padding": "10px"
        }


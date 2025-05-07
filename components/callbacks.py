# components/callbacks.py

from dash import Output, Input, State
import requests, random
from components.utils import append_log
import pandas as pd

def fetch_mock_signals():
    signals = ["Go Long", "Go Short", "Wait"]
    confidence = round(random.uniform(50, 99), 2)
    strength = random.choice(["Strong", "Moderate", "Weak"])
    return random.choice(signals), f"Confidence: {confidence}%", strength

def register_callbacks(app):
    live_price = {"value": None}  # global cache

    @app.callback(Output("live-btc-price", "children"), Input("interval-component", "n_intervals"))
    def update_price(n):
        try:
            response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
            price = float(response.json()["price"])
            live_price["value"] = price
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
            price = live_price.get("value", 0)
            append_log(timeframe, signal, confidence, strength, price)
            return signal, confidence, f"pill-{strength.lower()}"

    @app.callback(
        Output("export-status", "children"),
        Input("export-button", "n_clicks"),
        prevent_initial_call=True
    )
    def export_logs(n_clicks):
        try:
            df = pd.read_csv("logs/signal_log.csv")
            df.to_csv("assets/exported_signal_log.csv", index=False)
            return "✅ Exported to exported_signal_log.csv"
        except Exception as e:
            return f"❌ Export failed: {str(e)}"

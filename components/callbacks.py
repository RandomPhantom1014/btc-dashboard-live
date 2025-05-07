# components/callbacks.py

from dash import Output, Input, State
import requests
from components.signal_logic import fetch_live_signals, fetch_backtest_signals

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
            State("mode-toggle", "value")
        )
        def update_signals(n, mode, timeframe=timeframe):
            if mode == "live":
                signal, confidence, strength = fetch_live_signals()
            else:
                signal, confidence, strength = fetch_backtest_signals()
            return signal, confidence, f"pill-{strength.lower()}"


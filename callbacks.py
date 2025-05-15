from dash import Input, Output, State, callback_context
from datetime import datetime, timedelta
from utils.data import get_latest_price, get_indicator_data
from utils.signals_logic import generate_signals_for_timeframe
import pytz

timeframes = {
    "5m": {"minutes": 5, "is_short_term": True},
    "10m": {"minutes": 10, "is_short_term": True},
    "15m": {"minutes": 15, "is_short_term": True},
    "1h": {"minutes": 60, "is_short_term": False},
    "6h": {"minutes": 360, "is_short_term": False}
}

def register_callbacks(app):
    @app.callback(
        [Output("xrp-price-text", "children")],
        Input("interval-component", "n_intervals")
    )
    def update_price(n):
        price = get_latest_price()
        return [f"${price:.4f}"]

    @app.callback(
        [Output(f"{key}-signal", "children"),
         Output(f"{key}-confidence", "children"),
         Output(f"{key}-signal", "className"),
         Output(f"{key}-timestamp", "children"),
         Output(f"{key}-countdown", "children")]
        for key in timeframes
    , Input("interval-component", "n_intervals"))
    def update_signals(n):
        now = datetime.now(pytz.timezone("US/Hawaii"))
        timestamp = now.strftime("%H:%M:%S")

        prices, rsi_values, _, _ = get_indicator_data()

        results = []
        for key, config in timeframes.items():
            signal, confidence = generate_signals_for_timeframe(
                prices, rsi_values, key, is_short_term=config["is_short_term"]
            )

            # Style class based on signal strength
            if signal == "Go Long":
                class_name = "signal-pill long"
            elif signal == "Go Short":
                class_name = "signal-pill short"
            else:
                class_name = "signal-pill wait"

            # Countdown
            expires_at = now + timedelta(minutes=config["minutes"])
            countdown = expires_at.strftime("%H:%M:%S")

            results.extend([signal, f"{confidence}%", class_name, timestamp, countdown])

        return results

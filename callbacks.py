from dash import Output, Input, callback
from utils.data import get_latest_price, get_indicator_data
from utils.signals_logic import generate_signals_for_timeframe
from datetime import datetime, timedelta
import pytz

TIMEFRAMES = {
    "5m": 5,
    "10m": 10,
    "15m": 15,
    "1h": 60,
    "6h": 360
}

@callback(
    Output("xrp-price-text", "children"),
    Input("interval-component", "n_intervals")
)
def update_price(n):
    price = get_latest_price()
    return f"Live XRP Price: ${price:.4f}"

# Manually flatten the Outputs
@callback(
    [
        Output("5m-signal", "children"),
        Output("5m-confidence", "children"),
        Output("5m-signal", "className"),
        Output("5m-timestamp", "children"),
        Output("5m-countdown", "children"),

        Output("10m-signal", "children"),
        Output("10m-confidence", "children"),
        Output("10m-signal", "className"),
        Output("10m-timestamp", "children"),
        Output("10m-countdown", "children"),

        Output("15m-signal", "children"),
        Output("15m-confidence", "children"),
        Output("15m-signal", "className"),
        Output("15m-timestamp", "children"),
        Output("15m-countdown", "children"),

        Output("1h-signal", "children"),
        Output("1h-confidence", "children"),
        Output("1h-signal", "className"),
        Output("1h-timestamp", "children"),
        Output("1h-countdown", "children"),

        Output("6h-signal", "children"),
        Output("6h-confidence", "children"),
        Output("6h-signal", "className"),
        Output("6h-timestamp", "children"),
        Output("6h-countdown", "children"),
    ],
    Input("interval-component", "n_intervals")
)
def update_signals(n):
    df = get_indicator_data()
    now = datetime.now(pytz.timezone("US/Hawaii"))

    results = []
    for tf, minutes in TIMEFRAMES.items():
        signal, confidence = generate_signals_for_timeframe(df, tf)
        color = "green-pill" if signal == "Go Long" else "red-pill" if signal == "Go Short" else "gray-pill"
        timestamp = now.strftime("%I:%M %p %Z")
        countdown = f"{minutes}:00"
        results.extend([signal, f"{confidence}%", color, timestamp, countdown])

    return results

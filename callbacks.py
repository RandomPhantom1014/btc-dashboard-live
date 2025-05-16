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

@callback(
    [Output(f"{tf}-signal", "children"),
     Output(f"{tf}-confidence", "children"),
     Output(f"{tf}-signal", "className"),
     Output(f"{tf}-timestamp", "children"),
     Output(f"{tf}-countdown", "children")]
    for tf in TIMEFRAMES
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

        results.append((signal, f"{confidence}%", color, timestamp, countdown))

    return results


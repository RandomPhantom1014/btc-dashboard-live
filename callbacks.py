from dash import Output, Input, callback
from utils.signals_logic import generate_signal
from utils.data import fetch_live_price
from datetime import datetime, timedelta
import pytz

hst = pytz.timezone('US/Hawaii')
timeframes = ['5m', '10m', '15m', '1h', '6h']

# Generate outputs and inputs dynamically
output_list = []
for tf in timeframes:
    output_list.extend([
        Output(f"{tf}-signal", "children"),
        Output(f"{tf}-confidence", "children"),
        Output(f"{tf}-signal", "className"),
        Output(f"{tf}-timestamp", "children"),
        Output(f"{tf}-countdown", "children")
    ])
output_list.insert(0, Output("xrp-price-text", "children"))  # Live price at top

@callback(
    output_list,
    Input("interval-component", "n_intervals"),
    Input("mode-toggle", "value")
)
def update_signals(n, mode):
    price = fetch_live_price()
    now = datetime.now(hst).strftime('%H:%M:%S HST')

    all_outputs = [f"XRP Price: ${price:.4f}"]  # live price at top

    for tf in timeframes:
        signal, confidence = generate_signal(price, tf, mode)

        if signal == "Go Long":
            class_name = "pill pill-long"
        elif signal == "Go Short":
            class_name = "pill pill-short"
        else:
            class_name = "pill pill-wait"

        countdown_time = {
            '5m': 5, '10m': 10, '15m': 15,
            '1h': 60, '6h': 360
        }.get(tf, 5)

        expire_time = (datetime.now(hst) + timedelta(minutes=countdown_time)).strftime('%H:%M:%S')

        all_outputs.extend([
            signal,
            f"Confidence: {confidence}%",
            class_name,
            f"Signal Time: {now}",
            f"Expires: {expire_time}"
        ])

    return all_outputs

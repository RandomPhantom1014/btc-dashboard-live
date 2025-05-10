# callbacks.py

from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

# Track previous live price
previous_price = None
last_signal_times = {}

def register_callbacks(app):
    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_btc_price(n):
        global previous_price
        price = fetch_live_btc_price()
        if price is None:
            return "Live BTC Price: Error"

        color = "white"
        if previous_price is not None:
            if price > previous_price:
                color = "limegreen"
            elif price < previous_price:
                color = "red"
        previous_price = price

        return html.Div([
            html.Span("Live BTC Price: ", style={"fontWeight": "bold", "marginRight": "8px"}),
            html.Span(f"${float(price):,.2f}", style={"color": color, "fontWeight": "bold"})
        ])

    @app.callback(
        [Output(f"signal-{t}", "children") for t in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]] +
        [Output(f"confidence-{t}", "children") for t in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]] +
        [Output(f"strength-{t}", "children") for t in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]] +
        [Output(f"timestamp-{t}", "children") for t in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]] +
        [Output(f"countdown-{t}", "children") for t in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]],
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        timeframes = {
            "5m": 5,
            "10m": 10,
            "15m": 15,
            "1h": 60,
            "6h": 360,
            "12h": 720,
            "24h": 1440,
        }

        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        signal_outputs, confidence_outputs, strength_outputs, timestamps, countdowns = [], [], [], [], []

        for tf, minutes in timeframes.items():
            signal, confidence, strength = generate_signals(df, tf)
            signal_outputs.append(signal)
            confidence_outputs.append(f"Confidence: {confidence}%")
            strength_outputs.append(strength)

            # Save signal timestamp for countdown logic
            if signal != "Wait":
                last_signal_times[tf] = utc_now

            signal_time = last_signal_times.get(tf)
            if signal_time:
                local_time = signal_time.astimezone(pytz.timezone("Pacific/Honolulu"))
                timestamps.append(f"Issued: {local_time.strftime('%H:%M:%S HST')}")

                elapsed = utc_now - signal_time
                remaining = max(0, minutes * 60 - int(elapsed.total_seconds()))
                countdowns.append(f"Time left: {remaining // 60:02d}:{remaining % 60:02d}")
            else:
                timestamps.append("Issued: --")
                countdowns.append("Time left: --:--")

            # Save to logs if enabled
            if save_logs:
                current_price = df["close"].iloc[-1]
                append_log(tf, signal, confidence, strength, current_price)

        return signal_outputs + confidence_outputs + strength_outputs + timestamps + countdowns

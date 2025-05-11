from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

signal_times = {tf: None for tf in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]}
previous_price = None

def format_hst(dt):
    hst = pytz.timezone("Pacific/Honolulu")
    return dt.astimezone(hst).strftime("%Y-%m-%d %I:%M:%S %p HST")

def calculate_countdown(start_time, duration):
    if start_time is None:
        return "Waiting..."
    remaining = (start_time + timedelta(minutes=duration)) - datetime.utcnow()
    if remaining.total_seconds() <= 0:
        return "Refreshing..."
    minutes, seconds = divmod(int(remaining.total_seconds()), 60)
    return f"{minutes}m {seconds}s left"

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

        color = "black"
        if previous_price is not None:
            if price > previous_price:
                color = "green"
            elif price < previous_price:
                color = "red"
        previous_price = price

        return html.Div([
            html.Span("Live BTC Price: ", style={"fontWeight": "bold", "marginRight": "8px"}),
            html.Span(f"${float(price):,.2f}", style={"color": color, "fontWeight": "bold"})
        ])

    @app.callback(
        [Output(f"signal-{tf}", "children") for tf in signal_times] +
        [Output(f"confidence-{tf}", "children") for tf in signal_times] +
        [Output(f"strength-{tf}", "children") for tf in signal_times] +
        [Output(f"timestamp-{tf}", "children") for tf in signal_times] +
        [Output(f"countdown-{tf}", "children") for tf in signal_times],
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        durations = {
            "5m": 5, "10m": 10, "15m": 15,
            "1h": 60, "6h": 360, "12h": 720, "24h": 1440
        }

        signals, confidences, strengths, timestamps, countdowns = [], [], [], [], []

        for tf, minutes in durations.items():
            s, c, st = generate_signals(df, tf)
            signals.append(s)
            confidences.append(f"Confidence: {c}%")
            strengths.append(f"Strength: {st}")

            now = datetime.utcnow()
            if s != "Wait":
                signal_times[tf] = now

            timestamps.append("Issued: " + format_hst(signal_times[tf]) if signal_times[tf] else "Pending...")
            countdowns.append(calculate_countdown(signal_times[tf], minutes))

            if save_logs:
                price = df["close"].iloc[-1]
                append_log(tf, s, c, st, price)

        return signals + confidences + strengths + timestamps + countdowns

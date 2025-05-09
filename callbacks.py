# callbacks.py

from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta

previous_price = None
last_signals = {"5m": None, "10m": None, "15m": None}
last_timestamps = {"5m": None, "10m": None, "15m": None}

def format_countdown(signal_time, duration_minutes):
    remaining = (signal_time + timedelta(minutes=duration_minutes)) - datetime.utcnow()
    if remaining.total_seconds() < 0:
        return "Expired"
    mins, secs = divmod(int(remaining.total_seconds()), 60)
    return f"{mins}:{secs:02d}"

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

        return [
            "Live BTC Price: ",
            {"type": "span", "props": {
                "style": {"color": color, "fontWeight": "bold"},
                "children": f"${float(price):,.2f}"
            }}
        ]

    @app.callback(
        Output("signal-5m", "children"),
        Output("confidence-5m", "children"),
        Output("strength-5m", "children"),
        Output("signal-10m", "children"),
        Output("confidence-10m", "children"),
        Output("strength-10m", "children"),
        Output("signal-15m", "children"),
        Output("confidence-15m", "children"),
        Output("strength-15m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        global last_signals, last_timestamps

        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        now = datetime.utcnow()

        output = []
        for tf in ["5m", "10m", "15m"]:
            minutes = int(tf.replace("m", ""))

            if last_timestamps[tf] is None or now - last_timestamps[tf] >= timedelta(minutes=minutes):
                s, c, st = generate_signals(df, tf)
                last_signals[tf] = (s, c, st)
                last_timestamps[tf] = now
            else:
                s, c, st = last_signals[tf]

            timestamp_display = last_timestamps[tf].strftime("%H:%M:%S HST")
            countdown = format_countdown(last_timestamps[tf], minutes)
            label = f"{s} — {timestamp_display} — {countdown} left"

            output.extend([label, f"Confidence: {c}%", st])

            if save_logs:
                current_price = df["close"].iloc[-1]
                append_log(tf, s, c, st, current_price)

        return tuple(output)

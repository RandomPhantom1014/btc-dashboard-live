from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

previous_price = None
signal_times = {}

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
            html.Span(f"${price:,.2f}", style={"color": color})
        ])

    @app.callback(
        [Output(f"signal-{tf}", "children") for tf in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]] +
        [Output(f"confidence-{tf}", "children") for tf in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]] +
        [Output(f"strength-{tf}", "children") for tf in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]] +
        [Output(f"timestamp-{tf}", "children") for tf in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]] +
        [Output(f"countdown-{tf}", "children") for tf in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]],
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        global signal_times

        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        timeframes = {
            "5m": 5, "10m": 10, "15m": 15,
            "1h": 60, "6h": 360, "12h": 720, "24h": 1440
        }

        signal_outputs, confidence_outputs, strength_outputs, timestamps, countdowns = [], [], [], [], []
        price = df["close"].iloc[-1]

        for tf, minutes in timeframes.items():
            signal, confidence, strength = generate_signals(df, tf)
            signal_outputs.append(signal)
            confidence_outputs.append(f"Confidence: {confidence}%")
            strength_outputs.append(strength)

            # Track signal timestamp and countdown
            if tf not in signal_times or signal_times[tf]["signal"] != signal:
                signal_times[tf] = {"signal": signal, "time": now}

            sig_time = signal_times[tf]["time"]
            timestamps.append(f"Issued: {sig_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
            remaining = (sig_time + timedelta(minutes=minutes)) - now
            countdowns.append(f"⏳ {max(int(remaining.total_seconds()), 0)}s remaining")

            if save_logs:
                append_log(tf, signal, confidence, strength, price)

        return signal_outputs + confidence_outputs + strength_outputs + timestamps + countdowns

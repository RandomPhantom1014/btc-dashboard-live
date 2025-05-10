from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

# Track previous signal times
last_signal_times = {
    "5m": None,
    "10m": None,
    "15m": None,
    "1h": None,
    "6h": None,
    "12h": None,
    "24h": None
}

def register_callbacks(app):

    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_btc_price(n):
        price = fetch_live_btc_price()
        if price is None:
            return "Live BTC Price: Error"

        return html.Span(f"Live BTC Price: ${price:,.2f}", style={"fontWeight": "bold", "color": "#000"})

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
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        now = datetime.utcnow()
        timeframes = {
            "5m": timedelta(minutes=5),
            "10m": timedelta(minutes=10),
            "15m": timedelta(minutes=15),
            "1h": timedelta(hours=1),
            "6h": timedelta(hours=6),
            "12h": timedelta(hours=12),
            "24h": timedelta(hours=24)
        }

        signals = []
        confidences = []
        strengths = []
        timestamps = []
        countdowns = []

        for tf in timeframes:
            signal, confidence, strength = generate_signals(df, tf)
            signals.append(signal)
            confidences.append(f"Confidence: {confidence}%")
            strengths.append(strength)

            # Timestamp (HST)
            hst_now = datetime.now(pytz.timezone("Pacific/Honolulu"))
            hst_label = hst_now.strftime("%Y-%m-%d %H:%M:%S HST")

            # Store signal time
            last_time = last_signal_times.get(tf)
            if signal != "Wait":
                last_signal_times[tf] = now
                last_time = now

            # Countdown
            if last_time:
                expiry_time = last_time + timeframes[tf]
                remaining = expiry_time - now
                seconds_left = max(int(remaining.total_seconds()), 0)
                mins, secs = divmod(seconds_left, 60)
                countdown_label = f"{mins}m {secs}s left"
            else:
                countdown_label = "--"

            timestamps.append(f"Issued: {hst_label}")
            countdowns.append(countdown_label)

            if save_logs:
                current_price = df["close"].iloc[-1]
                append_log(tf, signal, confidence, strength, current_price)

        return signals + confidences + strengths + timestamps + countdowns

from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

# Internal state to track timestamps
last_timestamps = {}

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
        Output("signal-5m", "children"),
        Output("confidence-5m", "children"),
        Output("strength-5m", "children"),
        Output("timestamp-5m", "children"),
        Output("countdown-5m", "children"),

        Output("signal-10m", "children"),
        Output("confidence-10m", "children"),
        Output("strength-10m", "children"),
        Output("timestamp-10m", "children"),
        Output("countdown-10m", "children"),

        Output("signal-15m", "children"),
        Output("confidence-15m", "children"),
        Output("strength-15m", "children"),
        Output("timestamp-15m", "children"),
        Output("countdown-15m", "children"),

        Output("signal-1h", "children"),
        Output("confidence-1h", "children"),
        Output("strength-1h", "children"),
        Output("timestamp-1h", "children"),
        Output("countdown-1h", "children"),

        Output("signal-6h", "children"),
        Output("confidence-6h", "children"),
        Output("strength-6h", "children"),
        Output("timestamp-6h", "children"),
        Output("countdown-6h", "children"),

        Output("signal-12h", "children"),
        Output("confidence-12h", "children"),
        Output("strength-12h", "children"),
        Output("timestamp-12h", "children"),
        Output("countdown-12h", "children"),

        Output("signal-24h", "children"),
        Output("confidence-24h", "children"),
        Output("strength-24h", "children"),
        Output("timestamp-24h", "children"),
        Output("countdown-24h", "children"),

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
            "24h": 1440
        }

        output = []
        now = datetime.utcnow()
        hst = pytz.timezone("Pacific/Honolulu")

        for tf, minutes in timeframes.items():
            signal, conf, strength = generate_signals(df, tf)
            price = df["close"].iloc[-1]

            # Record HST timestamp for signal
            last_timestamps.setdefault(tf, now)
            last_timestamps[tf] = now  # update every cycle

            signal_time = last_timestamps[tf].astimezone(hst).strftime("%H:%M:%S HST")
            remaining = (last_timestamps[tf] + timedelta(minutes=minutes)) - now
            remaining_str = f"{int(remaining.total_seconds() // 60)}m {int(remaining.total_seconds() % 60)}s"

            if save_logs:
                append_log(tf, signal, conf, strength, price)

            output.extend([
                signal,
                f"Confidence: {conf}%",
                strength,
                f"Time: {signal_time}",
                f"⏳ {remaining_str}"
            ])

        return output

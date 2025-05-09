from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

# Global cache for signal timestamps
signal_times = {}

# Mapping from timeframe to timedelta for countdown
timeframe_to_delta = {
    "5m": timedelta(minutes=5),
    "10m": timedelta(minutes=10),
    "15m": timedelta(minutes=15),
    "1h": timedelta(hours=1),
    "6h": timedelta(hours=6),
    "12h": timedelta(hours=12),
    "24h": timedelta(hours=24),
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

        return html.Span([
            html.Span("Live BTC Price: ", style={"fontWeight": "bold", "marginRight": "8px"}),
            html.Span(f"${price:,.2f}", style={"color": "black", "fontWeight": "bold"})
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
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        timeframes = ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]

        signal_outputs = []
        confidence_outputs = []
        strength_outputs = []
        timestamp_outputs = []
        countdown_outputs = []

        now = datetime.now(pytz.timezone("Pacific/Honolulu"))

        for tf in timeframes:
            sig, conf, strength = generate_signals(df, tf)
            current_price = df["close"].iloc[-1]

            # Timestamp logic
            signal_times.setdefault(tf, now)
            if sig != "Wait":
                signal_times[tf] = now

            time_str = signal_times[tf].strftime("HST %H:%M:%S")
            countdown = max(signal_times[tf] + timeframe_to_delta[tf] - now, timedelta(seconds=0))
            countdown_str = f"⏳ {str(countdown).split('.')[0]} remaining"

            # Append data
            signal_outputs.append(sig)
            confidence_outputs.append(f"Confidence: {conf}%")
            strength_outputs.append(strength)
            timestamp_outputs.append(f"🕒 {time_str}")
            countdown_outputs.append(countdown_str)

            if save_logs:
                append_log(tf, sig, conf, strength, current_price)

        return (
            *signal_outputs,
            *confidence_outputs,
            *strength_outputs,
            *timestamp_outputs,
            *countdown_outputs
        )

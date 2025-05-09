# callbacks.py

from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

# To track timestamps per timeframe
signal_state = {}

def register_callbacks(app):
    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_btc_price(n):
        price = fetch_live_btc_price()
        if price is None:
            return "Live BTC Price: Error"
        return html.Div([
            html.Span("Live BTC Price: ", style={"fontWeight": "bold", "marginRight": "8px"}),
            html.Span(f"${price:,.2f}")
        ])

    @app.callback(
        [Output(f"signal-{t}", "children") for t in TIMEFRAMES] +
        [Output(f"confidence-{t}", "children") for t in TIMEFRAMES] +
        [Output(f"strength-{t}", "children") for t in TIMEFRAMES] +
        [Output(f"timestamp-{t}", "children") for t in TIMEFRAMES] +
        [Output(f"countdown-{t}", "children") for t in TIMEFRAMES],
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        now_utc = datetime.utcnow()
        now_hst = now_utc - timedelta(hours=10)

        signals, confidences, strengths, timestamps, countdowns = [], [], [], [], []

        for tf in TIMEFRAMES:
            signal, confidence, strength = generate_signals(df, tf)
            key = tf

            # Update timestamp if signal changes
            if signal_state.get(key, {}).get("signal") != signal:
                signal_state[key] = {
                    "signal": signal,
                    "time": now_hst
                }

            # Fallback if no prior signal yet
            signal_time = signal_state[key]["time"] if key in signal_state else now_hst
            duration = TIMEFRAME_MINUTES[tf]
            expire_time = signal_time + timedelta(minutes=duration)
            time_remaining = (expire_time - now_hst).total_seconds()
            minutes = int(time_remaining // 60)
            seconds = int(time_remaining % 60)
            countdown_str = f"{minutes}:{seconds:02d} left" if time_remaining > 0 else "Expired"

            # Save logs if enabled
            if save_logs:
                current_price = df["close"].iloc[-1]
                append_log(tf, signal, confidence, strength, current_price)

            signals.append(signal)
            confidences.append(f"Confidence: {confidence}%")
            strengths.append(strength)
            timestamps.append(f"Time: {signal_time.strftime('%H:%M:%S')} HST")
            countdowns.append(countdown_str)

        return signals + confidences + strengths + timestamps + countdowns


# Timeframes and durations in minutes
TIMEFRAMES = ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]
TIMEFRAME_MINUTES = {
    "5m": 5,
    "10m": 10,
    "15m": 15,
    "1h": 60,
    "6h": 360,
    "12h": 720,
    "24h": 1440
}

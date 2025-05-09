# callbacks.py

from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

# Store last signal times for countdown logic
last_signal_times = {"5m": None, "10m": None, "15m": None}

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
            html.Span(f"${price:,.2f}", style={"color": "#000", "fontWeight": "bold"})
        ])

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
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        timeframes = {"5m": 5, "10m": 10, "15m": 15}
        signal_outputs = []

        for tf, minutes in timeframes.items():
            signal, confidence, strength = generate_signals(df, tf)
            current_price = df["close"].iloc[-1]

            # Update and format timestamp in HST
            hst = pytz.timezone("Pacific/Honolulu")
            timestamp = datetime.now(hst).strftime("%Y-%m-%d %H:%M:%S")
            last_signal_times[tf] = datetime.now() if signal != "Wait" else last_signal_times[tf]

            # Countdown
            if last_signal_times[tf]:
                time_elapsed = datetime.now() - last_signal_times[tf]
                seconds_left = max(0, (minutes * 60) - int(time_elapsed.total_seconds()))
                countdown = f" | {seconds_left // 60}m {seconds_left % 60}s left"
            else:
                countdown = ""

            # Log if enabled
            if save_logs:
                append_log(tf, signal, confidence, strength, current_price)

            # Build output elements
            signal_label = html.Div([
                html.Span(signal, style={"fontWeight": "bold"}),
                html.Span(f" | HST: {timestamp}", style={"fontSize": "12px", "marginLeft": "8px"}),
                html.Span(countdown, style={"fontSize": "12px", "marginLeft": "4px"})
            ])

            confidence_label = f"Confidence: {confidence}%"
            strength_label = strength

            signal_outputs.extend([signal_label, confidence_label, strength_label])

        return tuple(signal_outputs)

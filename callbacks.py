# callbacks.py

from dash import html, Input, Output, State
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

previous_price = None
signal_times = {"5m": None, "10m": None, "15m": None}

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
                color = "limegreen"
            elif price < previous_price:
                color = "red"
        previous_price = price

        return html.Div([
            html.Span("Live BTC Price: ", style={"fontWeight": "bold", "marginRight": "8px"}),
            html.Span(f"${float(price):,.2f}", style={"color": color, "fontWeight": "bold", "fontSize": "36px"})
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
        global signal_times
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        now_hst = datetime.utcnow() - timedelta(hours=10)
        now = datetime.utcnow()

        outputs = []
        for tf, minutes in zip(["5m", "10m", "15m"], [5, 10, 15]):
            signal, confidence, strength = generate_signals(df, tf)
            current_price = df["close"].iloc[-1]

            # Set new signal time if it has changed
            if signal_times[tf] is None or signal != get_previous_signal(tf):
                signal_times[tf] = now
                set_previous_signal(tf, signal)

            # Format time and countdown
            issued_time = signal_times[tf]
            hst_time = issued_time - timedelta(hours=10)
            hst_str = hst_time.strftime("%H:%M:%S")
            remaining = minutes * 60 - int((now - issued_time).total_seconds())
            minutes_left = max(0, remaining // 60)
            seconds_left = max(0, remaining % 60)
            countdown = f"{minutes_left}:{seconds_left:02d} left"

            signal_label = html.Div([
                html.Span(signal, style={"fontWeight": "bold", "marginRight": "12px"}),
                html.Span(f"{hst_str} HST", style={"fontSize": "14px", "marginRight": "12px"}),
                html.Span(f"{countdown}", style={"fontSize": "14px", "fontWeight": "bold"})
            ], style={"backgroundColor": "#e0e0e0", "padding": "6px 12px", "borderRadius": "8px"})

            confidence_label = html.Div(f"Confidence: {confidence}%", className="confidence")
            strength_label = strength

            outputs.extend([signal_label, confidence_label, strength_label])

            if save_logs:
                append_log(tf, signal, confidence, strength, current_price)

        return tuple(outputs)

# These help track signal changes per timeframe
previous_signals = {"5m": None, "10m": None, "15m": None}

def get_previous_signal(tf):
    return previous_signals.get(tf)

def set_previous_signal(tf, signal):
    previous_signals[tf] = signal

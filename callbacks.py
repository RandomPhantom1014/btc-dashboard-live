from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

previous_price = None
last_timestamps = {"5m": None, "10m": None, "15m": None}

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
            html.Span("Live BTC Price: ", style={"fontWeight": "bold", "marginRight": "8px"}),
            html.Span(f"${price:,.2f}", style={"color": color})
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
        global last_timestamps
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        now = datetime.now(pytz.timezone("Pacific/Honolulu"))

        results = []
        for tf in ["5m", "10m", "15m"]:
            signal, conf, strength = generate_signals(df, tf)
            current_price = df["close"].iloc[-1]

            # Save signal timestamp
            if last_timestamps[tf] is None or signal != "Wait":
                last_timestamps[tf] = now

            # Compute time left for countdown
            delta = int(tf.replace("m", ""))
            if last_timestamps[tf]:
                seconds_passed = (now - last_timestamps[tf]).total_seconds()
                seconds_left = max(0, delta * 60 - int(seconds_passed))
            else:
                seconds_left = delta * 60

            minutes_left = seconds_left // 60
            seconds_display = seconds_left % 60
            countdown = f"{minutes_left}:{seconds_display:02d} left"

            timestamp_str = last_timestamps[tf].strftime("%H:%M:%S HST") if last_timestamps[tf] else "--:--:--"

            signal_label = html.Div([
                html.Span(signal, style={"fontWeight": "bold", "marginRight": "8px"}),
                html.Span(f"{timestamp_str} — {countdown}", style={"backgroundColor": "#e0e0e0", "padding": "3px 8px", "borderRadius": "6px"})
            ])

            if save_logs:
                append_log(tf, signal, conf, strength, current_price)

            results.extend([signal_label, f"Confidence: {conf}%", strength])

        return tuple(results)

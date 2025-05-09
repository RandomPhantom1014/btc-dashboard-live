from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from components.live_price import fetch_live_btc_price
from datetime import datetime, timedelta

# Store last signal times
last_signal_times = {}

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
        Output("signal-5m", "children"), Output("confidence-5m", "children"), Output("strength-5m", "children"),
        Output("timestamp-5m", "children"), Output("countdown-5m", "children"),

        Output("signal-10m", "children"), Output("confidence-10m", "children"), Output("strength-10m", "children"),
        Output("timestamp-10m", "children"), Output("countdown-10m", "children"),

        Output("signal-15m", "children"), Output("confidence-15m", "children"), Output("strength-15m", "children"),
        Output("timestamp-15m", "children"), Output("countdown-15m", "children"),

        Output("signal-1h", "children"), Output("confidence-1h", "children"), Output("strength-1h", "children"),
        Output("timestamp-1h", "children"), Output("countdown-1h", "children"),

        Output("signal-6h", "children"), Output("confidence-6h", "children"), Output("strength-6h", "children"),
        Output("timestamp-6h", "children"), Output("countdown-6h", "children"),

        Output("signal-12h", "children"), Output("confidence-12h", "children"), Output("strength-12h", "children"),
        Output("timestamp-12h", "children"), Output("countdown-12h", "children"),

        Output("signal-24h", "children"), Output("confidence-24h", "children"), Output("strength-24h", "children"),
        Output("timestamp-24h", "children"), Output("countdown-24h", "children"),

        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        timeframes = {
            "5m": 5, "10m": 10, "15m": 15,
            "1h": 60, "6h": 360, "12h": 720, "24h": 1440
        }

        outputs = []

        for tf, mins in timeframes.items():
            signal, confidence, strength = generate_signals(df, tf)
            now = datetime.utcnow()

            # Store/update signal time
            last_time = last_signal_times.get(tf, now)
            if tf not in last_signal_times or signal != "Wait":
                last_signal_times[tf] = now
                last_time = now

            # Countdown
            time_passed = (now - last_time).total_seconds()
            time_remaining = max(0, (mins * 60) - time_passed)
            mins_left = int(time_remaining // 60)
            secs_left = int(time_remaining % 60)
            countdown = f"{mins_left}m {secs_left}s left"

            timestamp_str = f"Signal @ {last_time.strftime('%H:%M:%S')} HST"

            # Log it
            if save_logs:
                current_price = df["close"].iloc[-1]
                append_log(tf, signal, confidence, strength, current_price)

            # Format return values
            outputs.extend([
                signal,
                f"Confidence: {confidence}%",
                strength,
                timestamp_str,
                countdown
            ])

        return tuple(outputs)

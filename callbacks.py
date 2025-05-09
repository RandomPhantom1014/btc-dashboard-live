from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

# Time tracker for each signal
signal_times = {
    "5m": None, "10m": None, "15m": None,
    "1h": None, "6h": None, "12h": None, "24h": None
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
        Output("signal-5m", "children"),
        Output("confidence-5m", "children"),
        Output("strength-5m", "children"),
        Output("signal-10m", "children"),
        Output("confidence-10m", "children"),
        Output("strength-10m", "children"),
        Output("signal-15m", "children"),
        Output("confidence-15m", "children"),
        Output("strength-15m", "children"),
        Output("signal-1h", "children"),
        Output("confidence-1h", "children"),
        Output("strength-1h", "children"),
        Output("signal-6h", "children"),
        Output("confidence-6h", "children"),
        Output("strength-6h", "children"),
        Output("signal-12h", "children"),
        Output("confidence-12h", "children"),
        Output("strength-12h", "children"),
        Output("signal-24h", "children"),
        Output("confidence-24h", "children"),
        Output("strength-24h", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        hst = pytz.timezone("Pacific/Honolulu")
        now = datetime.now(hst)

        results = []
        timeframes = ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]
        current_price = df["close"].iloc[-1]

        for tf in timeframes:
            signal, confidence, strength = generate_signals(df, tf)

            # Record timestamp
            if signal != "Wait":
                signal_times[tf] = now

            # Countdown timer
            duration_map = {
                "5m": 5, "10m": 10, "15m": 15,
                "1h": 60, "6h": 360, "12h": 720, "24h": 1440
            }
            countdown = ""
            if signal_times[tf]:
                elapsed = (now - signal_times[tf]).total_seconds()
                remaining = max(0, duration_map[tf] * 60 - elapsed)
                mins, secs = divmod(int(remaining), 60)
                countdown = f" ({mins:02d}:{secs:02d} left)"

            timestamp_str = signal_times[tf].strftime("%H:%M HST") if signal_times[tf] else "--:-- HST"
            signal_label = html.Div([
                html.Span(signal, style={"fontWeight": "bold"}),
                html.Span(f" | {timestamp_str}{countdown}", style={"fontSize": "12px", "marginLeft": "6px"})
            ])

            results.extend([signal_label, f"Confidence: {confidence}%", strength])

            # Optional logging
            if save_logs:
                append_log(tf, signal, confidence, strength, current_price)

        return tuple(results)

from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta
import pytz

# Store previous prices and timestamps per timeframe
previous_price = None
signal_times = {}

TIMEFRAMES = {
    "5m": 5,
    "10m": 10,
    "15m": 15,
    "1h": 60,
    "6h": 360,
    "12h": 720,
    "24h": 1440
}

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
            html.Span(f"${float(price):,.2f}", style={"color": color, "fontWeight": "bold"})
        ])

    @app.callback(
        [Output(f"signal-{tf}", "children") for tf in TIMEFRAMES] +
        [Output(f"confidence-{tf}", "children") for tf in TIMEFRAMES] +
        [Output(f"strength-{tf}", "children") for tf in TIMEFRAMES] +
        [Output(f"timestamp-{tf}", "children") for tf in TIMEFRAMES] +
        [Output(f"countdown-{tf}", "children") for tf in TIMEFRAMES],
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        global signal_times

        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        outputs = []
        now = datetime.now(pytz.timezone("Pacific/Honolulu"))

        for tf in TIMEFRAMES:
            signal, conf, strength = generate_signals(df, tf)
            current_price = df["close"].iloc[-1]

            # Save timestamp if new signal is issued
            if tf not in signal_times or signal_times[tf]["signal"] != signal:
                signal_times[tf] = {
                    "signal": signal,
                    "timestamp": now
                }

            issued = signal_times[tf]["timestamp"]
            countdown = max(0, TIMEFRAMES[tf]*60 - int((now - issued).total_seconds()))
            mins, secs = divmod(countdown, 60)

            outputs.append(signal)                                  # signal-pill
        for tf in TIMEFRAMES:
            signal, conf, _ = generate_signals(df, tf)
            outputs.append(f"Confidence: {conf}%")                 # confidence
        for tf in TIMEFRAMES:
            _, _, strength = generate_signals(df, tf)
            outputs.append(strength)                               # strength-meter
        for tf in TIMEFRAMES:
            if tf in signal_times:
                timestamp_str = signal_times[tf]["timestamp"].strftime("Issued: %H:%M:%S HST")
            else:
                timestamp_str = "Issued: --:--:-- HST"
            outputs.append(timestamp_str)                          # timestamp
        for tf in TIMEFRAMES:
            if tf in signal_times:
                countdown = max(0, TIMEFRAMES[tf]*60 - int((now - signal_times[tf]["timestamp"]).total_seconds()))
                mins, secs = divmod(countdown, 60)
                outputs.append(f"{mins:02}:{secs:02} left")         # countdown
            else:
                outputs.append("--:-- left")

            # Optional log
            signal, conf, strength = generate_signals(df, tf)
            if save_logs:
                append_log(tf, signal, conf, strength, current_price)

        return outputs

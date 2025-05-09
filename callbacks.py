from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from datetime import datetime, timedelta
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals

previous_price = None
signal_times = {}

def format_time(dt):
    return dt.strftime("%I:%M:%S %p HST")

def format_countdown(t_delta):
    minutes, seconds = divmod(int(t_delta.total_seconds()), 60)
    return f"{minutes:02}:{seconds:02}"

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

        return html.Span([
            html.Span("Live BTC Price: ", style={"fontWeight": "bold", "marginRight": "8px"}),
            html.Span(f"${float(price):,.2f}", style={"color": color, "fontWeight": "bold"})
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
        now = datetime.utcnow()
        timeframes = {
            "5m": 60,
            "10m": 60,
            "15m": 60,
            "1h": 300,
            "6h": 900,
            "12h": 3600,
            "24h": 3600
        }

        results = {}
        for tf, granularity in timeframes.items():
            df = get_btc_data(mode, granularity=granularity)
            if df is None or df.empty:
                return ["Error"] * 21

            signal, confidence, strength = generate_signals(df, tf)
            signal_times[tf] = now

            current_price = df["close"].iloc[-1]

            if save_logs:
                append_log(tf, signal, confidence, strength, current_price)

            issued_at = format_time(now)
            ends_in = format_countdown(timedelta(minutes=int(tf.replace("m", "").replace("h", "")) * (1 if "m" in tf else 60)))

            signal_label = html.Div([
                html.Span(signal, style={"fontWeight": "bold", "marginRight": "10px"}),
                html.Span(f"⏰ {issued_at}"),
                html.Br(),
                html.Span(f"⌛ {ends_in} remaining")
            ])

            results[tf] = (signal_label, f"Confidence: {confidence}%", strength)

        return (
            *results["5m"],
            *results["10m"],
            *results["15m"],
            *results["1h"],
            *results["6h"],
            *results["12h"],
            *results["24h"]
        )


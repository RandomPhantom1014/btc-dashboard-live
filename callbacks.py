# callbacks.py

from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta

previous_price = None
signal_timestamps = {"5m": None, "10m": None, "15m": None}

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
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        global signal_timestamps
        df = get_btc_data(mode)
        live_price = fetch_live_btc_price()

        if df is None or df.empty or live_price is None:
            raise PreventUpdate

        now = datetime.utcnow()

        def label_signal(timeframe, signal, conf, strength):
            ts = signal_timestamps[timeframe]
            if signal in ["Go Long", "Go Short"] or ts is None:
                signal_timestamps[timeframe] = now
                ts = now
            elapsed = now - ts
            remaining = {
                "5m": timedelta(minutes=5),
                "10m": timedelta(minutes=10),
                "15m": timedelta(minutes=15),
            }[timeframe] - elapsed

            min_left = max(0, int(remaining.total_seconds() // 60))
            sec_left = max(0, int(remaining.total_seconds() % 60))

            return html.Div([
                html.Div(signal, style={"fontWeight": "bold"}),
                html.Div(f"HST: {ts.strftime('%H:%M:%S')}", style={"fontSize": "13px", "marginTop": "3px"}),
                html.Div(f"{min_left:02d}:{sec_left:02d} left", style={"fontSize": "13px"})
            ])

        s5, c5, st5 = generate_signals(df, "5m", live_price)
        s10, c10, st10 = generate_signals(df, "10m", live_price)
        s15, c15, st15 = generate_signals(df, "15m", live_price)

        current_price = df["close"].iloc[-1]

        if save_logs:
            append_log("5m", s5, c5, st5, current_price)
            append_log("10m", s10, c10, st10, current_price)
            append_log("15m", s15, c15, st15, current_price)

        return (
            label_signal("5m", s5, c5, st5), f"Confidence: {c5}%", st5,
            label_signal("10m", s10, c10, st10), f"Confidence: {c10}%", st10,
            label_signal("15m", s15, c15, st15), f"Confidence: {c15}%", st15
        )

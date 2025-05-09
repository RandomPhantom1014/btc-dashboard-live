# callbacks.py

from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals

previous_price = None

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
            "Live BTC Price: ",
            {"type": "span", "props": {
                "style": {"color": color, "fontWeight": "bold"},
                "children": f"${float(price):,.2f}"
            }}
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
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        s5, c5, st5 = generate_signals(df, "5m")
        s10, c10, st10 = generate_signals(df, "10m")
        s15, c15, st15 = generate_signals(df, "15m")

        current_price = df["close"].iloc[-1]

        if save_logs:
            append_log("5m", s5, c5, st5, current_price)
            append_log("10m", s10, c10, st10, current_price)
            append_log("15m", s15, c15, st15, current_price)

        return (
            s5, f"Confidence: {c5}%", st5,
            s10, f"Confidence: {c10}%", st10,
            s15, f"Confidence: {c15}%", st15
        )

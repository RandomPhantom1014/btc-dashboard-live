# callbacks.py

from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from components.chart import render_candlestick_chart
from components.signals_logic import get_signal
from utils.data import get_btc_data, append_log

def register_callbacks(app):
    # Track previous price for color comparison
    previous_price = {"value": None}

    # Update Live BTC Price Display
    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals"),
        State("signal-mode", "value")
    )
    def update_btc_price(n, mode):
        if mode == "backtest":
            return "Backtest Mode: No Live Price"

        price = fetch_live_btc_price()
        if price is None:
            return "Live BTC Price: Error"

        color = "white"
        if previous_price["value"] is not None:
            if price > previous_price["value"]:
                color = "limegreen"
            elif price < previous_price["value"]:
                color = "red"
        previous_price["value"] = price

        return [
            f"Live BTC Price: ",
            {
                "type": "span",
                "props": {
                    "style": {"color": color, "fontWeight": "bold"},
                    "children": f"${price:,.2f}"
                }
            }
        ]

    # Update Chart + Signals
    @app.callback(
        Output("candlestick-chart", "figure"),
        Output("five-min-signal", "children"),
        Output("ten-min-signal", "children"),
        Output("fifteen-min-signal", "children"),
        Input("interval-component", "n_intervals"),
        State("signal-mode", "value"),
        State("save-logs-toggle", "value")
    )
    def update_dashboard(n, mode, save_logs):
        df = get_btc_data(mode)
        if df.empty:
            raise PreventUpdate

        # Generate chart
        chart = render_candlestick_chart(df)

        # Generate signals
        signal_5m, conf_5m, strength_5m = get_signal(df, 5)
        signal_10m, conf_10m, strength_10m = get_signal(df, 10)
        signal_15m, conf_15m, strength_15m = get_signal(df, 15)

        # Save logs if toggle is on and in live mode
        if save_logs and mode == "live":
            price_now = df["close"].iloc[-1]
            append_log("5m", signal_5m, conf_5m, strength_5m, price_now)
            append_log("10m", signal_10m, conf_10m, strength_10m, price_now)
            append_log("15m", signal_15m, conf_15m, strength_15m, price_now)

        return chart, (
            f"{signal_5m} | Confidence: {conf_5m}% | Strength: {strength_5m}/10",
            f"{signal_10m} | Confidence: {conf_10m}% | Strength: {strength_10m}/10",
            f"{signal_15m} | Confidence: {conf_15m}% | Strength: {strength_15m}/10"
        )


# callbacks.py

from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from components.chart import render_candlestick_chart
from components.indicators import render_indicators
from components.signals_logic import generate_signal
from utils.data import get_btc_data

previous_price = None

def register_callbacks(app):
    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_btc_price(n_intervals, mode):
        global previous_price
        df = get_btc_data(mode)
        if df.empty:
            return "Live BTC Price: Error"
        price = df["close"].iloc[-1]

        color = "white"
        if previous_price is not None:
            if price > previous_price:
                color = "limegreen"
            elif price < previous_price:
                color = "red"
        previous_price = price

        return [
            "Live BTC Price: ",
            {
                "type": "span",
                "props": {
                    "style": {"color": color, "fontWeight": "bold"},
                    "children": f"${price:,.2f}"
                }
            }
        ]

    @app.callback(
        Output("candlestick-chart", "figure"),
        Output("indicators-container", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_charts(n, mode):
        df = get_btc_data(mode)
        if df.empty:
            raise PreventUpdate
        return render_candlestick_chart(df), render_indicators(df)

    @app.callback(
        Output("signal-5m", "children"),
        Output("confidence-5m", "children"),
        Output("strength-5m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_signal_5m(n, mode):
        df = get_btc_data(mode)
        signal, confidence, strength = generate_signal(df, "5m")
        return signal, f"Confidence: {confidence}", strength

    @app.callback(
        Output("signal-10m", "children"),
        Output("confidence-10m", "children"),
        Output("strength-10m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_signal_10m(n, mode):
        df = get_btc_data(mode)
        signal, confidence, strength = generate_signal(df, "10m")
        return signal, f"Confidence: {confidence}", strength

    @app.callback(
        Output("signal-15m", "children"),
        Output("confidence-15m", "children"),
        Output("strength-15m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_signal_15m(n, mode):
        df = get_btc_data(mode)
        signal, confidence, strength = generate_signal(df, "15m")
        return signal, f"Confidence: {confidence}", strength

    @app.callback(
        Output("theme-toggle", "value"),
        Input("theme-toggle", "value"),
        prevent_initial_call=True
    )
    def sync_theme_toggle(value):
        return value

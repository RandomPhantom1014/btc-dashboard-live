# callbacks.py

from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from components.chart import render_candlestick_chart
from components.indicators import render_indicators
from utils.data import get_btc_data  # Make sure this returns a clean DataFrame

previous_price = None  # To track price changes between intervals

def register_callbacks(app):

    # ========== LIVE BTC PRICE ==========

    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_btc_price(n_intervals):
        global previous_price
        current_price = fetch_live_btc_price()

        if current_price is None:
            return "Live BTC Price: Error"

        color = "white"
        if previous_price is not None:
            if current_price > previous_price:
                color = "limegreen"
            elif current_price < previous_price:
                color = "red"
        previous_price = current_price

        return [
            f"Live BTC Price: ",
            {
                "type": "span",
                "props": {
                    "style": {"color": color, "fontWeight": "bold"},
                    "children": f"${current_price:,.2f}"
                }
            }
        ]

    # ========== CHART + INDICATORS ==========

    @app.callback(
        Output("candlestick-chart", "figure"),
        Output("indicators-container", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_chart_and_indicators(n_intervals):
        df = get_btc_data()
        if df is None or df.empty:
            raise PreventUpdate

        chart_fig = render_candlestick_chart(df)
        indicators = render_indicators(df)

        return chart_fig, indicators

    # ========== SIGNAL PLACEHOLDER CALLBACKS ==========

    @app.callback(
        Output("signal-5m", "children"),
        Output("confidence-5m", "children"),
        Output("strength-5m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_signal_5m(n, mode):
        signal = "Go Long" if n % 2 == 0 else "Go Short"
        confidence = f"Confidence: {85 + (n % 5)}%"
        strength = f"Strength: {(n % 10) + 1}/10"
        return signal, confidence, strength

    @app.callback(
        Output("signal-10m", "children"),
        Output("confidence-10m", "children"),
        Output("strength-10m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_signal_10m(n, mode):
        signal = "Wait" if n % 3 == 0 else "Go Long"
        confidence = f"Confidence: {75 + (n % 10)}%"
        strength = f"Strength: {(n % 5) + 3}/10"
        return signal, confidence, strength

    @app.callback(
        Output("signal-15m", "children"),
        Output("confidence-15m", "children"),
        Output("strength-15m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_signal_15m(n, mode):
        signal = "Go Short" if n % 4 == 0 else "Wait"
        confidence = f"Confidence: {65 + (n % 15)}%"
        strength = f"Strength: {(n % 7) + 2}/10"
        return signal, confidence, strength


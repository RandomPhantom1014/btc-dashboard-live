# callbacks.py

from dash import Input, Output, State
from components.live_price import fetch_live_btc_price

previous_price = None  # To track price changes between intervals

def register_callbacks(app):

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

    # Placeholder: Update signals if desired
    # @app.callback(
    #     Output("signal-5m", "children"),
    #     Output("confidence-5m", "children"),
    #     Input("interval-component", "n_intervals"),
    #     State("mode-toggle", "value")
    # )
    # def update_signal_5m(n, mode):
    #     return "Go Long", "Confidence: 87%"

    # Repeat similar logic for 10m and 15m signals if needed

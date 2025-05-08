# callbacks.py

from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from components.chart import render_candlestick_chart
from components.indicators import render_indicators
from utils.data import get_btc_data  # Make sure this returns a clean DataFrame

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

    # 🔁 Update Chart and Indicators on Interval
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

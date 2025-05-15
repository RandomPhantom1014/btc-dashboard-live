from dash import Input, Output
from utils.data import get_latest_price, get_indicator_data
from utils.signals_logic import generate_signals_for_timeframe

def register_callbacks(app):
    timeframes = ["5m", "10m", "15m", "1h", "6h"]

    @app.callback(
        Output("xrp-price-text", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_price(n):
        price = get_latest_price()
        return f"XRP Price: ${price}"

    for tf in timeframes:
        app.callback(
            Output(f"{tf}-signal", "children"),
            Input("interval-component", "n_intervals")
        )(generate_signals_for_timeframe(tf))

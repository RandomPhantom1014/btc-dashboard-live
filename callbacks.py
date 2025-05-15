from dash import callback, Output, Input
from utils.data import get_latest_price, get_indicator_data
from utils.signals_logic import generate_signals_for_timeframe

timeframes = {
    '5m': 5,
    '10m': 10,
    '15m': 15,
    '1h': 60,
    '6h': 360
}

def register_callbacks(app):
    # Price update callback
    @callback(
        Output("btc-price-text", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_price(_):
        price = get_latest_price()
        return f"XRP Price: ${price:.4f}"

    # Signal update callbacks
    for tf_label, tf_minutes in timeframes.items():
        @app.callback(
            Output(f"{tf_label}-signal", "children"),
            Output(f"{tf_label}-confidence", "children"),
            Output(f"{tf_label}-signal", "className"),
            Output(f"{tf_label}-timestamp", "children"),
            Output(f"{tf_label}-countdown", "children"),
            Input("interval-component", "n_intervals"),
            prevent_initial_call="initial_duplicate"
        )
        def update_signal(_, tf_label=tf_label, tf_minutes=tf_minutes):
            df = get_indicator_data()
            signal_data = generate_signals_for_timeframe(df, tf_minutes)
            signal = signal_data["signal"]
            confidence = signal_data["confidence"]
            timestamp = signal_data["timestamp"]
            countdown = signal_data["countdown"]

            pill_color = {
                "Go Long": "green-pill",
                "Go Short": "red-pill",
                "Wait": "gray-pill"
            }.get(signal, "gray-pill")

            return signal, confidence, pill_color, timestamp, countdown


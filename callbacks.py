import requests
from dash import Input, Output
from datetime import datetime, timedelta
from utils.signals_logic import get_signal_for_interval
from utils.data import get_coinbase_price

def register_callbacks(app):
    @app.callback(
        Output('xrp-price-text', 'children'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_price(n):
        price = get_coinbase_price("XRP-USD")
        if price:
            return f"XRP Price: ${price:.4f}"
        else:
            return "XRP Price: Unavailable"

    for interval_id, minutes in [('5m', 5), ('10m', 10), ('15m', 15), ('1h', 60), ('6h', 360)]:
        @app.callback(
            Output(f'signal-{interval_id}', 'children'),
            [Input('interval-component', 'n_intervals')],
        )
        def update_signal(n, interval_id=interval_id, minutes=minutes):
            now = datetime.utcnow()
            end_time = now + timedelta(minutes=minutes)
            price = get_coinbase_price("XRP-USD")
            if price is None:
                return ["No Data", "N/A", "N/A"]

            signal, confidence = get_signal_for_interval(minutes, "XRP-USD", price)
            return [
                f"{signal}",
                f"Confidence: {confidence}%",
                f"{now.strftime('%Y-%m-%d %H:%M:%S')} UTC | Expires in: {minutes}m 0s"
            ]

from dash import Output, Input
from dash.dependencies import ALL
from datetime import datetime, timedelta
from utils.data import get_latest_price, get_indicator_data
from utils.signals_logic import generate_signals_for_timeframe
import pytz

def register_callbacks(app):
    @app.callback(
        Output('xrp-price-text', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def update_xrp_price(n):
        price = get_latest_price()
        return f"XRP Price: ${price:.4f}"

    @app.callback(
        [Output(f"{interval}-signal", "children") for interval in ['5m', '10m', '15m', '1h', '6h']] +
        [Output(f"{interval}-confidence", "children") for interval in ['5m', '10m', '15m', '1h', '6h']] +
        [Output(f"{interval}-signal", "className") for interval in ['5m', '10m', '15m', '1h', '6h']] +
        [Output(f"{interval}-timestamp", "children") for interval in ['5m', '10m', '15m', '1h', '6h']] +
        [Output(f"{interval}-countdown", "children") for interval in ['5m', '10m', '15m', '1h', '6h']],
        Input('interval-component', 'n_intervals')
    )
    def update_signals(n):
        now = datetime.now(pytz.timezone('US/Hawaii'))
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S HST")

        prices, rsi, macd, volume = get_indicator_data()
        signals = generate_signals_for_timeframe(prices, rsi, macd, volume)

        signal_texts = []
        confidences = []
        classes = []
        timestamps = []
        countdowns = []

        countdown_map = {
            '5m': 5,
            '10m': 10,
            '15m': 15,
            '1h': 60,
            '6h': 360
        }

        for interval in ['5m', '10m', '15m', '1h', '6h']:
            data = signals.get(interval, {})
            signal = data.get('signal', 'Wait')
            confidence = data.get('confidence', 0)

            signal_texts.append(signal)
            confidences.append(f"{confidence}%")

            if signal == "Go Long":
                classes.append("signal-pill long")
            elif signal == "Go Short":
                classes.append("signal-pill short")
            else:
                classes.append("signal-pill wait")

            timestamps.append(timestamp)
            minutes = countdown_map.get(interval, 5)
            expires_at = now + timedelta(minutes=minutes)
            countdowns.append(expires_at.strftime("%H:%M:%S"))

        return signal_texts + confidences + classes + timestamps + countdowns

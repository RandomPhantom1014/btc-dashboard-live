from dash import Input, Output
from datetime import datetime, timedelta
from utils.data import fetch_live_data
from utils.signals_logic import generate_signals
import pytz

timeframes = ['5m', '10m', '15m', '1h', '6h']

def register_callbacks(app):
    for tf in timeframes:
        app.callback(
            Output(f'{tf}-signal-text', 'children'),
            Output(f'{tf}-confidence', 'children'),
            Output(f'{tf}-strength-meter', 'className'),
            Output(f'{tf}-timestamp', 'children'),
            Output(f'{tf}-countdown', 'children'),
            Input('interval-component', 'n_intervals')
        )(make_callback(tf))

    @app.callback(
        Output('btc-price-text', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def update_btc_price(n):
        df = fetch_live_data()
        price = df['close'].iloc[-1]
        return f"${price:,.2f}"

def make_callback(timeframe):
    def callback(n):
        df = fetch_live_data()
        signal_data = generate_signals(df, timeframe)

        hst = pytz.timezone("Pacific/Honolulu")
        timestamp = datetime.now(hst).strftime('%Y-%m-%d %H:%M:%S HST')

        expiry_map = {
            '5m': 5, '10m': 10, '15m': 15, '1h': 60, '6h': 360
        }
        expiry = datetime.now() + timedelta(minutes=expiry_map[timeframe])
        countdown = str(expiry - datetime.now()).split('.')[0]

        return (
            signal_data['signal'],
            f"Confidence: {signal_data['confidence']}%",
            signal_data['strength_class'],
            f"Updated: {timestamp}",
            f"Expires in: {countdown}"
        )
    return callback

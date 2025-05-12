from dash import Output, Input
from utils.data import fetch_live_data
from utils.signals_logic import generate_signals
import pytz
from datetime import datetime, timedelta

def register_callbacks(app):
    timeframes = ['5m', '10m', '15m', '1h', '6h']

    # Live BTC Price
    @app.callback(
        Output('btc-price-text', 'children'),
        Input('interval-btc', 'n_intervals')
    )
    def update_btc_price(n):
        try:
            df = fetch_live_data()
            if df.empty or 'close' not in df.columns:
                return "BTC Price: Unavailable"
            return f"${df['close'].iloc[-1]:,.2f}"
        except Exception as e:
            return f"Error: {str(e)}"

    # Signal Updates
    for tf in timeframes:
        @app.callback(
            Output(f'{tf}-signal', 'children'),
            Output(f'{tf}-confidence', 'children'),
            Output(f'{tf}-signal', 'className'),
            Output(f'{tf}-timestamp', 'children'),
            Output(f'{tf}-countdown', 'children'),
            Input('interval-slow', 'n_intervals'),
        )
        def update_signal(n, tf=tf):
            df = fetch_live_data()
            if df.empty:
                return "No Data", "", "pill neutral", "N/A", "N/A"

            result = generate_signals(df, tf)
            now = datetime.now(pytz.timezone("Pacific/Honolulu"))
            timestamp = now.strftime('%Y-%m-%d %I:%M:%S %p')

            # Countdown logic
            if tf.endswith('m'):
                total_minutes = int(tf.replace('m', ''))
            else:
                total_minutes = int(tf.replace('h', '')) * 60
            expiry_time = now + timedelta(minutes=total_minutes)
            remaining = expiry_time - now
            countdown = f"{remaining.seconds // 60}m {remaining.seconds % 60}s"

            return (
                result['signal'],
                f"{result['confidence']}%",
                f"pill {result['strength_class']}",
                timestamp,
                countdown
            )

from dash import Output, Input
from utils.data import fetch_live_data
from utils.signals_logic import generate_signals
import pytz
from datetime import datetime

def register_callbacks(app):
    timeframes = ['5m', '10m', '15m', '1h', '6h']

    for tf in timeframes:
        @app.callback(
            Output(f'{tf}-signal', 'children'),
            Output(f'{tf}-confidence', 'children'),
            Output(f'{tf}-pill', 'className'),
            Output(f'{tf}-timestamp', 'children'),
            Output(f'{tf}-countdown', 'children'),
            Input('interval-slow', 'n_intervals'),
        )
        def update_signals(n, tf=tf):
            df = fetch_live_data()
            if df.empty:
                return "No Data", "", "pill neutral", "N/A", "N/A"

            result = generate_signals(df, tf)
            now = datetime.now(pytz.timezone("Pacific/Honolulu"))
            timestamp = now.strftime('%Y-%m-%d %I:%M:%S %p')

            if tf.endswith('m'):
                minutes = int(tf.replace('m', ''))
            elif tf.endswith('h'):
                minutes = int(tf.replace('h', '')) * 60
            else:
                minutes = 5

            seconds = minutes * 60
            countdown = f"{seconds // 60}m {seconds % 60}s"

            return (
                result['signal'],
                f"{result['confidence']}%",
                f"pill {result['strength_class']}",
                timestamp,
                countdown
            )

    # Fast BTC price update every 5 seconds
    @app.callback(
        Output('btc-price-text', 'children'),
        Input('interval-btc', 'n_intervals')
    )
    def update_btc_price(n):
        try:
            df = fetch_live_data()
            if df.empty or 'close' not in df.columns:
                return "Price unavailable"
            price = df['close'].iloc[-1]
            return f"${price:,.2f}"
        except Exception as e:
            print(f"[ERROR - update_btc_price] {e}")
            return "Error fetching price"

from dash import Input, Output
from datetime import datetime, timedelta
from utils.data import fetch_live_data
from utils.signals_logic import generate_signals
import pytz

timeframes = ['5m', '10m', '15m', '1h', '6h']
signal_expiry_times = {tf: None for tf in timeframes}

def register_callbacks(app):
    # Signal + timestamp updates (every 30s)
    for tf in timeframes:
        app.callback(
            Output(f'{tf}-signal-text', 'children'),
            Output(f'{tf}-confidence', 'children'),
            Output(f'{tf}-strength-meter', 'className'),
            Output(f'{tf}-timestamp', 'children'),
            Input('interval-slow', 'n_intervals')
        )(make_signal_callback(tf))

    # Countdown refresh (every 1s)
    for tf in timeframes:
        app.callback(
            Output(f'{tf}-countdown', 'children'),
            Input('interval-fast', 'n_intervals')
        )(make_countdown_callback(tf))

    # BTC price update (every 30s)
    @app.callback(
        Output('btc-price-text', 'children'),
        Input('interval-slow', 'n_intervals')
    )
    def update_btc_price(n):
        try:
            df = fetch_live_data()
            if df.empty:
                return "Price unavailable"
            price = df['close'].iloc[-1]
            return f"${price:,.2f}"
        except Exception as e:
            print(f"[ERROR - update_btc_price] {e}")
            return "Error fetching price"

def make_signal_callback(timeframe):
    def callback(n):
        try:
            df = fetch_live_data()
            if df.empty:
                return "No data", "", "neutral", ""

            signal_data = generate_signals(df, timeframe)

            hst = pytz.timezone("Pacific/Honolulu")
            now = datetime.now(hst)
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S HST')

            expiry_map = {'5m': 5, '10m': 10, '15m': 15, '1h': 60, '6h': 360}
            signal_expiry_times[timeframe] = now + timedelta(minutes=expiry_map[timeframe])

            return (
                signal_data['signal'],
                f"Confidence: {signal_data['confidence']}%",
                signal_data['strength_class'],
                f"Updated: {timestamp}"
            )
        except Exception as e:
            print(f"[ERROR - signal callback {timeframe}] {e}")
            return "Error", "", "neutral", ""
    return callback

def make_countdown_callback(timeframe):
    def callback(n):
        try:
            expiry = signal_expiry_times.get(timeframe)
            if expiry is None:
                return "Expires in: --:--"
            now = datetime.now(pytz.timezone("Pacific/Honolulu"))
            remaining = expiry - now
            if remaining.total_seconds() <= 0:
                return "Expires in: 00:00"
            countdown = str(remaining).split('.')[0]
            return f"Expires in: {countdown}"
        except Exception as e:
            print(f"[ERROR - countdown {timeframe}] {e}")
            return "Expires in: --:--"
    return callback


from dash import Output, Input, State, callback_context
from utils.signals_logic import generate_signal
from utils.data import get_live_price
import datetime
from app import app

# List of all timeframes to loop through
timeframes = ['5m', '10m', '15m', '1h', '6h']

@app.callback(
    Output('xrp-price-text', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_xrp_price(n):
    price = get_live_price()
    return f"${price:.4f}"

# Dynamically create callbacks for each timeframe
for tf in timeframes:
    @app.callback(
        Output(f'{tf}-signal', 'children'),
        Output(f'{tf}-confidence', 'children'),
        Output(f'{tf}-signal', 'className'),
        Output(f'{tf}-timestamp', 'children'),
        Output(f'{tf}-countdown', 'children'),
        Input('interval-component', 'n_intervals'),
        State('mode-toggle', 'value'),
        prevent_initial_call='initial_duplicate'
    )
    def update_signals(n, mode, tf=tf):
        signal_data = generate_signal(tf, mode)
        signal = signal_data['signal']
        confidence = signal_data['confidence']
        color = f"pill pill-{signal.lower()}"
        now = datetime.datetime.now().strftime("%H:%M:%S HST")

        if 'expires_in' in signal_data:
            countdown = f"{signal_data['expires_in']}s"
        else:
            countdown = "N/A"

        return signal, f"{confidence}%", color, now, countdown

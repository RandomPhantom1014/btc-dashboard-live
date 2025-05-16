from dash import Output, Input, html
from utils.data import get_live_price
from utils.signals_logic import generate_short_term_signals, generate_long_term_signals
from datetime import datetime
import pytz

def format_signal_output(label, signal, confidence, strength, last_update):
    hst_time = last_update.astimezone(pytz.timezone("US/Hawaii")).strftime('%I:%M:%S %p')
    countdown_id = f'countdown-{label.lower()}'

    return html.Div([
        html.Div([
            html.Span(f"{label}: ", style={"fontWeight": "bold"}),
            html.Span(signal or "No Signal", className="signal-pill"),
            html.Span(f"{confidence}% confidence", style={"marginLeft": "10px"}),
            html.Span(f"({strength})", style={"marginLeft": "10px"}),
            html.Span(f"Last updated: {hst_time}", style={"marginLeft": "15px", "fontStyle": "italic"}),
            html.Span(id=countdown_id, style={"marginLeft": "15px", "color": "orange"}),
        ])
    ])

@app.callback(Output("signal-5m", "children"), Input("interval-component", "n_intervals"))
def update_signal_5m(n):
    price = get_live_price()
    rsi, macd, volume = 52, 1, 1200000  # Replace with real logic
    signal, confidence, strength = generate_short_term_signals(price, rsi, macd, volume)
    return format_signal_output("5M", signal, confidence, strength, datetime.now(pytz.utc))

@app.callback(Output("signal-10m", "children"), Input("interval-component", "n_intervals"))
def update_signal_10m(n):
    price = get_live_price()
    rsi, macd, volume = 50, 0.5, 1000000
    signal, confidence, strength = generate_short_term_signals(price, rsi, macd, volume)
    return format_signal_output("10M", signal, confidence, strength, datetime.now(pytz.utc))

@app.callback(Output("signal-15m", "children"), Input("interval-component", "n_intervals"))
def update_signal_15m(n):
    price = get_live_price()
    rsi, macd, volume = 48, -0.5, 950000
    signal, confidence, strength = generate_short_term_signals(price, rsi, macd, volume)
    return format_signal_output("15M", signal, confidence, strength, datetime.now(pytz.utc))

@app.callback(Output("signal-1h", "children"), Input("interval-component", "n_intervals"))
def update_signal_1h(n):
    price = get_live_price()
    rsi, macd, volume = 61, 1.2, 2200000
    signal, confidence, strength = generate_long_term_signals(price, rsi, macd, volume)
    return format_signal_output("1H", signal, confidence, strength, datetime.now(pytz.utc))

@app.callback(Output("signal-6h", "children"), Input("interval-component", "n_intervals"))
def update_signal_6h(n):
    price = get_live_price()
    rsi, macd, volume = 58, 0.9, 2100000
    signal, confidence, strength = generate_long_term_signals(price, rsi, macd, volume)
    return format_signal_output("6H", signal, confidence, strength, datetime.now(pytz.utc))

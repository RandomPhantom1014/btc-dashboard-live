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

@app.callback(Output("live-price", "children"), Input("interval-component", "n_intervals"))
def update_price(n):
    price = get_live_price()
    return f"Live XRP Price: ${price:.4f}"

@app.callback(Output("signal-5m", "children"), Input("interval-component", "n_intervals"))
def update_signal_5m(n):
    price = get_live_price()
    signal, confidence, strength = generate_short_term_signals(price, 56, 0.9, 1000000)
    return format_signal_output("5M", signal, confidence, strength, datetime.now(pytz.utc))

@app.callback(Output("signal-10m", "children"), Input("interval-component", "n_intervals"))
def update_signal_10m(n):
    price = get_live_price()
    signal, confidence, strength = generate_short_term_signals(price, 50, 0.3, 950000)
    return format_signal_output("10M", signal, confidence, strength, datetime.now(pytz.utc))

@app.callback(Output("signal-15m", "children"), Input("interval-component", "n_intervals"))
def update_signal_15m(n):
    price = get_live_price()
    signal, confidence, strength = generate_short_term_signals(price, 48, -0.2, 870000)
    return format_signal_output("15M", signal, confidence, strength, datetime.now(pytz.utc))

@app.callback(Output("signal-1h", "children"), Input("interval-component", "n_intervals"))
def update_signal_1h(n):
    price = get_live_price()
    signal, confidence, strength = generate_long_term_signals(price, 61, 1.2, 2100000)
    return format_signal_output("1H", signal, confidence, strength, datetime.now(pytz.utc))

@app.callback(Output("signal-6h", "children"), Input("interval-component", "n_intervals"))
def update_signal_6h(n):
    price = get_live_price()
    signal, confidence, strength = generate_long_term_signals(price, 59, 0.6, 2000000)
    return format_signal_output("6H", signal, confidence, strength, datetime.now(pytz.utc))

from dash import Output, Input, html
from utils.data import get_live_price
from utils.signals_logic import generate_short_term_signals, generate_long_term_signals
from datetime import datetime
import pytz

def get_pill_class(strength):
    if strength == "Strong":
        return "strong-pill"
    elif strength == "Medium":
        return "medium-pill"
    else:
        return "weak-pill"

def format_signal(label, signal, confidence, strength):
    now = datetime.now(pytz.utc)
    hst_time = now.astimezone(pytz.timezone("US/Hawaii")).strftime('%I:%M:%S %p')
    pill_class = f"signal-pill {get_pill_class(strength)}"
    countdown_id = f"countdown-{label.lower()}"

    return html.Div([
        html.Span(f"{label}: ", style={"fontWeight": "bold"}),
        html.Span(signal, className=pill_class),
        html.Span(f" {confidence}% confidence", style={"marginLeft": "10px"}),
        html.Span(f"({strength})", style={"marginLeft": "10px"}),
        html.Span(f"Last updated: {hst_time}", style={"marginLeft": "15px"}),
        html.Span(id=countdown_id, style={"marginLeft": "10px", "color": "orange"}),
    ])

def register_callbacks(app):
    @app.callback(Output("live-price", "children"), Input("interval-component", "n_intervals"))
    def update_price(n):
        price = get_live_price()
        return f"Live XRP Price: ${price:.4f}"

    @app.callback(Output("signal-5m", "children"), Input("interval-component", "n_intervals"))
    def update_signal_5m(n):
        price = get_live_price()
        signal, confidence, strength = generate_short_term_signals(price, 56, 0.5, 1000000)
        return format_signal("5M", signal, confidence, strength)

    @app.callback(Output("signal-10m", "children"), Input("interval-component", "n_intervals"))
    def update_signal_10m(n):
        price = get_live_price()
        signal, confidence, strength = generate_short_term_signals(price, 50, 0.2, 950000)
        return format_signal("10M", signal, confidence, strength)

    @app.callback(Output("signal-15m", "children"), Input("interval-component", "n_intervals"))
    def update_signal_15m(n):
        price = get_live_price()
        signal, confidence, strength = generate_short_term_signals(price, 48, -0.2, 870000)
        return format_signal("15M", signal, confidence, strength)

    @app.callback(Output("signal-1h", "children"), Input("interval-component", "n_intervals"))
    def update_signal_1h(n):
        price = get_live_price()
        signal, confidence, strength = generate_long_term_signals(price, 61, 1.1, 2000000)
        return format_signal("1H", signal, confidence, strength)

    @app.callback(Output("signal-6h", "children"), Input("interval-component", "n_intervals"))
    def update_signal_6h(n):
        price = get_live_price()
        signal, confidence, strength = generate_long_term_signals(price, 59, 0.6, 1800000)
        return format_signal("6H", signal, confidence, strength)

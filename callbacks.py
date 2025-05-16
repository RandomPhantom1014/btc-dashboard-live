from dash import Output, Input, html
from utils.data import get_live_price
from utils.signals_logic import generate_short_term_signals, generate_long_term_signals
from datetime import datetime
import pytz

def format_signal(label, signal, confidence, strength, last_update):
    hst_time = last_update.astimezone(pytz.timezone("US/Hawaii")).strftime('%I:%M:%S %p')
    countdown_id = f'countdown-{label.lower()}'

    return html.Div([
        html.Span(f"{label}: ", style={"fontWeight": "bold"}),
        html.Span(signal, className="signal-pill"),
        html.Span(f"{confidence}% confidence", style={"marginLeft": "10px"}),
        html.Span(f"({strength})", style={"marginLeft": "10px"}),
        html.Span(f"Last updated: {hst_time}", style={"marginLeft": "15px"}),
        html.Span(id=countdown_id, style={"marginLeft": "10px", "color": "orange"})
    ])

def register_callbacks(app):
    @app.callback(Output("live-price", "children"), Input("interval-component", "n_intervals"))
    def update_price(n):
        price = get_live_price()
        return f"Live XRP Price: ${price}"

    @app.callback(Output("signal-5m", "children"), Input("interval-component", "n_intervals"))
    def update_5m(n):
        price = get_live_price()
        return format_signal("5M", *generate_short_term_signals(price, 56, 0.5, 1000000), datetime.now(pytz.utc))

    @app.callback(Output("signal-10m", "children"), Input("interval-component", "n_intervals"))
    def update_10m(n):
        price = get_live_price()
        return format_signal("10M", *generate_short_term_signals(price, 51, 0.3, 950000), datetime.now(pytz.utc))

    @app.callback(Output("signal-15m", "children"), Input("interval-component", "n_intervals"))
    def update_15m(n):
        price = get_live_price()
        return format_signal("15M", *generate_short_term_signals(price, 49, -0.2, 870000), datetime.now(pytz.utc))

    @app.callback(Output("signal-1h", "children"), Input("interval-component", "n_intervals"))
    def update_1h(n):
        price = get_live_price()
        return format_signal("1H", *generate_long_term_signals(price, 61, 1.1, 2000000), datetime.now(pytz.utc))

    @app.callback(Output("signal-6h", "children"), Input("interval-component", "n_intervals"))
    def update_6h(n):
        price = get_live_price()
        return format_signal("6H", *generate_long_term_signals(price, 59, 0.6, 1800000), datetime.now(pytz.utc))

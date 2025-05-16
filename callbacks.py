from dash import Output, Input, State, html
from utils.data import get_live_price
from utils.signals_logic import generate_short_term_signals, generate_long_term_signals
from datetime import datetime
import pytz
import json

# Pill color logic
def get_pill_class(strength):
    if strength == "Strong":
        return "strong-pill"
    elif strength == "Medium":
        return "medium-pill"
    else:
        return "weak-pill"

# Signal formatting with timestamp and style
def format_signal(label, signal, confidence, strength, last_update):
    hst_time = last_update.astimezone(pytz.timezone("US/Hawaii")).strftime('%I:%M:%S %p')
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

# Register all signal callbacks
def register_callbacks(app):
    @app.callback(Output("live-price", "children"), Input("interval-component", "n_intervals"))
    def update_price(n):
        price = get_live_price()
        return f"Live XRP Price: ${price:.4f}"

    def create_signal_callback(signal_id, generator, rsi, macd, volume):
        signal_div = f"signal-{signal_id}"
        store_id = f"store-{signal_id}"

        @app.callback(
            Output(signal_div, "children"),
            Output(store_id, "data"),
            Input("interval-component", "n_intervals"),
            State(store_id, "data"),
        )
        def update_signal(n, stored):
            price = get_live_price()
            signal, confidence, strength = generator(price, rsi, macd, volume)
            now = datetime.now(pytz.utc)

            # If signal unchanged, reuse stored time
            if stored:
                previous = json.loads(stored)
                if previous.get("signal") == signal:
                    last_update = datetime.fromisoformat(previous["last_update"])
                else:
                    last_update = now
            else:
                last_update = now

            new_data = json.dumps({
                "signal": signal,
                "last_update": last_update.isoformat()
            })

            return format_signal(signal_id.upper(), signal, confidence, strength, last_update), new_data

    # Attach all timeframes
    create_signal_callback("5m", generate_short_term_signals, 56, 0.5, 1000000)
    create_signal_callback("10m", generate_short_term_signals, 50, 0.2, 950000)
    create_signal_callback("15m", generate_short_term_signals, 48, -0.2, 870000)
    create_signal_callback("1h", generate_long_term_signals, 61, 1.1, 2000000)
    create_signal_callback("6h", generate_long_term_signals, 59, 0.6, 1800000)

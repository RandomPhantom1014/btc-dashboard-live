from dash import Output, Input, State, html
from utils.data import get_live_price
from utils.signals_logic import generate_short_term_signals, generate_long_term_signals
from datetime import datetime
import pytz
import json
from logger import log_trade

def get_pill_class(strength):
    if strength == "Strong":
        return "strong-pill"
    elif strength == "Medium":
        return "medium-pill"
    else:
        return "weak-pill"

def format_signal(label, signal, confidence, strength, last_update):
    hst_time = last_update.astimezone(pytz.timezone("US/Hawaii")).strftime('%I:%M:%S %p')
    pill_class = f"signal-pill {get_pill_class(strength)}"
    countdown_id = f"countdown-{label.lower()}"

    duration_map = {
        "5M": 300,
        "10M": 600,
        "15M": 900,
        "1H": 3600,
        "6H": 21600
    }
    duration_seconds = duration_map.get(label.upper(), 300)

    return html.Div([
        html.Span(f"{label}: ", style={"fontWeight": "bold"}),
        html.Span(signal, className=pill_class),
        html.Span(f" {confidence}% confidence", style={"marginLeft": "10px"}),
        html.Span(f"({strength})", style={"marginLeft": "10px"}),
        html.Span(f"Last updated: {hst_time}", style={"marginLeft": "15px", "fontStyle": "italic"}),
        html.Span("counting...", id=countdown_id, **{
            "data-time": last_update.isoformat(),
            "data-duration": duration_seconds,
            "style": {"marginLeft": "10px", "color": "orange"}
        })
    ])

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

            if stored:
                previous = json.loads(stored)
                prev_signal = previous.get("signal")
                prev_time = datetime.fromisoformat(previous["last_update"])

                if prev_signal == signal:
                    elapsed = (now - prev_time).total_seconds()
                    duration_map = {
                        "5M": 300,
                        "10M": 600,
                        "15M": 900,
                        "1H": 3600,
                        "6H": 21600
                    }
                    duration_seconds = duration_map.get(signal_id.upper(), 300)

                    if elapsed >= duration_seconds:
                        last_update = now  # ⏱ reset countdown
                    else:
                        last_update = prev_time
                else:
                    last_update = now
            else:
                last_update = now

            # ✅ Log the signal event
            log_trade(
                signal_timeframe=signal_id.upper(),
                action=signal,
                confidence=confidence,
                strength=strength,
                price=price,
                status="Dashboard Display

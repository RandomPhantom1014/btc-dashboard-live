from dash import Output, Input, callback, dcc
from utils.data import get_latest_price
from utils.signals_logic import generate_signals_for_timeframe
from datetime import datetime, timedelta
import pytz

# Define your timeframes and movement targets
TIMEFRAMES = {
    "5m": {"minutes": 5, "target": 0.01},
    "10m": {"minutes": 10, "target": 0.02},
    "15m": {"minutes": 15, "target": 0.02},
    "1h": {"minutes": 60, "target": 0.05},
    "6h": {"minutes": 360, "target": 0.10}
}

@callback(
    Output("xrp-price-text", "children"),
    Input("interval-component", "n_intervals")
)
def update_price(n):
    return f"${get_latest_price():,.4f}"

# Create callbacks for each timeframe
for timeframe_id, config in TIMEFRAMES.items():
    @callback(
        Output(f"{timeframe_id}-signal", "children"),
        Output(f"{timeframe_id}-confidence", "children"),
        Output(f"{timeframe_id}-signal", "className"),
        Output(f"{timeframe_id}-timestamp", "children"),
        Output(f"{timeframe_id}-countdown", "children"),
        Input("interval-component", "n_intervals"),
        prevent_initial_call="initial_duplicate"
    )
    def update_signal(n, timeframe_id=timeframe_id, config=config):
        signal, confidence, strength = generate_signals_for_timeframe(
            timeframe_id, config["minutes"], config["target"]
        )

        # Get HST timestamp
        hst_time = datetime.utcnow() - timedelta(hours=10)
        timestamp = hst_time.strftime("%H:%M:%S")

        # Calculate expiration countdown
        now = datetime.utcnow()
        expiry_time = now + timedelta(minutes=config["minutes"])
        countdown = str(timedelta(seconds=int((expiry_time - now).total_seconds())))

        # Determine style class from strength
        if strength == "strong":
            color_class = "pill pill-strong"
        elif strength == "moderate":
            color_class = "pill pill-moderate"
        else:
            color_class = "pill pill-weak"

        return signal, f"{confidence}%", color_class, f"📅 {timestamp} HST", f"⏳ {countdown}"

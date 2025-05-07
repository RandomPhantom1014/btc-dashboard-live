# components/signal_logic.py

import random

def get_signal_data(mode, timeframe):
    """
    Returns mock or live/backtest signals based on the selected mode.
    """
    if mode == "live":
        return fetch_live_signals(timeframe)
    else:
        return fetch_backtest_signals(timeframe)

def fetch_live_signals(timeframe):
    signals = ["Go Long", "Go Short", "Wait"]
    confidence = round(random.uniform(60, 99), 2)
    strength = random.choice(["Strong", "Moderate", "Weak"])
    return random.choice(signals), f"Confidence: {confidence}%", strength

def fetch_backtest_signals(timeframe):
    signals = ["Go Long", "Go Short", "Wait"]
    confidence = round(random.uniform(40, 95), 2)
    strength = random.choice(["Weak", "Moderate", "Strong"])
    return random.choice(signals), f"Backtest Conf: {confidence}%", strength

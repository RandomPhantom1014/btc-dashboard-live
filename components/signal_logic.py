# components/signal_logic.py

import random

def fetch_live_signals():
    signals = ["Go Long", "Go Short", "Wait"]
    confidence = round(random.uniform(50, 99), 2)
    strength = random.choice(["Strong", "Moderate", "Weak"])
    return random.choice(signals), f"Confidence: {confidence}%", strength

def fetch_backtest_signals():
    # Replace this logic with actual backtest data logic later
    signals = ["Go Long", "Go Short", "Wait"]
    confidence = round(random.uniform(60, 95), 2)
    strength = random.choice(["Moderate", "Weak"])
    return random.choice(signals), f"(Backtest) Confidence: {confidence}%", strength


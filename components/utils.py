# components/utils.py

import csv
import os
from datetime import datetime

LOG_FILE = "logs/signal_log.csv"

def ensure_log_file_exists():
    os.makedirs("logs", exist_ok=True)
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "timeframe", "signal", "confidence", "strength", "price"])

def append_log(timeframe, signal, confidence, strength, price):
    ensure_log_file_exists()
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            timeframe,
            signal,
            confidence,
            strength,
            price
        ])


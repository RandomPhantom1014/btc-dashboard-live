# components/logger.py

import os
import csv
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "btc_signals_log.csv")

def save_log_entry(timestamp, timeframe, signal, confidence):
    os.makedirs(LOG_DIR, exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Timeframe", "Signal", "Confidence"])
        writer.writerow([timestamp, timeframe, signal, confidence])

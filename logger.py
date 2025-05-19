import csv
import os
from datetime import datetime

def log_trade(signal_timeframe, action, confidence, strength, price, status, reason, amount):
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"logs/dashboard_signals_{date_str}.csv"
    
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow([
                "Timestamp",
                "Timeframe",
                "Action",
                "Confidence",
                "Strength",
                "Price",
                "Status",
                "Reason",
                "Amount"
            ])
        
        writer.writerow([
            datetime.utcnow().isoformat(),
            signal_timeframe,
            action,
            confidence,
            strength,
            price,
            status,
            reason,
            amount
        ])

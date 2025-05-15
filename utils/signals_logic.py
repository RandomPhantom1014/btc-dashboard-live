from datetime import datetime
import random

def get_rsi_mock():
    # In real usage, replace this with actual RSI data
    return random.randint(40, 65)

def generate_signals_for_timeframe(timeframe):
    def callback(n):
        now = datetime.now().strftime("%H:%M:%S")
        rsi = get_rsi_mock()
        
        # Define move target thresholds
        if timeframe in ["5m", "10m", "15m"]:
            move_target = 0.01 if rsi < 45 else 0.02  # 1–2¢
        else:
            move_target = 0.05 if rsi < 45 else 0.10  # 5–10¢

        # Trading logic based on RSI
        if rsi > 55:
            direction = "GO LONG"
        elif rsi < 45:
            direction = "GO SHORT"
        else:
            direction = "WAIT"

        return f"{timeframe.upper()} Signal: {direction} | Target: ${move_target:.2f} | RSI: {rsi} | {now}"
    return callback

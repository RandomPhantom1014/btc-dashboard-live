from datetime import datetime

def generate_signals_for_timeframe(timeframe):
    def callback(n):
        now = datetime.now().strftime("%H:%M:%S")
        if timeframe in ["5m", "10m", "15m"]:
            price_move = 0.02
        else:
            price_move = 0.1
        return f"{timeframe.upper()} Signal: GO LONG - {price_move} move @ {now}"
    return callback

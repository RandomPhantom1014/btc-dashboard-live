import random

def generate_signal(prices, interval, rsi, macd, volume, threshold_up=0.02, threshold_down=0.01):
    latest_price = prices[-1]
    price_change = (latest_price - prices[0]) / prices[0]

    if interval in ['1h', '6h']:
        up_move = 0.10  # 10 cents
        down_move = -0.05  # 5 cents
    else:
        up_move = 0.02  # 2 cents
        down_move = -0.01  # 1 cent

    if rsi > 55 and macd > 0 and volume > 0:
        if price_change >= up_move:
            return "Go Long", random.uniform(70, 90)
    elif rsi < 45 and macd < 0 and volume > 0:
        if price_change <= down_move:
            return "Go Short", random.uniform(70, 90)

    return "Wait", random.uniform(50, 60)

import random

def generate_signal(prices, interval, rsi, macd, volume):
    latest_price = prices[-1]
    price_change = (latest_price - prices[0])

    # Define thresholds for XRP
    if interval in ['1h', '6h']:
        up_move = 0.10   # 10 cents
        down_move = -0.05  # 5 cents
    else:
        up_move = 0.02    # 2 cents
        down_move = -0.01  # 1 cent

    if rsi > 55 and macd > 0 and volume > 0:
        if price_change >= up_move:
            return "Go Long", random.uniform(70, 90)
    elif rsi < 45 and macd < 0 and volume > 0:
        if price_change <= down_move:
            return "Go Short", random.uniform(70, 90)

    return "Wait", random.uniform(50, 60)


def generate_signals_for_timeframe(prices_dict, rsi_dict, macd_dict, volume_dict):
    signals = {}

    for interval in prices_dict.keys():
        prices = prices_dict[interval]
        rsi = rsi_dict.get(interval, 50)
        macd = macd_dict.get(interval, 0)
        volume = volume_dict.get(interval, 0)

        signal, confidence = generate_signal(prices, interval, rsi, macd, volume)
        signals[interval] = {
            'signal': signal,
            'confidence': round(confidence, 2)
        }

    return signals

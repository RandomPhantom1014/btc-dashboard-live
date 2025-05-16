def generate_short_term_signals(price, rsi, macd, volume):
    if price == 0.0:
        return None, 0, 'Weak'

    if rsi > 55 and macd > 0 and volume > 1000000:
        return 'Go Long', 85, 'Strong'
    elif rsi < 45 and macd < 0:
        return 'Go Short', 80, 'Medium'
    else:
        return 'Wait', 60, 'Weak'


def generate_long_term_signals(price, rsi, macd, volume):
    if price == 0.0:
        return None, 0, 'Weak'

    if rsi > 60 and macd > 0 and volume > 2000000:
        return 'Go Long', 90, 'Strong'
    elif rsi < 40 and macd < 0:
        return 'Go Short', 85, 'Medium'
    else:
        return 'Wait', 65, 'Weak'

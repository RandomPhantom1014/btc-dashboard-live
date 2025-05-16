def generate_short_term_signals(price, rsi, macd, volume):
    if price == 0.0:
        return None, 0, 'Weak'

    # Short-Term: Targeting $0.01 to $0.02 movements
    if rsi > 55 and macd > 0 and volume > 800000:
        return 'Go Long', 85, 'Strong'
    elif rsi < 45 and macd < 0 and volume > 800000:
        return 'Go Short', 80, 'Medium'
    else:
        return 'Wait', 60, 'Weak'


def generate_long_term_signals(price, rsi, macd, volume):
    if price == 0.0:
        return None, 0, 'Weak'

    # Long-Term: Targeting $0.05 to $0.10 movements

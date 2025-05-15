def get_signal_for_interval(minutes, symbol, current_price):
    import random
    rsi = random.uniform(30, 70)
    confidence = 50

    if minutes <= 15:
        price_target = 0.02  # 1–2 cents
    else:
        price_target = 0.10  # 5–10 cents

    if rsi > 55:
        signal = "Go Long"
        confidence = int((rsi - 55) * 2 + 50)
    elif rsi < 45:
        signal = "Go Short"
        confidence = int((45 - rsi) * 2 + 50)
    else:
        signal = "Wait"
        confidence = 50

    return signal, min(confidence, 100)

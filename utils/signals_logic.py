def generate_signals(df, tf):
    if df.empty or 'close' not in df.columns:
        return {"signal": "Wait", "confidence": 0, "strength_class": "neutral"}

    # Set movement threshold
    movement_target = 0.05 if tf in ['5m', '10m', '15m'] else 0.10

    # Set candle lookback by timeframe
    lookback = {
        "5m": 5,
        "10m": 10,
        "15m": 15,
        "1h": 60,
        "6h": 360
    }.get(tf, 5)

    recent = df.tail(lookback)
    price_change = recent['close'].iloc[-1] - recent['close'].iloc[0]
    rsi = compute_rsi(recent['close'])

    if price_change >= movement_target and rsi > 55:
        return {"signal": "Go Long", "confidence": 92, "strength_class": "strong"}
    elif price_change <= -movement_target and rsi < 45:
        return {"signal": "Go Short", "confidence": 90, "strength_class": "strong"}
    else:
        return {"signal": "Wait", "confidence": 60, "strength_class": "neutral"}

def compute_rsi(series, period=14):
    delta = series.diff().dropna()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss.replace(to_replace=0, method='ffill').fillna(0)
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else 50

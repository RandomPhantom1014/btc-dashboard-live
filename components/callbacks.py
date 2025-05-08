# callbacks.py

from dash import Input, Output, State, dcc
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from components.chart import render_candlestick_chart
from components.indicators import render_indicators
from utils.data import get_btc_data, get_backtest_data, append_log
from utils.indicators import calculate_rsi, calculate_macd, calculate_volume_strength
import os

previous_price = None

def register_callbacks(app):

    # ========== LIVE BTC PRICE ==========
    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_btc_price(n_intervals):
        global previous_price
        current_price = fetch_live_btc_price()

        if current_price is None:
            return "Live BTC Price: Error"

        color = "white"
        if previous_price is not None:
            if current_price > previous_price:
                color = "limegreen"
            elif current_price < previous_price:
                color = "red"
        previous_price = current_price

        return [
            f"Live BTC Price: ",
            {
                "type": "span",
                "props": {
                    "style": {"color": color, "fontWeight": "bold"},
                    "children": f"${current_price:,.2f}"
                }
            }
        ]

    # ========== CHART + INDICATORS ==========
    @app.callback(
        Output("candlestick-chart", "figure"),
        Output("indicators-container", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_chart_and_indicators(n_intervals, mode):
        df = get_backtest_data() if mode == "backtest" else get_btc_data()
        if df.empty:
            raise PreventUpdate

        chart_fig = render_candlestick_chart(df)
        rsi = calculate_rsi(df)
        macd_line, _, _ = calculate_macd(df)
        volume = df["volume"]

        indicators = render_indicators(
            rsi_data=rsi[-30:].tolist(),
            macd_data=macd_line[-30:].tolist(),
            volume_data=volume[-30:].tolist()
        )

        return chart_fig, indicators

    # ========== SIGNAL ENGINE W/ PRICE TARGET LOGIC ==========
    def generate_signal(df):
        # Measure actual price change
        price_start = df["close"].iloc[0]
        price_end = df["close"].iloc[-1]
        price_change = price_end - price_start

        rsi = calculate_rsi(df).iloc[-1]
        macd_line, signal_line, _ = calculate_macd(df)
        macd_current = macd_line.iloc[-1]
        macd_prev = macd_line.iloc[-2]
        signal_current = signal_line.iloc[-1]
        signal_prev = signal_line.iloc[-2]
        volume_strength = calculate_volume_strength(df).iloc[-1]

        signal = "Wait"
        confidence = 50
        strength = 5

        # Require at least $100 move
        if abs(price_change) >= 100:
            if price_change > 0:
                signal = "Go Long"
            else:
                signal = "Go Short"

            # Boost confidence if indicators align
            indicator_score = 0
            if signal == "Go Long" and rsi < 35 and macd_current > signal_current and macd_prev < signal_prev:
                indicator_score += 2
            if signal == "Go Short" and rsi > 65 and macd_current < signal_current and macd_prev > signal_prev:
                indicator_score += 2
            if volume_strength > 1:
                indicator_score += 1

            confidence = 70 + (indicator_score * 5)
            strength = min(10, 5 + indicator_score)

        return signal, f"Confidence: {confidence}%", f"Strength: {strength}/10"

    def log_signal_if_enabled(log_enabled, timeframe, signal, confidence, strength, price):
        if log_enabled:
            append_log(timeframe, signal, confidence, strength, price)

    # ========== SIGNAL CALLBACKS ==========
    @app.callback(
        Output("signal-5m", "children"),
        Output("confidence-5m", "children"),
        Output("strength-5m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signal_5m(n, mode, log_enabled):
        df = get_backtest_data() if mode == "backtest" else get_btc_data()
        if df.empty:
            raise PreventUpdate
        signal, confidence, strength = generate_signal(df.tail(5))
        price = df["close"].iloc[-1]
        log_signal_if_enabled(log_enabled, "5m", signal, confidence, strength, price)
        return signal, confidence, strength

    @app.callback(
        Output("signal-10m", "children"),
        Output("confidence-10m", "children"),
        Output("strength-10m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signal_10m(n, mode, log_enabled):
        df = get_backtest_data() if mode == "backtest" else get_btc_data()
        if df.empty:
            raise PreventUpdate
        signal, confidence, strength = generate_signal(df.tail(10))
        price = df["close"].iloc[-1]
        log_signal_if_enabled(log_enabled, "10m", signal, confidence, strength, price)
        return signal, confidence, strength

    @app.callback(
        Output("signal-15m", "children"),
        Output("confidence-15m", "children"),
        Output("strength-15m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signal_15m(n, mode, log_enabled):
        df = get_backtest_data() if mode == "backtest" else get_btc_data()
        if df.empty:
            raise PreventUpdate
        signal, confidence, strength = generate_signal(df.tail(15))
        price = df["close"].iloc[-1]
        log_signal_if_enabled(log_enabled, "15m", signal, confidence, strength, price)
        return signal, confidence, strength

    # ========== EXPORT CSV ==========
    @app.callback(
        Output("export-button", "href"),
        Input("export-button", "n_clicks"),
        prevent_initial_call=True
    )
    def export_csv(n_clicks):
        log_path = "logs/signal_log.csv"
        if os.path.exists(log_path):
            return "/logs/signal_log.csv"
        else:
            raise PreventUpdate


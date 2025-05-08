# callbacks.py

from dash import Input, Output, State, dcc
from dash.exceptions import PreventUpdate
from components.chart import render_candlestick_chart
from components.indicators import render_indicators
from utils.data import get_btc_data, get_backtest_data, append_log, ensure_log_file_exists
from utils.indicators import calculate_rsi, calculate_macd, calculate_volume_strength
import os
import requests

LOG_PATH = "logs/signal_log.csv"
previous_price = None

# Replace old Binance function with CoinGecko-based fetch
def fetch_live_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data["bitcoin"]["usd"])
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

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

        current_price = float(current_price)

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

    def generate_signal(df):
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

        if abs(price_change) >= 100:
            if price_change > 0:
                signal = "Go Long"
            else:
                signal = "Go Short"

            score = 0
            if signal == "Go Long" and rsi < 35 and macd_current > signal_current and macd_prev < signal_prev:
                score += 2
            if signal == "Go Short" and rsi > 65 and macd_current < signal_current and macd_prev > signal_prev:
                score += 2
            if volume_strength > 1:
                score += 1

            confidence = 70 + (score * 5)
            strength = min(10, 5 + score)

        return signal, f"Confidence: {confidence}%", f"Strength: {strength}/10"

    def log_signal_if_enabled(log_enabled, timeframe, signal, confidence, strength, price):
        if log_enabled:
            ensure_log_file_exists()
            append_log(timeframe, signal, confidence, strength, price)

    def make_signal_callback(timeframe, tail_n):
        @app.callback(
            Output(f"signal-{timeframe}", "children"),
            Output(f"confidence-{timeframe}", "children"),
            Output(f"strength-{timeframe}", "children"),
            Input("interval-component", "n_intervals"),
            State("mode-toggle", "value"),
            State("save-logs-toggle", "value")
        )
        def signal_callback(n, mode, log_enabled):
            df = get_backtest_data() if mode == "backtest" else get_btc_data()
            if df.empty:
                raise PreventUpdate
            sliced_df = df.tail(tail_n)
            signal, confidence, strength = generate_signal(sliced_df)
            price = sliced_df["close"].iloc[-1]
            log_signal_if_enabled(log_enabled, timeframe, signal, confidence, strength, price)
            return signal, confidence, strength

    make_signal_callback("5m", 5)
    make_signal_callback("10m", 10)
    make_signal_callback("15m", 15)

    @app.callback(
        Output("export-button", "href"),
        Input("export-button", "n_clicks"),
        prevent_initial_call=True
    )
    def export_csv(n_clicks):
        ensure_log_file_exists()
        if os.path.exists(LOG_PATH):
            return f"/{LOG_PATH}"
        else:
            raise PreventUpdate

    @app.callback(
        Output("url", "href"),
        Input("theme-toggle", "value"),
        prevent_initial_call=True
    )
    def switch_theme(theme):
        return f"/?theme={theme}"


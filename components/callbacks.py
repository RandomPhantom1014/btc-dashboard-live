# callbacks.py

from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from components.chart import render_candlestick_chart
from components.indicators import render_indicators
from utils.data import get_btc_data
from utils.indicators import calculate_rsi, calculate_macd, calculate_volume_strength

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
        Input("interval-component", "n_intervals")
    )
    def update_chart_and_indicators(n_intervals):
        df = get_btc_data()
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

    # ========== SIGNAL GENERATION HELPERS ==========
    def generate_signal(df):
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

        if rsi < 30 and macd_current > signal_current and macd_prev < signal_prev:
            signal = "Go Long"
            confidence = 80
            strength = 8 if volume_strength > 1 else 6
        elif rsi > 70 and macd_current < signal_current and macd_prev > signal_prev:
            signal = "Go Short"
            confidence = 80
            strength = 8 if volume_strength > 1 else 6

        return signal, f"Confidence: {confidence}%", f"Strength: {strength}/10"

    # ========== SIGNAL CALLBACKS ==========

    @app.callback(
        Output("signal-5m", "children"),
        Output("confidence-5m", "children"),
        Output("strength-5m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_signal_5m(n, mode):
        df = get_btc_data()
        if df.empty:
            raise PreventUpdate
        df_5m = df.tail(5)
        return generate_signal(df_5m)

    @app.callback(
        Output("signal-10m", "children"),
        Output("confidence-10m", "children"),
        Output("strength-10m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_signal_10m(n, mode):
        df = get_btc_data()
        if df.empty:
            raise PreventUpdate
        df_10m = df.tail(10)
        return generate_signal(df_10m)

    @app.callback(
        Output("signal-15m", "children"),
        Output("confidence-15m", "children"),
        Output("strength-15m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_signal_15m(n, mode):
        df = get_btc_data()
        if df.empty:
            raise PreventUpdate
        df_15m = df.tail(15)
        return generate_signal(df_15m)



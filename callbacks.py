# callbacks.py

from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from components.indicators import render_indicators
from utils.indicators import calculate_indicators
from utils.data import get_btc_data
from utils.signals_logic import generate_signals
from utils.data import append_log
import datetime

previous_price = None  # For color change tracking

def register_callbacks(app):
    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals"),
        prevent_initial_call=True
    )
    def update_btc_price(n):
        global previous_price
        price = fetch_live_btc_price()
        if price is None:
            return "Live BTC Price: Error"

        color = "white"
        if previous_price is not None:
            if price > previous_price:
                color = "limegreen"
            elif price < previous_price:
                color = "red"
        previous_price = price

        return html.Span([
            "Live BTC Price: ",
            html.Span(f"${price:,.2f}", style={"color": color, "fontWeight": "bold"})
        ])

    # Main signal callback
    @app.callback(
        Output("signal-5m", "children"),
        Output("confidence-5m", "children"),
        Output("strength-5m", "children"),
        Output("signal-10m", "children"),
        Output("confidence-10m", "children"),
        Output("strength-10m", "children"),
        Output("signal-15m", "children"),
        Output("confidence-15m", "children"),
        Output("strength-15m", "children"),
        Output("indicators-container", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value"),
    )
    def update_signals(n, mode, save_logs):
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        rsi, macd, volume = calculate_indicators(df)
        indicators = render_indicators(rsi, macd, volume)

        signals = {}
        for tf in ["5m", "10m", "15m"]:
            signal, confidence, strength = generate_signals(df, tf)
            signals[tf] = (signal, confidence, strength)

            if save_logs:
                try:
                    append_log(tf, signal, confidence, strength, df['close'].iloc[-1])
                except Exception as e:
                    print(f"Log save error: {e}")

        return (
            signals["5m"][0], f"Confidence: {signals['5m'][1]}%", signals["5m"][2],
            signals["10m"][0], f"Confidence: {signals['10m'][1]}%", signals["10m"][2],
            signals["15m"][0], f"Confidence: {signals['15m'][1]}%", signals["15m"][2],
            indicators
        )

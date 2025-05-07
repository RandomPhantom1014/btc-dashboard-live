# components/callbacks.py

from dash import Input, Output
from .styles import light_theme, dark_theme
from .indicators import calculate_rsi, calculate_macd, calculate_volume
from .utils import fetch_binance_price, simulate_signals

def register_callbacks(app):
    @app.callback(
        Output('live-price-display', 'children'),
        Output('btc-price-chart', 'figure'),
        Output('rsi-chart', 'figure'),
        Output('macd-chart', 'figure'),
        Output('volume-chart', 'figure'),
        Output('signal-5m', 'children'),
        Output('confidence-5m', 'children'),
        Output('signal-10m', 'children'),
        Output('confidence-10m', 'children'),
        Output('signal-15m', 'children'),
        Output('confidence-15m', 'children'),
        Output('strength-meter', 'children'),
        Input('price-update-interval', 'n_intervals'),
        Input('theme-toggle', 'value')
    )
    def update_dashboard(n, theme):
        # Select the active theme
        colors = light_theme if theme == "light" else dark_theme

        # Live price
        btc_price = fetch_binance_price()

        # Simulate historical price data (replace with real data for production)
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        price_data = pd.DataFrame({
            'time': [now - timedelta(minutes=i) for i in range(49, -1, -1)],
            'price': [btc_price + np.random.randint(-100, 100) for _ in range(50)]
        })

        # Calculate indicators
        rsi_fig = calculate_rsi(price_data, colors)
        macd_fig = calculate_macd(price_data, colors)
        vol_fig = calculate_volume(price_data, colors)

        # Candlestick chart
        import plotly.graph_objs as go
        candlestick_fig = {
            "data": [
                go.Candlestick(
                    x=price_data["time"],
                    open=price_data["price"],
                    high=price_data["price"] + 50,
                    low=price_data["price"] - 50,
                    close=price_data["price"],
                    name="BTC",
                    increasing_line_color=colors["accent"],
                    decreasing_line_color='red'
                )
            ],
            "layout": go.Layout(
                title="Live BTC Price Chart",
                xaxis={"title": "Time"},
                yaxis={"title": "Price (USD)"},
                paper_bgcolor=colors["background"],
                plot_bgcolor=colors["background"],
                font={"color": colors["text"]}
            )
        }

        # Simulated signals
        signals = simulate_signals()

        def make_signal_row(tf):
            signal = signals[tf]['signal']
            confidence = signals[tf]['confidence']
            pill_color = colors[f"pill_{signal.lower()}"]
            return (
                f"{signal}",
                f"Confidence: {confidence}%"
            )

        # Strength meter
        average_conf = int((signals['5m']['confidence'] + signals['10m']['confidence'] + signals['15m']['confidence']) / 3)
        if average_conf >= 90:
            strength = "Strong"
            strength_color = colors["pill_go_long"]
        elif average_conf >= 80:
            strength = "Moderate"
            strength_color = colors["pill_wait"]
        else:
            strength = "Weak"
            strength_color = colors["pill_go_short"]

        return (
            f"BTC Price: ${btc_price:,.2f}",
            candlestick_fig,
            rsi_fig,
            macd_fig,
            vol_fig,
            *make_signal_row("5m"),
            *make_signal_row("10m"),
            *make_signal_row("15m"),
            f"Signal Strength: {strength}"
        )

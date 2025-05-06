# components/callbacks.py

from dash import Input, Output, State
import plotly.graph_objs as go
from datetime import datetime, timedelta
import pandas as pd
import random
from .themes import light_theme, dark_theme
from .signal_logic import generate_signal_data
from .binance_ws import get_latest_price

def register_callbacks(app):

    @app.callback(
        Output('main-container', 'className'),
        Input('theme-toggle', 'value')
    )
    def update_theme_class(theme):
        return f"{theme}-theme"

    @app.callback(
        Output('live-price-display', 'children'),
        Input('price-update-interval', 'n_intervals')
    )
    def update_live_price(n):
        price = get_latest_price()
        if price:
            return f"Live BTC Price: ${price:,.2f}"
        else:
            return "Fetching price..."

    @app.callback(
        Output('btc-price-chart', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_price_chart(n):
        now = datetime.now()
        times = [now - timedelta(minutes=i) for i in range(50)]
        prices = [get_latest_price() + random.randint(-150, 150) for _ in range(50)]
        df = pd.DataFrame({'time': times[::-1], 'price': prices[::-1]})

        return {
            'data': [go.Candlestick(
                x=df['time'],
                open=df['price'],
                high=df['price'] + 20,
                low=df['price'] - 20,
                close=df['price']
            )],
            'layout': go.Layout(
                title="Live BTC Price Chart",
                xaxis={'title': 'Time'},
                yaxis={'title': 'Price (USD)'},
                paper_bgcolor='transparent',
                plot_bgcolor='transparent'
            )
        }

    @app.callback(
        Output('signal-5m', 'children'),
        Output('confidence-5m', 'children'),
        Output('signal-10m', 'children'),
        Output('confidence-10m', 'children'),
        Output('signal-15m', 'children'),
        Output('confidence-15m', 'children'),
        Output('strength-meter', 'children'),
        Input('interval-component', 'n_intervals'),
        State('mode-toggle', 'value')
    )
    def update_signals(n, mode):
        data = generate_signal_data(mode)

        def pill(signal):
            color_class = {
                "Go Long": "pill pill-long",
                "Go Short": "pill pill-short",
                "Wait": "pill pill-wait"
            }.get(signal, "pill")
            return f"{signal}"

        strength = f"Signal Strength: {max(data['5m']['confidence'], data['10m']['confidence'], data['15m']['confidence'])}%"

        return (
            pill(data['5m']['signal']), f"Confidence: {data['5m']['confidence']}%",
            pill(data['10m']['signal']), f"Confidence: {data['10m']['confidence']}%",
            pill(data['15m']['signal']), f"Confidence: {data['15m']['confidence']}%",
            strength
        )


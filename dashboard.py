from dash import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import random
from dash.exceptions import PreventUpdate
from .utils import fetch_binance_price, simulate_signals
from .indicators import calculate_rsi, calculate_macd, calculate_volume


def register_callbacks(app):

    @app.callback(
        Output('live-btc-price-chart', 'figure'),
        Input('interval-component', 'n_intervals'),
        prevent_initial_call=True
    )
    def update_price_chart(n):
        price = fetch_binance_price()
        if price is None:
            raise PreventUpdate
        return {
            "data": [go.Scatter(x=[0], y=[price], mode='lines+markers', name='BTC/USDT')],
            "layout": go.Layout(title='Live BTC Price', xaxis=dict(title='Time'), yaxis=dict(title='Price'))
        }

    @app.callback(
        [
            Output('signal-5m', 'children'),
            Output('signal-10m', 'children'),
            Output('signal-15m', 'children'),
            Output('signal-strength', 'children')
        ],
        Input('interval-component', 'n_intervals'),
        prevent_initial_call=True
    )
    def update_signals(n):
        signals = simulate_signals()

        strength = max([
            signals['5m']['confidence'],
            signals['10m']['confidence'],
            signals['15m']['confidence']
        ])

        strength_color = (
            "🟢 Strong" if strength >= 90 else
            "🟡 Moderate" if strength >= 80 else
            "🔴 Weak"
        )

        return (
            f"{signals['5m']['signal']} ({signals['5m']['confidence']}%)",
            f"{signals['10m']['signal']} ({signals['10m']['confidence']}%)",
            f"{signals['15m']['signal']} ({signals['15m']['confidence']}%)",
            strength_color
        )

    @app.callback(
        [
            Output('rsi-chart', 'figure'),
            Output('macd-chart', 'figure'),
            Output('volume-chart', 'figure')
        ],
        Input('interval-component', 'n_intervals'),
        prevent_initial_call=True
    )
    def update_indicator_charts(n):
        price = fetch_binance_price()
        if price is None:
            raise PreventUpdate

        # Simulate a small dummy DataFrame for indicators
        df = pd.DataFrame({
            "price": [price + random.uniform(-50, 50) for _ in range(100)],
            "volume": [random.randint(100, 1000) for _ in range(100)]
        })

        rsi = calculate_rsi(df)
        macd_line, signal_line = calculate_macd(df)
        volume = calculate_volume(df)

        rsi_fig = go.Figure(go.Scatter(y=rsi, mode="lines", name="RSI"))
        rsi_fig.update_layout(title="RSI", height=200)

        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(y=macd_line, mode="lines", name="MACD"))
        macd_fig.add_trace(go.Scatter(y=signal_line, mode="lines", name="Signal"))
        macd_fig.update_layout(title="MACD", height=200)

        volume_fig = go.Figure(go.Bar(y=volume, name="Volume"))
        volume_fig.update_layout(title="Volume", height=200)

        return rsi_fig, macd_fig, volume_fig


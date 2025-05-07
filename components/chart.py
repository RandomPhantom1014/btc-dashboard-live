# components/chart.py

import plotly.graph_objs as go
from dash import dcc
import pandas as pd

def render_candlestick_chart(df: pd.DataFrame):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name="BTC/USD"
            )
        ]
    )
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        height=400
    )
    return dcc.Graph(figure=fig, id="candlestick-chart")

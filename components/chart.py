# components/chart.py

import plotly.graph_objs as go

def render_candlestick_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name="Candles"
    ))

    fig.update_layout(
        title="BTC/USD - Candlestick Chart",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400
    )

    return fig

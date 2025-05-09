# components/chart.py

import plotly.graph_objs as go

def render_candlestick_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df["timestamp"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="BTC"
    ))

    fig.update_layout(
        title="BTC Candlestick Chart",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig


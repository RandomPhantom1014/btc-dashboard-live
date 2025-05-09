# components/chart.py

from dash import dcc
import plotly.graph_objs as go

def render_candlestick_chart(df):
    if df.empty or "timestamp" not in df.columns:
        return go.Figure()

    fig = go.Figure(data=[go.Candlestick(
        x=df["timestamp"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="BTC/USD"
    )])

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_rangeslider_visible=False,
        xaxis_title="Time",
        yaxis_title="Price (USD)",
    )

    return fig


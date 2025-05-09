# components/chart.py

from dash import dcc
import plotly.graph_objs as go

def render_candlestick_chart(df):
    if df is None or df.empty:
        return go.Figure()

    fig = go.Figure(data=[
        go.Candlestick(
            x=df["timestamp"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Candles"
        )
    ])

    fig.update_layout(
        margin=dict(l=30, r=30, t=30, b=30),
        height=400,
        xaxis_rangeslider_visible=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#fff"),
        yaxis_title="BTC Price",
        xaxis_title="Time"
    )

    return fig


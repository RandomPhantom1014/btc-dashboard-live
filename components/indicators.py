# components/indicators.py

from dash import html, dcc
import plotly.graph_objs as go

def render_indicators(df):
    # Assume RSI, MACD, Signal, and Volume columns are already present in the DataFrame
    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["RSI"],
        mode="lines",
        name="RSI"
    ))
    rsi_fig.update_layout(
        height=200,
        margin=dict(l=30, r=30, t=30, b=30),
        yaxis_title="RSI",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    macd_fig = go.Figure()
    macd_fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["MACD"],
        mode="lines",
        name="MACD"
    ))
    macd_fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["Signal"],
        mode="lines",
        name="Signal"
    ))
    macd_fig.update_layout(
        height=200,
        margin=dict(l=30, r=30, t=30, b=30),
        yaxis_title="MACD",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    volume_fig = go.Figure()
    volume_fig.add_trace(go.Bar(
        x=df["timestamp"],
        y=df["volume"],
        name="Volume"
    ))
    volume_fig.update_layout(
        height=200,
        margin=dict(l=30, r=30, t=30, b=30),
        yaxis_title="Volume",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return html.Div([
        dcc.Graph(figure=rsi_fig),
        dcc.Graph(figure=macd_fig),
        dcc.Graph(figure=volume_fig)
    ])


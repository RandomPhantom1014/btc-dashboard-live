# components/indicators.py

from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd

def render_indicators(df):
    if df.empty or "timestamp" not in df.columns:
        return html.Div("Loading indicators...")

    rsi_chart = go.Figure(
        data=[go.Scatter(x=df["timestamp"], y=df["rsi"], mode="lines", name="RSI")],
        layout=go.Layout(
            height=200,
            margin=dict(l=30, r=30, t=30, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title="RSI", range=[0, 100])
        )
    )

    macd_chart = go.Figure(
        data=[go.Scatter(x=df["timestamp"], y=df["macd"], mode="lines", name="MACD")],
        layout=go.Layout(
            height=200,
            margin=dict(l=30, r=30, t=30, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title="MACD")
        )
    )

    volume_chart = go.Figure(
        data=[go.Bar(x=df["timestamp"], y=df["volume"], name="Volume")],
        layout=go.Layout(
            height=200,
            margin=dict(l=30, r=30, t=30, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title="Volume")
        )
    )

    return html.Div([
        html.Div([
            html.H5("RSI Indicator"),
            dcc.Graph(figure=rsi_chart, config={"displayModeBar": False})
        ]),
        html.Div([
            html.H5("MACD Indicator"),
            dcc.Graph(figure=macd_chart, config={"displayModeBar": False})
        ]),
        html.Div([
            html.H5("Volume"),
            dcc.Graph(figure=volume_chart, config={"displayModeBar": False})
        ])
    ], style={"padding": "10px"})


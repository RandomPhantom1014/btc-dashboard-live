# components/indicators.py

from dash import html, dcc
import plotly.graph_objs as go

def render_indicators(rsi_data, macd_data, volume_data):
    return html.Div([
        html.Div([
            html.H5("RSI Indicator"),
            dcc.Graph(figure=go.Figure(go.Scatter(y=rsi_data, name="RSI")))
        ]),
        html.Div([
            html.H5("MACD Indicator"),
            dcc.Graph(figure=go.Figure(go.Scatter(y=macd_data, name="MACD")))
        ]),
        html.Div([
            html.H5("Volume"),
            dcc.Graph(figure=go.Figure(go.Bar(y=volume_data, name="Volume")))
        ])
    ])


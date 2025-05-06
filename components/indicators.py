# components/indicators.py

from dash import dcc, html

def rsi_chart():
    return html.Div([
        html.H4("RSI"),
        dcc.Graph(id="rsi-graph", config={"displayModeBar": False})
    ], className="indicator-section")

def macd_chart():
    return html.Div([
        html.H4("MACD"),
        dcc.Graph(id="macd-graph", config={"displayModeBar": False})
    ], className="indicator-section")

def volume_chart():
    return html.Div([
        html.H4("Volume"),
        dcc.Graph(id="volume-graph", config={"displayModeBar": False})
    ], className="indicator-section")

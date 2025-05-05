import dash
from dash import html, dcc

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("BTC Signal Dashboard"),
    html.Div("Signal Output: Go Long / Short / Hold"),
    html.Div("Confidence: 73%"),
    html.Div("Signal Strength Meter: ██████░░░░"),
])

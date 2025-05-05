import dash
from dash import html

# This must be named 'app' — gunicorn looks for this
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("BTC Signal Dashboard"),
    html.Div("Signal Output: Go Long / Short / Hold"),
    html.Div("Confidence: 73%"),
    html.Div("Signal Strength Meter: ██████░░░░"),
])


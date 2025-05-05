import dash
from dash import html

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1('BTC Signal Dashboard'),
    html.P('Live signals will be displayed here.')
])

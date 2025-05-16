from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from layout import serve_layout
from callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

app.layout = html.Div([
    serve_layout(),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
])

register_callbacks(app)

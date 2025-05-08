# app.py

import dash
import dash_bootstrap_components as dbc
from dash import html
from components.layout import create_layout
from callbacks import register_callbacks

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="BTC Signal Dashboard",
    update_title="Updating...",
)

app.layout = html.Div(id="main-layout", children=[create_layout()])
register_callbacks(app)

server = app.server  # For deployment on Render


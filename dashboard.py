# dashboard.py

import dash
from dash import html
import dash_bootstrap_components as dbc
from components.layout import create_layout
from components.callbacks import register_callbacks
from components.theme import register_theme_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "BTC Signal Dashboard"
app._favicon = "btc.ico"

app.layout = create_layout(app)

register_callbacks(app)
register_theme_callbacks(app)

server = app.server

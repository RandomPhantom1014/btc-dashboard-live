# dashboard.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.layout import create_layout
from components.callbacks import register_callbacks

# Initialize the Dash app with Bootstrap and custom CSS
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder="assets"
)

# App metadata
app.title = "BTC Signal Dashboard"
app._favicon = "btc.ico"

# Set layout
app.layout = create_layout(app)

# Register callbacks
register_callbacks(app)

# Expose server for deployment
server = app.server


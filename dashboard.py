# dashboard.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.layout import create_layout
from components.callbacks import register_callbacks

# Initialize the Dash app with Bootstrap for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "BTC Signal Dashboard"
app._favicon = "btc.ico"

# Set the layout
app.layout = create_layout()  # ✅ FIXED: Removed 'app' argument

# Register all app callbacks
register_callbacks(app)

# Expose the app’s server for Render to find it
server = app.server

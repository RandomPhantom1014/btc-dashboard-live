import dash
from dash import html, dcc
from flask import Flask
from components.layout import create_layout
from callbacks import register_callbacks
import dash_bootstrap_components as dbc

# Setup server for Render compatibility
server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]  # Important for responsive layout
)

# Inject layout and callbacks
app.title = "BTC Signal Dashboard"
app.layout = create_layout()
register_callbacks(app)

# Run app locally
if __name__ == "__main__":
    app.run_server(debug=True)

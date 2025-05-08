# app.py

import dash
from dash import html, dcc
from flask import Flask
from components.layout import create_layout
from callbacks import register_callbacks

# Setup server for Render compatibility
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

# Inject layout and callbacks
app.title = "BTC Signal Dashboard"
app.layout = create_layout()
register_callbacks(app)

# Run app locally (ignored by Render)
if __name__ == "__main__":
    app.run_server(debug=True)

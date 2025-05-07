# dashboard.py

import dash
from dash import dcc
import dash_bootstrap_components as dbc
from components.layout import create_layout
from components.callbacks import register_callbacks

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    assets_folder="assets"
)
app.title = "BTC Signal Dashboard"
app._favicon = "btc.ico"  # Ensure 'btc.ico' is present in the assets folder

# Set the app layout
app.layout = create_layout(app)

# Register callbacks (including WebSocket handlers and UI updates)
register_callbacks(app)

# Expose server for Render
server = app.server

# Run locally (optional, for development/testing)
if __name__ == "__main__":
    app.run_server(debug=True)

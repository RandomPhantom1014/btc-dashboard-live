# dashboard.py

import dash
from dash import html
from components.layout import create_layout

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Set the layout using the function (no arguments needed)
app.layout = create_layout()

# For deployment with gunicorn
server = app.server

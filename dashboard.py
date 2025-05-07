# dashboard.py

import dash
import dash_bootstrap_components as dbc
from components.layout import create_layout
from components.callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "BTC Signal Dashboard"
app._favicon = "btc.ico"
app.layout = create_layout()
register_callbacks(app)
server = app.server

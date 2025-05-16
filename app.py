from dash import Dash
from layout import serve_layout
import callbacks  # <-- this ensures callbacks run but no import of register_callbacks

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = serve_layout

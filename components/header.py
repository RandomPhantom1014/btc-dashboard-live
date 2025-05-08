# components/header.py

from dash import html

def render_header():
    return html.Div([
        html.H2("BTC Signal Dashboard", className="header-title"),
        html.Hr()
    ], className="header-container")

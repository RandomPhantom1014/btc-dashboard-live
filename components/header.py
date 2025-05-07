# components/header.py

from dash import html

def render_header():
    return html.Div(
        children=[
            html.H1("BTC Signal Dashboard", className="header-title"),
            html.Hr(className="header-divider")
        ],
        className="header-container"
    )

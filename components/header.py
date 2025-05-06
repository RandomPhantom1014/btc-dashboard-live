# components/header.py

from dash import html

def build_header():
    return html.Div(
        className="dashboard-header",
        children=[
            html.H1("BTC Signal Dashboard", className="dashboard-title"),
            html.Div(
                className="mode-toggle",
                children=[
                    html.Label("Dark Mode"),
                    html.Input(type="checkbox", id="theme-toggle", className="theme-toggle")
                ]
            )
        ]
    )

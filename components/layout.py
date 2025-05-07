# components/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
from components.styles import card_style
from components.chart import render_candlestick_chart
from components.indicators import render_indicators
from components.strength_meter import render_strength_meter

def create_layout(app):
    return html.Div(
        id="theme-container",
        className="light-mode",
        children=[
            dbc.Container([
                html.Div([
                    dbc.Switch(
                        id="theme-toggle",
                        label="Dark Mode",
                        value=False,
                        className="mb-3 float-end"
                    )
                ]),
                html.H1("BTC Signal Dashboard", className="text-center mb-4"),

                render_candlestick_chart(),

                render_indicators(),

                dbc.Row([
                    dbc.Col(render_strength_meter("5m"), width=4),
                    dbc.Col(render_strength_meter("10m"), width=4),
                    dbc.Col(render_strength_meter("15m"), width=4)
                ], className="mb-4"),

                dcc.Interval(id="interval-component", interval=5000, n_intervals=0)
            ], fluid=True)
        ]
    )

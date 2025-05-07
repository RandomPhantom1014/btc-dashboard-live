# components/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
from components.styles import card_style

def create_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("BTC Signal Dashboard", className="text-center text-white mb-4"), width=12)
        ]),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Live BTC Price", className="bg-dark text-white"),
                dbc.CardBody(html.H4(id="live-btc-price", className="card-title"))
            ], style=card_style), md=4, sm=12),

            dbc.Col(dbc.Card([
                dbc.CardHeader("5m Signal", className="bg-dark text-white"),
                dbc.CardBody([
                    html.Div(id="signal-5m"),
                    html.Div(id="confidence-5m"),
                    html.Div(id="strength-5m", className="pill-container")
                ])
            ], style=card_style), md=4, sm=12),

            dbc.Col(dbc.Card([
                dbc.CardHeader("10m Signal", className="bg-dark text-white"),
                dbc.CardBody([
                    html.Div(id="signal-10m"),
                    html.Div(id="confidence-10m"),
                    html.Div(id="strength-10m", className="pill-container")
                ])
            ], style=card_style), md=4, sm=12),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("15m Signal", className="bg-dark text-white"),
                dbc.CardBody([
                    html.Div(id="signal-15m"),
                    html.Div(id="confidence-15m"),
                    html.Div(id="strength-15m", className="pill-container")
                ])
            ], style=card_style), md=4, sm=12),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(html.Div(id="candlestick-chart"), width=12),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(html.Div(id="indicator-charts"), width=12),
        ], className="mb-4"),

        dcc.Interval(id="interval-component", interval=5000, n_intervals=0)
    ], fluid=True)

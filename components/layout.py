# components/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
from components.styles import card_style

def create_layout():
    return dbc.Container([
        html.H1("BTC Signal Dashboard", className="text-center mb-4"),

        # Toggle between Live and Backtest
        dbc.Row([
            dbc.Col([
                dbc.Label("Signal Mode"),
                dcc.RadioItems(
                    id="mode-toggle",
                    options=[
                        {"label": "Live", "value": "live"},
                        {"label": "Backtest", "value": "backtest"}
                    ],
                    value="live",
                    labelStyle={"display": "inline-block", "margin-right": "15px"},
                    inputStyle={"margin-right": "5px"}
                )
            ])
        ], className="mb-3"),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Live BTC Price"),
                dbc.CardBody(html.H4(id="live-btc-price", className="card-title"))
            ], style=card_style), width=4),

            dbc.Col(dbc.Card([
                dbc.CardHeader("5m Signal"),
                dbc.CardBody([
                    html.Div(id="signal-5m"),
                    html.Div(id="confidence-5m"),
                    html.Div(id="strength-5m")
                ])
            ], style=card_style), width=4),

            dbc.Col(dbc.Card([
                dbc.CardHeader("10m Signal"),
                dbc.CardBody([
                    html.Div(id="signal-10m"),
                    html.Div(id="confidence-10m"),
                    html.Div(id="strength-10m")
                ])
            ], style=card_style), width=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("15m Signal"),
                dbc.CardBody([
                    html.Div(id="signal-15m"),
                    html.Div(id="confidence-15m"),
                    html.Div(id="strength-15m")
                ])
            ], style=card_style), width=4),
        ]),

        dcc.Interval(id="interval-component", interval=5000, n_intervals=0)
    ], fluid=True)


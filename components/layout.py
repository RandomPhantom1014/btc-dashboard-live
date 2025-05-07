# components/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
from components.styles import card_style, pill_styles


def create_layout():
    return dbc.Container([
        html.H1("BTC Signal Dashboard", className="text-center mb-4", style={"color": "aqua"}),

        # Row 1: Candlestick chart
        dbc.Row([
            dbc.Col(dcc.Graph(id="candlestick-chart"), width=12),
        ], className="mb-4"),

        # Row 2: RSI, MACD, Volume charts
        dbc.Row([
            dbc.Col(dcc.Graph(id="rsi-chart"), width=4),
            dbc.Col(dcc.Graph(id="macd-chart"), width=4),
            dbc.Col(dcc.Graph(id="volume-chart"), width=4),
        ], className="mb-4"),

        # Row 3: Live BTC price and signal cards
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

        # Row 4: 15m Signal
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("15m Signal"),
                dbc.CardBody([
                    html.Div(id="signal-15m"),
                    html.Div(id="confidence-15m"),
                    html.Div(id="strength-15m")
                ])
            ], style=card_style), width=4),

            # Backtest / Live toggle
            dbc.Col(dbc.Card([
                dbc.CardHeader("Data Mode"),
                dbc.CardBody([
                    dcc.RadioItems(
                        id="mode-toggle",
                        options=[
                            {"label": "Live", "value": "live"},
                            {"label": "Backtest", "value": "backtest"},
                        ],
                        value="live",
                        labelStyle={"display": "block", "color": "white"}
                    )
                ])
            ], style=card_style), width=4),
        ], className="mb-4"),

        dcc.Interval(id="interval-component", interval=5000, n_intervals=0)
    ], fluid=True)

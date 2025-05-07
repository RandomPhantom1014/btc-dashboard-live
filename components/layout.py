# components/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
from components.styles import card_style
from components.chart import render_candlestick_chart
from components.indicators import render_indicators

def create_layout():
    return dbc.Container([
        html.H1("BTC Signal Dashboard", className="text-center mb-4"),

        # Toggle for Live / Backtest
        dbc.Row([
            dbc.Col(dbc.RadioItems(
                id="mode-toggle",
                options=[
                    {"label": "Live Mode", "value": "live"},
                    {"label": "Backtest Mode", "value": "backtest"}
                ],
                value="live",
                inline=True,
                labelStyle={"marginRight": "20px"},
                inputStyle={"marginRight": "8px"},
                className="mb-3 text-light"
            ), width="auto"),
        ], justify="center"),

        # Live BTC Price
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Live BTC Price"),
                dbc.CardBody(html.H4(id="live-btc-price", className="card-title"))
            ], style=card_style), width=12)
        ], className="mb-4"),

        # Candlestick Chart
        dbc.Row([
            dbc.Col(render_candlestick_chart(), width=12)
        ], className="mb-4"),

        # Indicators
        dbc.Row([
            dbc.Col(render_indicators(), width=12)
        ], className="mb-4"),

        # Signal Cards
        dbc.Row([
            *[
                dbc.Col(dbc.Card([
                    dbc.CardHeader(f"{tf.upper()} Signal"),
                    dbc.CardBody([
                        html.Div(id=f"signal-{tf}"),
                        html.Div(id=f"confidence-{tf}"),
                        html.Div(id=f"strength-{tf}", className="pill-placeholder")
                    ])
                ], style=card_style), width=4)
                for tf in ["5m", "10m", "15m"]
            ]
        ], className="mb-4"),

        # Update interval
        dcc.Interval(id="interval-component", interval=5000, n_intervals=0)
    ], fluid=True)

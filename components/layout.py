# components/layout.py

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd

from components.header import render_header
from components.indicators import render_indicators
from components.strength_meter import render_strength_meter

def create_layout():
    return dbc.Container(
        [
            dcc.Interval(id="interval-component", interval=10*1000, n_intervals=0),

            # Header
            render_header(),

            # Live BTC Price (replaces chart)
            html.Div(id="live-btc-price", className="live-price", style={
                "fontSize": "36px",
                "fontWeight": "bold",
                "textAlign": "center",
                "marginBottom": "20px"
            }),

            # RSI, MACD, Volume Indicators
            html.Div(render_indicators(), className="indicators-container"),

            # Signal Mode Toggle (Live vs Backtest)
            html.Div(
                [
                    html.Label("Signal Mode:"),
                    dcc.RadioItems(
                        id="mode-toggle",
                        options=[
                            {"label": "Live", "value": "live"},
                            {"label": "Backtest", "value": "backtest"},
                        ],
                        value="live",
                        inline=True,
                        labelStyle={"marginRight": "15px"}
                    ),
                ],
                className="mode-toggle"
            ),

            # Signal Outputs for Each Timeframe
            html.Div([
                dbc.Row([
                    dbc.Col(html.Div("5 Minute Signal", className="timeframe-title"), width=12),
                    dbc.Col(html.Div(id="signal-5m", className="signal-pill"), width=4),
                    dbc.Col(html.Div(id="confidence-5m", className="confidence"), width=4),
                    dbc.Col(html.Div(render_strength_meter("5m"), id="strength-5m"), width=4),
                ], className="signal-row"),

                dbc.Row([
                    dbc.Col(html.Div("10 Minute Signal", className="timeframe-title"), width=12),
                    dbc.Col(html.Div(id="signal-10m", className="signal-pill"), width=4),
                    dbc.Col(html.Div(id="confidence-10m", className="confidence"), width=4),
                    dbc.Col(html.Div(render_strength_meter("10m"), id="strength-10m"), width=4),
                ], className="signal-row"),

                dbc.Row([
                    dbc.Col(html.Div("15 Minute Signal", className="timeframe-title"), width=12),
                    dbc.Col(html.Div(id="signal-15m", className="signal-pill"), width=4),
                    dbc.Col(html.Div(id="confidence-15m", className="confidence"), width=4),
                    dbc.Col(html.Div(render_strength_meter("15m"), id="strength-15m"), width=4),
                ], className="signal-row"),
            ]),

            # CSV Export Button
            html.Div(
                dbc.Button("Export CSV", id="export-button", color="primary", className="mt-3"),
                className="export-container"
            ),

            # Log Saving Toggle
            html.Div(
                dbc.Checkbox(
                    id="save-logs-toggle",
                    className="mt-2",
                    value=False
                ),
                className="log-toggle"
            ),
        ],
        fluid=True,
        className="main-container"
    )

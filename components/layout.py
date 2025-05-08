# components/layout.py

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd

from components.header import render_header
from components.chart import render_candlestick_chart
from components.indicators import render_indicators
from components.strength_meter import render_strength_meter

def create_layout(theme="light"):
    return dbc.Container(
        [
            dcc.Location(id="url", refresh=False),
            dcc.Interval(id="interval-component", interval=10*1000, n_intervals=0),

            render_header(),

            html.Div(id="live-btc-price", className="live-price"),

            html.Div(
                dcc.Graph(id="candlestick-chart"),
                className="chart-container"
            ),

            html.Div(
                id="indicators-container",
                className="indicators-container"
            ),

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
                        inline=True
                    )
                ],
                className="mode-toggle"
            ),

            # === Signal Outputs ===
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

            html.Div(
                dbc.Button("Export CSV", id="export-button", color="primary", className="mt-3"),
                className="export-container"
            ),

            html.Div(
                dbc.Checkbox(id="save-logs-toggle", className="mt-2", value=False),
                className="log-toggle"
            ),

            html.Div([
                html.Label("Theme:"),
                dcc.RadioItems(
                    id="theme-toggle",
                    options=[
                        {"label": "Light", "value": "light"},
                        {"label": "Dark", "value": "dark"}
                    ],
                    value="light",
                    inline=True
                )
            ], className="theme-toggle")
        ],
        fluid=True,
        className=f"{theme} main-container"
    )

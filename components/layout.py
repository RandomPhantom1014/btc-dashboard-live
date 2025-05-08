# components/layout.py

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd

from components.header import render_header

def create_layout():
    return dbc.Container([
        dcc.Interval(id="interval-component", interval=15 * 1000, n_intervals=0),

        # Header
        render_header(),

        # Theme Toggle
        html.Div([
            html.Label("Theme:"),
            dcc.RadioItems(
                id="theme-toggle",
                options=[
                    {"label": "Light", "value": "light"},
                    {"label": "Dark", "value": "dark"},
                ],
                value="light",
                inline=True,
                labelStyle={"margin-right": "15px"}
            ),
        ], className="theme-toggle"),

        # Mode Toggle
        html.Div([
            html.Label("Signal Mode:"),
            dcc.RadioItems(
                id="signal-mode",
                options=[
                    {"label": "Live", "value": "live"},
                    {"label": "Backtest", "value": "backtest"},
                ],
                value="backtest",
                inline=True,
                labelStyle={"margin-right": "15px"}
            ),
        ], className="mode-toggle"),

        # Live BTC Price Display
        html.Div(id="live-btc-price", className="live-price"),

        # Candlestick Chart
        html.Div([
            dcc.Graph(id="candlestick-chart", config={"displayModeBar": False}),
        ], className="chart-container"),

        # Signal Output: 5 Minute
        html.Div([
            html.H5("5 Minute Signal"),
            html.Div(id="five-min-signal", className="signal-pill")
        ], className="signal-section"),

        # Signal Output: 10 Minute
        html.Div([
            html.H5("10 Minute Signal"),
            html.Div(id="ten-min-signal", className="signal-pill")
        ], className="signal-section"),

        # Signal Output: 15 Minute
        html.Div([
            html.H5("15 Minute Signal"),
            html.Div(id="fifteen-min-signal", className="signal-pill")
        ], className="signal-section"),

        # CSV Export
        html.Div(
            dbc.Button("Export CSV", id="export-button", color="primary", className="mt-3"),
            className="export-container"
        ),

        # Log Saving Toggle
        html.Div(
            dbc.Checkbox(id="save-logs-toggle", value=False, className="mt-2"),
            className="log-toggle"
        )
    ], fluid=True, className="main-container")


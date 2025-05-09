# components/layout.py

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from components.header import render_header
from components.strength_meter import render_strength_meter

def signal_block(timeframe):
    return dbc.Col([
        html.Div(f"{timeframe} Signal", className="timeframe-title"),
        html.Div(id=f"signal-{timeframe}", className="signal-pill"),
        html.Div(id=f"confidence-{timeframe}", className="confidence"),
        html.Div(render_strength_meter(timeframe), id=f"strength-{timeframe}", className="strength-meter"),
        html.Div(id=f"timestamp-{timeframe}", className="timestamp"),
        html.Div(id=f"countdown-{timeframe}", className="countdown")
    ], className="signal-col", width=6)

def create_layout():
    return dbc.Container([
        dcc.Interval(id="interval-component", interval=10*1000, n_intervals=0),

        # Header
        render_header(),

        # Live BTC Price
        html.Div(id="live-btc-price", className="live-price"),

        # Mode Toggle
        html.Div([
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
        ], className="mode-toggle"),

        # Signals Block (Side-by-side rows, each with short + long timeframe)
        dbc.Row([
            signal_block("5m"),
            signal_block("1h"),
        ], className="signal-row"),
        dbc.Row([
            signal_block("10m"),
            signal_block("6h"),
        ], className="signal-row"),
        dbc.Row([
            signal_block("15m"),
            signal_block("12h"),
        ], className="signal-row"),
        dbc.Row([
            dbc.Col([], width=6),
            signal_block("24h"),
        ], className="signal-row"),

        # Export Button
        html.Div(
            dbc.Button("Export CSV", id="export-button", color="primary", className="mt-3"),
            className="export-container"
        ),

        # Log Toggle
        html.Div(
            dbc.Checkbox(
                id="save-logs-toggle",
                className="mt-2",
                value=False
            ),
            className="log-toggle"
        )
    ], fluid=True, className="main-container")



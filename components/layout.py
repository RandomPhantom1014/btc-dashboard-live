import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from components.header import render_header
from components.strength_meter import render_strength_meter

def create_layout():
    return dbc.Container(
        [
            dcc.Interval(id="interval-component", interval=10 * 1000, n_intervals=0),
            render_header(),

            # Live BTC Price
            html.Div(id="live-btc-price", className="live-price"),

            # Mode Toggle
            html.Div([
                html.Label("Signal Mode:"),
                dcc.RadioItems(
                    id="mode-toggle",
                    options=[{"label": "Live", "value": "live"}, {"label": "Backtest", "value": "backtest"}],
                    value="live",
                    inline=True,
                    labelStyle={"marginRight": "15px"}
                ),
            ], className="mode-toggle"),

            # Signal Rows
            html.Div([
                dbc.Row([
                    dbc.Col(html.Div("5 Minute Signal", className="timeframe-title"), width=12),
                    dbc.Col(html.Div(id="signal-5m", className="signal-pill"), width=12),
                    dbc.Col(html.Div(id="confidence-5m", className="confidence"), width=12),
                    dbc.Col(html.Div(id="strength-5m", className="strength-meter"), width=12),
                ], className="signal-row"),

                dbc.Row([
                    dbc.Col(html.Div("10 Minute Signal", className="timeframe-title"), width=12),
                    dbc.Col(html.Div(id="signal-10m", className="signal-pill"), width=12),
                    dbc.Col(html.Div(id="confidence-10m", className="confidence"), width=12),
                    dbc.Col(html.Div(id="strength-10m", className="strength-meter"), width=12),
                ], className="signal-row"),

                dbc.Row([
                    dbc.Col(html.Div("15 Minute Signal", className="timeframe-title"), width=12),
                    dbc.Col(html.Div(id="signal-15m", className="signal-pill"), width=12),
                    dbc.Col(html.Div(id="confidence-15m", className="confidence"), width=12),
                    dbc.Col(html.Div(id="strength-15m", className="strength-meter"), width=12),
                ], className="signal-row"),
            ]),

            html.Div(dbc.Button("Export CSV", id="export-button", color="primary", className="mt-3"), className="export-container"),
            html.Div(dbc.Checkbox(id="save-logs-toggle", className="mt-2", value=False), className="log-toggle")
        ],
        fluid=True,
        className="main-container"
    )


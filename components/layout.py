# components/layout.py

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from components.header import render_header
from components.strength_meter import render_strength_meter

def create_layout():
    return dbc.Container(
        [
            dcc.Interval(id="interval-component", interval=10*1000, n_intervals=0),

            render_header(),

            html.Div(id="live-btc-price", className="live-price"),

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

            dbc.Row([
                # Left Column (Short-Term)
                dbc.Col([
                    *generate_signal_block("5 Minute", "5m"),
                    *generate_signal_block("10 Minute", "10m"),
                    *generate_signal_block("15 Minute", "15m")
                ], md=6),

                # Right Column (Long-Term)
                dbc.Col([
                    *generate_signal_block("1 Hour", "1h"),
                    *generate_signal_block("6 Hour", "6h"),
                    *generate_signal_block("12 Hour", "12h"),
                    *generate_signal_block("24 Hour", "24h")
                ], md=6),
            ]),

            html.Div(
                dbc.Button("Export CSV", id="export-button", color="primary", className="mt-3"),
                className="export-container"
            ),

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


def generate_signal_block(label, key):
    return [
        html.Div([
            html.Div(f"{label} Signal", className="timeframe-title"),
            dbc.Row([
                dbc.Col(html.Div(id=f"signal-{key}", className="signal-pill"), width=4),
                dbc.Col(html.Div(id=f"confidence-{key}", className="confidence"), width=4),
                dbc.Col(html.Div(render_strength_meter(key), id=f"strength-{key}"), width=4),
            ]),
            dbc.Row([
                dbc.Col(html.Div(id=f"timestamp-{key}", className="timestamp"), width=6),
                dbc.Col(html.Div(id=f"countdown-{key}", className="countdown"), width=6)
            ])
        ], className="signal-row")
    ]

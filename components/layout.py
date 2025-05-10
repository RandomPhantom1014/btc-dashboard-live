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

                # Left Column: Short-term Signals
                dbc.Col([
                    create_signal_block("5m"),
                    create_signal_block("10m"),
                    create_signal_block("15m"),
                ], md=6),

                # Right Column: Long-term Signals
                dbc.Col([
                    create_signal_block("1h"),
                    create_signal_block("6h"),
                    create_signal_block("12h"),
                    create_signal_block("24h"),
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

def create_signal_block(timeframe):
    return html.Div([
        html.Div(f"{timeframe.upper()} Signal", className="timeframe-title"),

        dbc.Row([
            dbc.Col(html.Div(id=f"signal-{timeframe}", className="signal-pill"), width=4),
            dbc.Col(html.Div(id=f"confidence-{timeframe}", className="confidence"), width=4),
            dbc.Col(html.Div(render_strength_meter(timeframe), id=f"strength-{timeframe}"), width=4),
        ]),

        dbc.Row([
            dbc.Col(html.Div(id=f"timestamp-{timeframe}", className="timestamp"), width=6),
            dbc.Col(html.Div(id=f"countdown-{timeframe}", className="countdown"), width=6),
        ]),
    ], className="signal-row")

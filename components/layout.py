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

            dbc.Row([
                dbc.Col([  # SHORT-TERM
                    html.Div("Short-Term Signals", className="timeframe-title"),
                    *[build_signal_block(tf) for tf in ["5m", "10m", "15m"]]
                ], md=6, xs=12),

                dbc.Col([  # LONG-TERM
                    html.Div("Futures Signals", className="timeframe-title"),
                    *[build_signal_block(tf) for tf in ["1h", "6h", "12h", "24h"]]
                ], md=6, xs=12),
            ]),

            html.Div(
                dbc.Button("Export CSV", id="export-button", color="primary", className="mt-3"),
                className="export-container"
            ),
            html.Div(
                dbc.Checkbox(id="save-logs-toggle", className="mt-2", value=False),
                className="log-toggle"
            )
        ],
        fluid=True,
        className="main-container"
    )

def build_signal_block(tf):
    return html.Div([
        html.Div(f"{tf.upper()} Signal", className="timeframe-title"),
        dbc.Row([
            dbc.Col(html.Div(id=f"signal-{tf}", className="signal-pill"), width=4),
            dbc.Col(html.Div(id=f"confidence-{tf}", className="confidence"), width=4),
            dbc.Col(render_strength_meter(tf), width=4),
        ]),
        dbc.Row([
            dbc.Col(html.Div(id=f"timestamp-{tf}", className="timestamp"), width=6),
            dbc.Col(html.Div(id=f"countdown-{tf}", className="countdown"), width=6),
        ]),
    ], className="signal-row")

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from components.header import render_header
from components.strength_meter import render_strength_meter

def create_layout():
    return dbc.Container(
        [
            dcc.Interval(id="interval-component", interval=10*1000, n_intervals=0),

            # Header
            render_header(),

            # Live BTC Price
            html.Div(id="live-btc-price", className="live-price"),

            # Mode toggle (Live / Backtest)
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
                # Short-Term Signals (Left Column)
                dbc.Col([
                    html.Div("SHORT-TERM SIGNALS", className="timeframe-title"),
                    *[dbc.Row([
                        dbc.Col(html.Div(f"{label} Signal", className="timeframe-title"), width=12),
                        dbc.Col(html.Div(id=f"signal-{key}", className="signal-pill"), width=4),
                        dbc.Col(html.Div(id=f"confidence-{key}", className="confidence"), width=4),
                        dbc.Col(html.Div(render_strength_meter(key), id=f"strength-{key}"), width=4),
                    ], className="signal-row") for key, label in [("5m", "5 Minute"), ("10m", "10 Minute"), ("15m", "15 Minute")]]
                ], md=6),

                # Long-Term Futures Signals (Right Column)
                dbc.Col([
                    html.Div("FUTURES SIGNALS", className="timeframe-title"),
                    *[dbc.Row([
                        dbc.Col(html.Div(f"{label} Signal", className="timeframe-title"), width=12),
                        dbc.Col(html.Div(id=f"signal-{key}", className="signal-pill"), width=4),
                        dbc.Col(html.Div(id=f"confidence-{key}", className="confidence"), width=4),
                        dbc.Col(html.Div(render_strength_meter(key), id=f"strength-{key}"), width=4),
                    ], className="signal-row") for key, label in [("1h", "1 Hour"), ("6h", "6 Hour"), ("12h", "12 Hour"), ("24h", "24 Hour")]]
                ], md=6),
            ]),

            # Export CSV Button
            html.Div(
                dbc.Button("Export CSV", id="export-button", color="primary", className="mt-3"),
                className="export-container"
            ),

            # Save Logs Toggle
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

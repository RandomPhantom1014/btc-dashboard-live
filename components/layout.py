import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from components.header import render_header
from components.strength_meter import render_strength_meter

def create_signal_row(timeframe):
    return dbc.Row([
        dbc.Col(html.Div(f"{timeframe} Signal", className="timeframe-title"), width=12),
        dbc.Col(html.Div(id=f"signal-{timeframe}", className="signal-pill"), width=4),
        dbc.Col(html.Div(id=f"confidence-{timeframe}", className="confidence"), width=4),
        dbc.Col(html.Div(render_strength_meter(timeframe), id=f"strength-{timeframe}"), width=4),
    ], className="signal-row")

def create_layout():
    return dbc.Container(
        [
            dcc.Interval(id="interval-component", interval=10 * 1000, n_intervals=0),

            # Header
            render_header(),

            # Live BTC Price (text instead of chart)
            html.Div(id="live-btc-price", className="live-price"),

            # Mode toggle (Live or Backtest)
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

            # Main Split Layout: Short-Term Left | Futures Right
            dbc.Row([
                # Left: Short-Term Signals
                dbc.Col([
                    create_signal_row("5m"),
                    create_signal_row("10m"),
                    create_signal_row("15m"),
                ], xs=12, md=6),

                # Right: Futures Signals
                dbc.Col([
                    create_signal_row("1h"),
                    create_signal_row("6h"),
                    create_signal_row("12h"),
                    create_signal_row("24h"),
                ], xs=12, md=6)
            ]),

            # Export & Logging
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
            )
        ],
        fluid=True,
        className="main-container"
    )

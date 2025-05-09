import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from components.header import render_header
from components.strength_meter import render_strength_meter

def create_layout():
    return dbc.Container(
        [
            dcc.Interval(id="interval-component", interval=10 * 1000, n_intervals=0),

            # Header
            render_header(),

            # Live BTC Price
            html.Div(id="live-btc-price", className="live-price"),

            # Signal Mode Toggle
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
                        labelStyle={"marginRight": "15px"},
                    ),
                ],
                className="mode-toggle"
            ),

            # Side-by-side signal columns
            dbc.Row([
                # Left Column - Short-Term
                dbc.Col([
                    html.Div("Short-Term Signals", className="timeframe-title"),

                    # 5m
                    dbc.Row([
                        dbc.Col(html.Div("5 Minute Signal", className="timeframe-title"), width=12),
                        dbc.Col(html.Div(id="signal-5m", className="signal-pill"), width=4),
                        dbc.Col(html.Div(id="confidence-5m", className="confidence"), width=4),
                        dbc.Col(html.Div(render_strength_meter("5m"), id="strength-5m"), width=4),
                        dbc.Col(html.Div(id="timestamp-5m", className="timestamp"), width=6),
                        dbc.Col(html.Div(id="countdown-5m", className="countdown"), width=6),
                    ], className="signal-row"),

                    # 10m
                    dbc.Row([
                        dbc.Col(html.Div("10 Minute Signal", className="timeframe-title"), width=12),
                        dbc.Col(html.Div(id="signal-10m", className="signal-pill"), width=4),
                        dbc.Col(html.Div(id="confidence-10m", className="confidence"), width=4),
                        dbc.Col(html.Div(render_strength_meter("10m"), id="strength-10m"), width=4),
                        dbc.Col(html.Div(id="timestamp-10m", className="timestamp"), width=6),
                        dbc.Col(html.Div(id="countdown-10m", className="countdown"), width=6),
                    ], className="signal-row"),

                    # 15m
                    dbc.Row([
                        dbc.Col(html.Div("15 Minute Signal", className="timeframe-title"), width=12),
                        dbc.Col(html.Div(id="signal-15m", className="signal-pill"), width=4),
                        dbc.Col(html.Div(id="confidence-15m", className="confidence"), width=4),
                        dbc.Col(html.Div(render_strength_meter("15m"), id="strength-15m"), width=4),
                        dbc.Col(html.Div(id="timestamp-15m", className="timestamp"), width=6),
                        dbc.Col(html.Div(id="countdown-15m", className="countdown"), width=6),
                    ], className="signal-row"),

                ], md=6),  # Left half column

                # Right Column - Long-Term
                dbc.Col([
                    html.Div("Futures Signals", className="timeframe-title"),

                    # 1h
                    dbc.Row([
                        dbc.Col(html.Div("1 Hour Signal", className="timeframe-title"), width=12),
                        dbc.Col(html.Div(id="signal-1h", className="signal-pill"), width=4),
                        dbc.Col(html.Div(id="confidence-1h", className="confidence"), width=4),
                        dbc.Col(html.Div(render_strength_meter("1h"), id="strength-1h"), width=4),
                        dbc.Col(html.Div(id="timestamp-1h", className="timestamp"), width=6),
                        dbc.Col(html.Div(id="countdown-1h", className="countdown"), width=6),
                    ], className="signal-row"),

                    # 6h
                    dbc.Row([
                        dbc.Col(html.Div("6 Hour Signal", className="timeframe-title"), width=12),
                        dbc.Col(html.Div(id="signal-6h", className="signal-pill"), width=4),
                        dbc.Col(html.Div(id="confidence-6h", className="confidence"), width=4),
                        dbc.Col(html.Div(render_strength_meter("6h"), id="strength-6h"), width=4),
                        dbc.Col(html.Div(id="timestamp-6h", className="timestamp"), width=6),
                        dbc.Col(html.Div(id="countdown-6h", className="countdown"), width=6),
                    ], className="signal-row"),

                    # 12h
                    dbc.Row([
                        dbc.Col(html.Div("12 Hour Signal", className="timeframe-title"), width=12),
                        dbc.Col(html.Div(id="signal-12h", className="signal-pill"), width=4),
                        dbc.Col(html.Div(id="confidence-12h", className="confidence"), width=4),
                        dbc.Col(html.Div(render_strength_meter("12h"), id="strength-12h"), width=4),
                        dbc.Col(html.Div(id="timestamp-12h", className="timestamp"), width=6),
                        dbc.Col(html.Div(id="countdown-12h", className="countdown"), width=6),
                    ], className="signal-row"),

                    # 24h
                    dbc.Row([
                        dbc.Col(html.Div("24 Hour Signal", className="timeframe-title"), width=12),
                        dbc.Col(html.Div(id="signal-24h", className="signal-pill"), width=4),
                        dbc.Col(html.Div(id="confidence-24h", className="confidence"), width=4),
                        dbc.Col(html.Div(render_strength_meter("24h"), id="strength-24h"), width=4),
                        dbc.Col(html.Div(id="timestamp-24h", className="timestamp"), width=6),
                        dbc.Col(html.Div(id="countdown-24h", className="countdown"), width=6),
                    ], className="signal-row"),
                ], md=6),  # Right half column
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

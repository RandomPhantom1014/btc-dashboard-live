# components/layout.py

from dash import html, dcc

def layout():
    return html.Div([
        html.H1("🚀 BTC Signal Dashboard", className="dashboard-title"),

        # BTC Price Chart and Signal Outputs Side-by-Side
        html.Div([
            # Left: BTC Candlestick Chart + Timeframe Toggle
            html.Div([
                html.Div([
                    html.H3("Live BTC Price Chart", className="chart-title"),
                    dcc.RadioItems(
                        id='timeframe-selector',
                        options=[
                            {'label': '5 min', 'value': '5m'},
                            {'label': '10 min', 'value': '10m'},
                            {'label': '15 min', 'value': '15m'},
                        ],
                        value='5m',
                        labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                        className="timeframe-toggle"
                    ),
                ], className="chart-header"),

                dcc.Graph(id='btc-price-chart', className="price-chart")
            ], className="chart-container"),

            # Right: Signals
            html.Div([
                html.H3("Signal Output", className="section-title"),

                html.Div([
                    html.Div([
                        html.P("5-Minute", className="signal-label"),
                        html.Div(id='signal-5m', className="signal-pill"),
                        html.Div(id='confidence-5m', className="confidence-text")
                    ], className="signal-row"),

                    html.Div([
                        html.P("10-Minute", className="signal-label"),
                        html.Div(id='signal-10m', className="signal-pill"),
                        html.Div(id='confidence-10m', className="confidence-text")
                    ], className="signal-row"),

                    html.Div([
                        html.P("15-Minute", className="signal-label"),
                        html.Div(id='signal-15m', className="signal-pill"),
                        html.Div(id='confidence-15m', className="confidence-text")
                    ], className="signal-row"),

                    html.Div([
                        html.P("Strength Meter"),
                        html.Div(id="strength-meter")
                    ], className="strength-box"),
                ])
            ], className="signal-panel"),
        ], className="main-grid"),

        # Indicators Below
        html.Div([
            html.Div([
                html.H4("RSI"),
                dcc.Graph(id='rsi-chart', className="indicator-graph")
            ], className="indicator-box"),

            html.Div([
                html.H4("MACD"),
                dcc.Graph(id='macd-chart', className="indicator-graph")
            ], className="indicator-box"),

            html.Div([
                html.H4("Volume"),
                dcc.Graph(id='volume-chart', className="indicator-graph")
            ], className="indicator-box"),
        ], className="indicator-grid"),

        # Mode and Theme Toggles
        html.Div([
            html.Div([
                html.Label("Mode"),
                dcc.RadioItems(
                    id='mode-toggle',
                    options=[
                        {'label': 'Live', 'value': 'live'},
                        {'label': 'Backtest', 'value': 'backtest'}
                    ],
                    value='live',
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'}
                )
            ], className="toggle-section"),

            html.Div([
                html.Label("Theme"),
                dcc.RadioItems(
                    id='theme-toggle',
                    options=[
                        {'label': 'Light', 'value': 'light'},
                        {'label': 'Dark', 'value': 'dark'}
                    ],
                    value='light',
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'}
                )
            ], className="toggle-section"),
        ], className="toggles-container"),

        dcc.Interval(
            id='interval-component',
            interval=30 * 1000,
            n_intervals=0
        )
    ], id='main-container')

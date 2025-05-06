import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("BTC Signal Dashboard", className="text-center mb-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="candlestick-chart", config={"displayModeBar": False})
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div("RSI", className="indicator-label"),
            dcc.Graph(id="rsi-chart", config={"displayModeBar": False})
        ], width=4),
        dbc.Col([
            html.Div("MACD", className="indicator-label"),
            dcc.Graph(id="macd-chart", config={"displayModeBar": False})
        ], width=4),
        dbc.Col([
            html.Div("Volume", className="indicator-label"),
            dcc.Graph(id="volume-chart", config={"displayModeBar": False})
        ], width=4)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H5("5-Min Signal"),
            html.Div(id="signal-5m"),
            html.Div(id="confidence-5m"),
            html.Div(id="price-5m")
        ], width=4),
        dbc.Col([
            html.H5("10-Min Signal"),
            html.Div(id="signal-10m"),
            html.Div(id="confidence-10m"),
            html.Div(id="price-10m")
        ], width=4),
        dbc.Col([
            html.H5("15-Min Signal"),
            html.Div(id="signal-15m"),
            html.Div(id="confidence-15m"),
            html.Div(id="price-15m")
        ], width=4)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Label("Mode:"),
            dcc.RadioItems(
                id="mode-toggle",
                options=[
                    {"label": "Live", "value": "live"},
                    {"label": "Backtest", "value": "backtest"}
                ],
                value="live",
                inline=True
            )
        ], width=6),
        dbc.Col([
            html.Label("Dark Mode:"),
            dbc.Switch(id="theme-toggle", value=False, className="float-end")
        ], width=6)
    ])
], fluid=True)

def register_callbacks(app):
    @app.callback(
        dash.dependencies.Output("signal-5m", "children"),
        dash.dependencies.Output("confidence-5m", "children"),
        dash.dependencies.Output("price-5m", "children"),
        dash.dependencies.Input("mode-toggle", "value")
    )
    def update_5m_signal(mode):
        # Placeholder logic
        return "Signal: Long", "Confidence: 72%", "Price Target: +$100"

    @app.callback(
        dash.dependencies.Output("signal-10m", "children"),
        dash.dependencies.Output("confidence-10m", "children"),
        dash.dependencies.Output("price-10m", "children"),
        dash.dependencies.Input("mode-toggle", "value")
    )
    def update_10m_signal(mode):
        return "Signal: Hold", "Confidence: 61%", "Price Target: $0"

    @app.callback(
        dash.dependencies.Output("signal-15m", "children"),
        dash.dependencies.Output("confidence-15m", "children"),
        dash.dependencies.Output("price-15m", "children"),
        dash.dependencies.Input("mode-toggle", "value")
    )
    def update_15m_signal(mode):
        return "Signal: Short", "Confidence: 68%", "Price Target: -$100"


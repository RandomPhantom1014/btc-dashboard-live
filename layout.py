from dash import html, dcc
import dash_bootstrap_components as dbc
from header import render_header

timeframes = ["5m", "10m", "15m", "1h", "6h"]

def create_signal_row(tf):
    return html.Div([
        html.Div(tf.upper(), className="label"),
        html.Div(id=f"{tf}-signal", className="signal-pill"),
        html.Div(id=f"{tf}-confidence", className="confidence"),
        html.Div(id=f"{tf}-timestamp", className="timestamp"),
        html.Div(id=f"{tf}-countdown", className="countdown")
    ], className="signal-row")

def serve_layout():
    return html.Div([
        render_header(),
        html.Div([
            html.H1("XRP Signal Dashboard", className="title"),
            html.H2(id="xrp-price-text", className="live-price"),
        ], className="price-container"),

        html.Div([
            html.Div([
                html.H4("Short-Term Signals"),
                create_signal_row("5m"),
                create_signal_row("10m"),
                create_signal_row("15m"),
            ], className="signal-section short-signals"),

            html.Div([
                html.H4("Long-Term Signals"),
                create_signal_row("1h"),
                create_signal_row("6h"),
            ], className="signal-section long-signals")
        ], className="signals-container"),

        dcc.Interval(
            id="interval-component",
            interval=5*1000,  # 5 seconds
            n_intervals=0
        )
    ])

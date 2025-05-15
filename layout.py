from dash import html, dcc
from header import render_header

def serve_layout():
    return html.Div([
        render_header(),
        html.Div(id="xrp-price-text", className="live-price"),
        html.Div(id="5m-signal", className="signal-pill"),
        html.Div(id="10m-signal", className="signal-pill"),
        html.Div(id="15m-signal", className="signal-pill"),
        html.Div(id="1h-signal", className="signal-pill"),
        html.Div(id="6h-signal", className="signal-pill"),
        dcc.Interval(id="interval-component", interval=5*1000, n_intervals=0)
    ])

from dash import html, dcc
from header import render_header

def signal_display_block(interval_id):
    return html.Div(className="signal-row", children=[
        html.Div(id=f"{interval_id}-timestamp", className="signal-timestamp"),
        html.Div(id=f"{interval_id}-signal", className="signal-pill"),
        html.Div(id=f"{interval_id}-confidence", className="signal-confidence"),
        html.Div(id=f"{interval_id}-countdown", className="signal-countdown"),
    ])

def serve_layout():
    return html.Div(
        className="main-container",
        children=[
            render_header(),
            html.Div(id="xrp-price-text", className="live-price"),
            html.Div(className="signals-container", children=[
                html.Div(className="short-term-signals", children=[
                    html.H3("Short-Term XRP Signals"),
                    signal_display_block("5m"),
                    signal_display_block("10m"),
                    signal_display_block("15m"),
                ]),
                html.Div(className="long-term-signals", children=[
                    html.H3("Long-Term XRP Futures Signals"),
                    signal_display_block("1h"),
                    signal_display_block("6h"),
                ])
            ]),
            dcc.Interval(id="update-interval", interval=5000, n_intervals=0)
        ]
    )

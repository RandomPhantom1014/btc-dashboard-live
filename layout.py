from dash import html, dcc
from components.header import render_header

def serve_layout():
    return html.Div([
        render_header(),

        html.H2(id='btc-price-text', children="Loading price...", style={
            'textAlign': 'center',
            'marginTop': '10px',
            'fontSize': '28px',
            'color': '#111'
        }),

        html.Div(id='signals-container'),

        dcc.Interval(id='interval-slow', interval=30000, n_intervals=0),  # Signal updates
        dcc.Interval(id='interval-btc', interval=5000, n_intervals=0),    # Live BTC price updates
    ])

from dash import html, dcc
from components.header import render_header

timeframes = ['5m', '10m', '15m', '1h', '6h']

def signal_block(tf):
    return html.Div([
        html.Div(f"{tf.upper()} Signal", className="signal-title"),
        html.Div(id=f"{tf}-signal", className="pill pill-wait"),
        html.Div(id=f"{tf}-confidence", className="confidence-text"),
        html.Div(id=f"{tf}-timestamp", className="timestamp-text"),
        html.Div(id=f"{tf}-countdown", className="countdown-text"),
    ], className="signal-row")

def serve_layout():
    return html.Div([
        render_header(),
        html.Div(id="xrp-price-text", className="live-price"),
        html.Div([
            html.Div([signal_block(tf) for tf in timeframes[:3]], className="left-signals"),
            html.Div([signal_block(tf) for tf in timeframes[3:]], className="right-signals")
        ], className="signal-board"),
        dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0),
        dcc.RadioItems(
            id='mode-toggle',
            options=[
                {'label': 'Live', 'value': 'live'},
                {'label': 'Backtest', 'value': 'backtest'}
            ],
            value='live',
            className='mode-toggle'
        )
    ], className="main-container")

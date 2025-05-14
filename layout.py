from dash import html, dcc
from header import render_header

def serve_layout():
    def make_signal_block(tf):
        return html.Div([
            html.Strong(f"{tf.upper()} Signal"),
            html.Div(id=f"{tf}-signal", className='pill neutral'),
            html.Div(id=f"{tf}-confidence"),
            html.Div(id=f"{tf}-timestamp"),
            html.Div(id=f"{tf}-countdown")
        ], id=f"{tf}-signal-block", className='signal-block', style={'marginBottom': '20px'})

    return html.Div([
        render_header(),

        html.H2(id='btc-price-text', children="Loading BTC Price...", style={
            'textAlign': 'center',
            'fontSize': '30px',
            'marginTop': '10px',
            'marginBottom': '30px'
        }),

        html.Div([
            html.Div([
                html.H4("Short-Term Signals", style={'textAlign': 'center'}),
                make_signal_block("5m"),
                make_signal_block("10m"),
                make_signal_block("15m")
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

            html.Div([
                html.H4("Futures Signals", style={'textAlign': 'center'}),
                make_signal_block("1h"),
                make_signal_block("6h")
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'flexWrap': 'wrap'}),

        dcc.Interval(id='interval-slow', interval=30000, n_intervals=0),  # Signal refresh every 30s
        dcc.Interval(id='interval-btc', interval=5000, n_intervals=0)     # BTC price refresh every 5s
    ])


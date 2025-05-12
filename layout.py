from dash import html, dcc
from header import render_header

def serve_layout():
    return html.Div([
        render_header(),

        html.H2(id='btc-price-text', children="Loading price...", style={
            'textAlign': 'center',
            'marginTop': '10px',
            'fontSize': '28px',
            'color': '#111'
        }),

        html.Div([
            html.Div([
                html.H4("Short-Term Signals", style={'textAlign': 'center'}),
                html.Div([
                    html.Div([
                        html.Strong("5M Signal"),
                        html.Div(id='5m-signal', className='pill neutral'),
                        html.Div(id='5m-confidence'),
                        html.Div(id='5m-timestamp'),
                        html.Div(id='5m-countdown')
                    ], id='5m-signal-block', className='signal-block'),

                    html.Div([
                        html.Strong("10M Signal"),
                        html.Div(id='10m-signal', className='pill neutral'),
                        html.Div(id='10m-confidence'),
                        html.Div(id='10m-timestamp'),
                        html.Div(id='10m-countdown')
                    ], id='10m-signal-block', className='signal-block'),

                    html.Div([
                        html.Strong("15M Signal"),
                        html.Div(id='15m-signal', className='pill neutral'),
                        html.Div(id='15m-confidence'),
                        html.Div(id='15m-timestamp'),
                        html.Div(id='15m-countdown')
                    ], id='15m-signal-block', className='signal-block'),
                ])
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

            html.Div([
                html.H4("Futures Signals", style={'textAlign': 'center'}),
                html.Div([
                    html.Div([
                        html.Strong("1H Signal"),
                        html.Div(id='1h-signal', className='pill neutral'),
                        html.Div(id='1h-confidence'),
                        html.Div(id='1h-timestamp'),
                        html.Div(id='1h-countdown')
                    ], id='1h-signal-block', className='signal-block'),

                    html.Div([
                        html.Strong("6H Signal"),
                        html.Div(id='6h-signal', className='pill neutral'),
                        html.Div(id='6h-confidence'),
                        html.Div(id='6h-timestamp'),
                        html.Div(id='6h-countdown')
                    ], id='6h-signal-block', className='signal-block'),
                ])
            ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%', 'verticalAlign': 'top'})
        ]),

        dcc.Interval(id='interval-slow', interval=30000, n_intervals=0),  # Signal refresh
        dcc.Interval(id='interval-btc', interval=5000, n_intervals=0),    # BTC price refresh
    ])

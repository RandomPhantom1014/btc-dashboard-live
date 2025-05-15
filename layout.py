from dash import html

def serve_layout():
    return html.Div([
        html.H2("XRP Signal Dashboard", style={'textAlign': 'center'}),
        html.H4(id='xrp-price-text', style={'textAlign': 'center', 'marginBottom': '20px'}),

        html.Div([
            html.Div([
                html.H5("Short-Term Signals", style={'textAlign': 'center'}),
                html.Div(id='signal-5m', className='signal-box'),
                html.Div(id='signal-10m', className='signal-box'),
                html.Div(id='signal-15m', className='signal-box'),
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

            html.Div([
                html.H5("Futures Signals", style={'textAlign': 'center'}),
                html.Div(id='signal-1h', className='signal-box'),
                html.Div(id='signal-6h', className='signal-box'),
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'float': 'right'}),
        ])
    ])


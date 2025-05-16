import dash_bootstrap_components as dbc
from dash import html

def serve_layout():
    return html.Div([
        html.H2("XRP Signal Dashboard", style={'textAlign': 'center'}),
        html.H4(id='live-price', style={'textAlign': 'center'}),

        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H5("Short-Term Signals", className="signal-section-title"),
                    html.Div(id='signal-5m', className='signal-card'),
                    html.Div(id='signal-10m', className='signal-card'),
                    html.Div(id='signal-15m', className='signal-card'),
                ], width=6),

                dbc.Col([
                    html.H5("Long-Term Signals", className="signal-section-title"),
                    html.Div(id='signal-1h', className='signal-card'),
                    html.Div(id='signal-6h', className='signal-card'),
                ], width=6),
            ], className='mt-4'),
        ])
    ])


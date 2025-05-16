from dash import html
import dash_bootstrap_components as dbc

def serve_layout():
    return html.Div([
        html.H2("XRP Signal Dashboard", style={'textAlign': 'center'}),
        html.H4(id='live-price', style={'textAlign': 'center'}),

        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H5("Short-Term Signals"),
                    html.Div(id='signal-5m'),
                    html.Div(id='signal-10m'),
                    html.Div(id='signal-15m'),
                ], width=6),

                dbc.Col([
                    html.H5("Long-Term Signals"),
                    html.Div(id='signal-1h'),
                    html.Div(id='signal-6h'),
                ], width=6),
            ])
        ])
    ])

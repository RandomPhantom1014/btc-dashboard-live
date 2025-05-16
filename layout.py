from dash import html
import dash_bootstrap_components as dbc

def serve_layout():
    return html.Div([
        html.H2("XRP Signal Dashboard", className="dashboard-title"),
        html.H4(id='live-price', className="live-price"),

        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H5("Short-Term Signals", className="section-title"),
                    html.Div(id='signal-5m', className='signal-block'),
                    html.Div(id='signal-10m', className='signal-block'),
                    html.Div(id='signal-15m', className='signal-block'),
                ], width=6),

                dbc.Col([
                    html.H5("Long-Term Signals", className="section-title"),
                    html.Div(id='signal-1h', className='signal-block'),
                    html.Div(id='signal-6h', className='signal-block'),
                ], width=6),
            ])
        ], fluid=True, className="main-container", style={"maxWidth": "90%", "margin": "auto"})
    ])

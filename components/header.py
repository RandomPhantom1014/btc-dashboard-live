from dash import html

def render_header():
    return html.Div(
        id='header',
        style={'textAlign': 'center', 'marginBottom': '20px'},
        children=[
            html.H1('BTC Signal Dashboard', style={'marginBottom': '5px'}),
            html.Div(id='btc-price-text', style={
                'fontSize': '24px',
                'fontWeight': 'bold',
                'color': '#2a9d8f'
            }),
        ]
    )

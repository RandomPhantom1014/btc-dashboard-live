from dash import html

def render_header():
    return html.Div(
        style={'textAlign': 'center', 'padding': '10px'},
        children=[
            html.H1("XRP Signal Dashboard", style={'color': 'white'}),
            html.H3(id='xrp-price-text', style={'color': 'lightgreen'})
        ]
    )

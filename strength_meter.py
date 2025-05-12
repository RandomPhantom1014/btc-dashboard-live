from dash import html

def render_signal_block(timeframe):
    return html.Div(
        id=f'{timeframe}-signal-block',
        style={'marginBottom': '20px', 'padding': '10px', 'border': '1px solid #ccc', 'borderRadius': '8px'},
        children=[
            html.H4(f'{timeframe.upper()} Signal'),
            html.Div(id=f'{timeframe}-signal-text', style={'fontSize': '20px', 'marginBottom': '5px'}),
            html.Div(id=f'{timeframe}-confidence', style={'fontSize': '16px'}),
            html.Div(id=f'{timeframe}-strength-meter', style={'marginTop': '10px'}),
            html.Div([
                html.Span(id=f'{timeframe}-timestamp', style={'fontSize': '12px', 'marginRight': '10px'}),
                html.Span(id=f'{timeframe}-countdown', style={'fontSize': '12px'})
            ])
        ]
    )

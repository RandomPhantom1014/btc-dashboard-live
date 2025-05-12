from dash import html, dcc
from header import render_header
from strength_meter import render_signal_block

def serve_layout():
    return html.Div(
        id='main-container',
        children=[
            render_header(),

            html.Div(
                id='signals-container',
                style={'display': 'flex', 'flexWrap': 'wrap'},
                children=[

                    # Short-Term Signals
                    html.Div(
                        id='short-term-signals',
                        style={'flex': '1', 'minWidth': '300px', 'padding': '10px'},
                        children=[
                            html.H3('Short-Term Signals', style={'textAlign': 'center'}),
                            render_signal_block('5m'),
                            render_signal_block('10m'),
                            render_signal_block('15m')
                        ]
                    ),

                    # Long-Term Signals
                    html.Div(
                        id='long-term-signals',
                        style={'flex': '1', 'minWidth': '300px', 'padding': '10px'},
                        children=[
                            html.H3('Futures Signals', style={'textAlign': 'center'}),
                            render_signal_block('1h'),
                            render_signal_block('6h')
                        ]
                    )
                ]
            ),

            dcc.Interval(id='interval-component', interval=30000, n_intervals=0)
        ],
        style={'fontFamily': 'Arial', 'backgroundColor': '#f9f9f9', 'padding': '10px'}
    )

from dash import html, dcc
from header import render_header

def serve_layout():
    def make_signal_block(tf_label):
        return html.Div([
            html.Strong(f"{tf_label.upper()} Signal"),
            html.Div(id=f"{tf_label}-signal", className='pill neutral'),
            html.Div(id=f"{tf_label}-confidence"),
            html.Div(id=f"{tf_label}-timestamp"),
            html.Div(id=f"{tf_label}-countdown")
        ], id=f"{tf_label}-signal-block", className='signal-block')

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
                make_signal_block("5m"),
                make_signal_block("10m"),
                make_signal_block("15m")
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

            html.Div([
                html.H4("Futures Signals", style={'textAlign': 'center'}),
                make_signal_block("1h"),
                make_signal_block("6h")
            ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%', 'verticalAlign': 'top'})
        ]),

        dcc.Interval(id='interval-slow', interval=30000, n_intervals=0),
        dcc.Interval(id='interval-btc', interval=5000, n_intervals=0)
    ])


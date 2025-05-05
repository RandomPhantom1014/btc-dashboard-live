
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random
import datetime
import pandas as pd

# Simulated Signal Generator (replace with real logic later)
def generate_signal():
    directions = ['Long', 'Short', 'Hold']
    signal = random.choices(
        directions,
        weights=[0.4, 0.4, 0.2],
        k=1
    )[0]
    confidence = round(random.uniform(0.45, 0.85), 2)
    strength = "Weak"
    if confidence >= 0.70:
        strength = "Strong"
    elif confidence >= 0.60:
        strength = "Moderate"
    return signal, confidence, strength

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Layout
app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
    html.H1('BTC Signal Dashboard', style={'textAlign': 'center'}),
    html.Div([
        html.Label('Mode:'),
        dcc.RadioItems(
            id='mode-selector',
            options=[
                {'label': 'Live', 'value': 'live'},
                {'label': 'Backtest', 'value': 'backtest'}
            ],
            value='live',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        )
    ], style={'marginBottom': '20px'}),
    html.Div(id='signal-output', style={'fontSize': '24px', 'margin': '20px 0'}),
    html.Div(id='confidence-output', style={'fontSize': '20px', 'margin': '10px 0'}),
    html.Div(id='strength-output', style={'fontSize': '20px', 'margin': '10px 0'}),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # 5 seconds
        n_intervals=0
    ),
])

# Callbacks
@app.callback(
    [Output('signal-output', 'children'),
     Output('confidence-output', 'children'),
     Output('strength-output', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('mode-selector', 'value')]
)
def update_dashboard(n, mode):
    signal, confidence, strength = generate_signal()
    color = 'gray'
    if signal == 'Long':
        color = 'green'
    elif signal == 'Short':
        color = 'red'

    return (
        html.Span(f'Signal: {signal}', style={'color': color}),
        f'Confidence: {confidence * 100}%',
        f'Strength: {strength}'
    )

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import random
import datetime

app = dash.Dash(__name__)
server = app.server

# Simulated signal generator
def generate_signal():
    signal = random.choice(["Go Long", "Go Short", "Hold"])
    confidence = round(random.uniform(50, 99), 2)
    strength = "High" if confidence > 85 else "Medium" if confidence > 65 else "Low"
    return signal, confidence, strength

# Simulated BTC price chart
def generate_price_data():
    now = datetime.datetime.now()
    times = [now - datetime.timedelta(minutes=i) for i in range(60)][::-1]
    prices = np.cumsum(np.random.randn(60)) + 30000
    return pd.DataFrame({'Time': times, 'Price': prices})

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("🚀 BTC Signal Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Div("Live BTC Price", style={'fontWeight': 'bold'}),
        dcc.Graph(id='price-chart', config={'displayModeBar': False}),
    ], style={'marginBottom': '30px'}),

    html.Div([
        html.Div("Signal Output", style={'fontWeight': 'bold'}),
        html.Div(id='live-signal', style={'fontSize': '24px', 'marginTop': '10px'})
    ], style={'marginBottom': '30px'}),

    html.Div([
        html.Label("Confidence %"),
        html.Div(id='confidence-level', style={'fontSize': '20px'}),
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.Label("Signal Strength"),
        html.Div(id='strength-meter', style={'fontSize': '20px'})
    ], style={'marginBottom': '30px'}),

    html.Div([
        html.Label("Mode"),
        dcc.RadioItems(
            id='mode-toggle',
            options=[{'label': i, 'value': i} for i in ['Live', 'Backtest']],
            value='Live',
            labelStyle={'display': 'inline-block', 'marginRight': '20px'}
        )
    ], style={'marginBottom': '30px'}),

    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # every 5 seconds
        n_intervals=0
    )
])

@app.callback(
    Output('price-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_price_chart(n):
    df = generate_price_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Time'], y=df['Price'], mode='lines', name='BTC/USDT'))
    fig.update_layout(
        margin={'l': 40, 'r': 40, 't': 20, 'b': 30},
        height=300,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return fig

@app.callback(
    [Output('live-signal', 'children'),
     Output('confidence-level', 'children'),
     Output('strength-meter', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('mode-toggle', 'value')]
)
def update_signals(n, mode):
    signal, confidence, strength = generate_signal()
    return (
        f"📣 Signal: {signal}",
        f"{confidence}%",
        f"{strength} Strength"
    )

if __name__ == '__main__':
    app.run_server(debug=True)

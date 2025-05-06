import dash
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Simulated Data (Replace with real-time feed in production)
time_intervals = ['5m', '10m', '15m']
signals = ['Long', 'Short', 'Hold']
btc_price = round(random.uniform(67000, 69000), 2)
confidence_levels = [round(random.uniform(60, 95), 2) for _ in time_intervals]
strengths = ['Weak', 'Moderate', 'Strong']

# Simulate price history
price_data = pd.DataFrame({
    'Time': pd.date_range(end=pd.Timestamp.now(), periods=50, freq='T'),
    'Price': [btc_price + random.uniform(-50, 50) for _ in range(50)]
})

fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=price_data['Time'],
    open=price_data['Price'] - 10,
    high=price_data['Price'] + 10,
    low=price_data['Price'] - 15,
    close=price_data['Price'],
    name='BTC Price'
))
fig.update_layout(
    title='Live BTC Price (Simulated)',
    xaxis_title='Time',
    yaxis_title='Price (USD)',
    height=400,
    margin=dict(l=40, r=40, t=40, b=40),
)

# Layout
app.layout = html.Div([
    html.Div([
        html.H1("BTC Signal Dashboard", style={"textAlign": "center"}),
        dcc.Graph(id='btc-price-chart', figure=fig),
    ], style={"marginBottom": "40px"}),

    html.Div([
        html.Div([
            html.H3(f"{interval} Signal"),
            html.Div([
                html.Span(f"Signal: {random.choice(signals)}", className="pill"),
                html.Span(f"Confidence: {confidence_levels[i]}%", className="pill"),
                html.Span(f"Strength: {random.choice(strengths)}", className="pill")
            ], style={"display": "flex", "gap": "10px"})
        ], style={"marginBottom": "20px"})
        for i, interval in enumerate(time_intervals)
    ]),

    html.Div([
        html.Label("Mode:"),
        dcc.RadioItems(
            options=[
                {'label': 'Live', 'value': 'live'},
                {'label': 'Backtest', 'value': 'backtest'}
            ],
            value='live',
            labelStyle={'display': 'inline-block', 'marginRight': '20px'}
        )
    ], style={"marginTop": "30px"})
])

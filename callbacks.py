import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, State, callback, dcc, html
from app import app
from signals import generate_signals

df_backtest = pd.read_csv('data/backtest_btc.csv')
df_backtest['timestamp'] = pd.to_datetime(df_backtest['timestamp'])

@callback(
    Output("candlestick-chart", "figure"),
    Output("five-min-signal", "children"),
    Output("ten-min-signal", "children"),
    Output("fifteen-min-signal", "children"),
    Input("signal-mode", "value"),
)
def update_dashboard(signal_mode):
    if signal_mode == "backtest":
        df = df_backtest.copy()
        fig = go.Figure(data=[go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='BTC'
        )])
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=300)

        # Generate backtest signals
        signals = generate_signals(df)
        signal_5 = signals.get('5m', {})
        signal_10 = signals.get('10m', {})
        signal_15 = signals.get('15m', {})

        return (
            fig,
            html.Div([
                html.Div(signal_5.get('signal', 'No Data'), className='pill'),
                html.Div(f"Confidence: {signal_5.get('confidence', 0)}%", className='pill-subtext'),
                html.Div(f"Strength: {signal_5.get('strength', 0)}/10", className='pill-subtext'),
            ]),
            html.Div([
                html.Div(signal_10.get('signal', 'No Data'), className='pill'),
                html.Div(f"Confidence: {signal_10.get('confidence', 0)}%", className='pill-subtext'),
                html.Div(f"Strength: {signal_10.get('strength', 0)}/10", className='pill-subtext'),
            ]),
            html.Div([
                html.Div(signal_15.get('signal', 'No Data'), className='pill'),
                html.Div(f"Confidence: {signal_15.get('confidence', 0)}%", className='pill-subtext'),
                html.Div(f"Strength: {signal_15.get('strength', 0)}/10", className='pill-subtext'),
            ]),
        )
    else:
        return go.Figure(), "", "", ""



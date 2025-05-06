# components/layout.py

import dash
from dash import html, dcc
import plotly.graph_objs as go

# Default to light mode; dark mode handled by toggle in UI
def layout():
    return html.Div([
        html.H1("BTC Signal Dashboard", className="header-title"),

        dcc.Graph(id='btc-price-chart'),

        html.Div([
            html.Div([
                html.H4("RSI"),
                dcc.Graph(id='rsi-chart')
            ], className="indicator-section"),

            html.Div([
                html.H4("MACD"),
                dcc.Graph(id='macd-chart')
            ], className="indicator-section"),

            html.Div([
                html.H4("Volume"),
                dcc.Graph(id='volume-chart')
            ], className="indicator-section")
        ], className="indicators-container"),

        html.Div([
            html.Div([
                html.H4("5 Minute Signal"),
                html.Div(id='signal-5m'),
                html.Div(id='confidence-5m')
            ], className="signal-box"),

            html.Div([
                html.H4("10 Minute Signal"),
                html.Div(id='signal-10m'),
                html.Div(id='confidence-10m')
            ], className="signal-box"),

            html.Div([
                html.H4("15 Minute Signal"),
                html.Div(id='signal-15m'),
                html.Div(id='confidence-15m')
            ], className="signal-box"),
        ], className="signals-container"),

        html.Div([
            html.H4("Signal Strength Meter"),
            html.Div(id='strength-meter')
        ], className="strength-section"),

        html.Div([
            html.Label("Mode"),
            dcc.RadioItems(
                id='mode-toggle',
                options=[
                    {'label': 'Live', 'value': 'live'},
                    {'label': 'Backtest', 'value': 'backtest'}
                ],
                value='live',
                labelStyle={'display': 'inline-block', 'margin-right': '20px'}
            )
        ], className="mode-toggle"),

        html.Div([
            html.Label("Theme"),
            dcc.RadioItems(
                id='theme-toggle',
                options=[
                    {'label': 'Light', 'value': 'light'},
                    {'label': 'Dark', 'value': 'dark'}
                ],
                value='light',
                labelStyle={'display': 'inline-block', 'margin-right': '20px'}
            )
        ], className="theme-toggle"),

        dcc.Interval(
            id='interval-component',
            interval=60 * 1000,  # Refresh every 60 seconds
            n_intervals=0
        )
    ], id='main-container')

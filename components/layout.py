# components/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
from components.styles import card_style
from components.header import render_header
from components.chart import render_candlestick_chart
from components.indicators import render_indicators
from components.signal_logic import render_signal_card


def create_layout(app):
    return dbc.Container([
        render_header(),

        dbc.Row([
            dbc.Col(render_candlestick_chart(), width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(render_indicators(), width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(render_signal_card("5m"), width=4),
            dbc.Col(render_signal_card("10m"), width=4),
            dbc.Col(render_signal_card("15m"), width=4),
        ], className="mb-4"),

        dcc.Interval(id="interval-component", interval=5000, n_intervals=0)
    ], fluid=True)

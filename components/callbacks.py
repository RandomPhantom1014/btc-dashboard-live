# components/callbacks.py

from dash import Input, Output, State, callback, ctx
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import datetime
import random

# Dummy signal generation for demonstration (replace with actual logic later)
def generate_mock_signal():
    return random.choice(["Go Long", "Go Short", "Wait"]), round(random.uniform(60, 99), 2)

@callback(
    Output("btc-price", "children"),
    Input("interval-component", "n_intervals"),
)
def update_btc_price(_):
    # Placeholder for live BTC price fetch — replace with WebSocket or API data
    mock_price = f"${random.randint(64000, 68000):,}"
    return f"BTC Price: {mock_price}"

@callback(
    Output("signal-output-5m", "children"),
    Output("signal-confidence-5m", "children"),
    Output("signal-strength-5m", "color"),
    Input("interval-component", "n_intervals"),
    State("mode-toggle", "value"),
)
def update_5m_signals(_, mode):
    signal, confidence = generate_mock_signal()
    color = "green" if signal == "Go Long" else "red" if signal == "Go Short" else "gray"
    return signal, f"{confidence}%", color

@callback(
    Output("signal-output-10m", "children"),
    Output("signal-confidence-10m", "children"),
    Output("signal-strength-10m", "color"),
    Input("interval-component", "n_intervals"),
    State("mode-toggle", "value"),
)
def update_10m_signals(_, mode):
    signal, confidence = generate_mock_signal()
    color = "green" if signal == "Go Long" else "red" if signal == "Go Short" else "gray"
    return signal, f"{confidence}%", color

@callback(
    Output("signal-output-15m", "children"),
    Output("signal-confidence-15m", "children"),
    Output("signal-strength-15m", "color"),
    Input("interval-component", "n_intervals"),
    State("mode-toggle", "value"),
)
def update_15m_signals(_, mode):
    signal, confidence = generate_mock_signal()
    color = "green" if signal == "Go Long" else "red" if signal == "Go Short" else "gray"
    return signal, f"{confidence}%", color

@callback(
    Output("backtest-section", "style"),
    Input("mode-toggle", "value")
)
def toggle_backtest_section(mode):
    if mode == "Backtest":
        return {"display": "block"}
    return {"display": "none"}

@callback(
    Output("theme-styles", "data"),
    Input("theme-toggle", "value"),
)
def update_theme_style(value):
    return {"theme": value or "light"}

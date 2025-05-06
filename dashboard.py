import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import random
from datetime import datetime, timedelta

app = dash.Dash(__name__)
server = app.server

# Simulated signal generator
def generate_signal_data():
    return {
        "5m": {"signal": random.choice(["Long", "Short", "Hold"]), "confidence": random.randint(70, 99)},
        "10m": {"signal": random.choice(["Long", "Short", "Hold"]), "confidence": random.randint(70, 99)},
        "15m": {"signal": random.choice(["Long", "Short", "Hold"]), "confidence": random.randint(70, 99)},
    }

# Simulated strength meter color logic
def get_strength_color(confidence):
    if confidence >= 90:
        return "green"
    elif confidence >= 80:
        return "orange"
    else:
        return "red"

# Simulated price data
def generate_price_data():
    now = datetime.now()
    return pd.DataFrame({
        "time": [now - timedelta(minutes=i) for i in range(50)],
        "price": [50000 + random.randint(-300, 300) for _ in range(50)]
    }).sort_values("time")

signal_data = generate_signal_data()
price_data = generate_price_data()

# UI Layout
app.layout = html.Div([
    html.H1("BTC Signal Dashboard", style={"textAlign": "center"}),

    dcc.Graph(
        id="btc-chart",
        figure={
            "data": [
                go.Candlestick(
                    x=price_data["time"],
                    open=price_data["price"],
                    high=price_data["price"] + 50,
                    low=price_data["price"] - 50,
                    close=price_data["price"],
                    name="BTC"
                )
            ],
            "layout": go.Layout(
                title="Live BTC Price Chart",
                xaxis={"title": "Time"},
                yaxis={"title": "Price (USD)"}
            )
        }
    ),

    html.Div([
        html.Div([
            html.H3("5-Minute Signal"),
            html.Div([
                html.Span(signal_data["5m"]["signal"], className="pill", style={"backgroundColor": get_strength_color(signal_data["5m"]["confidence"]), "padding": "5px 10px", "borderRadius": "10px", "color": "white"}),
                html.Span(f"Confidence: {signal_data['5m']['confidence']}%", style={"marginLeft": "10px"})
            ])
        ], className="signal-box"),

        html.Div([
            html.H3("10-Minute Signal"),
            html.Div([
                html.Span(signal_data["10m"]["signal"], className="pill", style={"backgroundColor": get_strength_color(signal_data["10m"]["confidence"]), "padding": "5px 10px", "borderRadius": "10px", "color": "white"}),
                html.Span(f"Confidence: {signal_data['10m']['confidence']}%", style={"marginLeft": "10px"})
            ])
        ], className="signal-box"),

        html.Div([
            html.H3("15-Minute Signal"),
            html.Div([
                html.Span(signal_data["15m"]["signal"], className="pill", style={"backgroundColor": get_strength_color(signal_data["15m"]["confidence"]), "padding": "5px 10px", "borderRadius": "10px", "color": "white"}),
                html.Span(f"Confidence: {signal_data['15m']['confidence']}%", style={"marginLeft": "10px"})
            ])
        ], className="signal-box")
    ], style={"display": "grid", "gridTemplateColumns": "repeat(3, 1fr)", "gap": "20px", "margin": "20px"}),

    html.Div("Mode: Live / Backtest", style={"textAlign": "center", "marginTop": "40px"})
], style={"padding": "20px", "fontFamily": "Arial"})




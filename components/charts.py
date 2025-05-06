# components/charts.py

from dash import html, dcc
import plotly.graph_objs as go

def btc_price_chart():
    return html.Div([
        html.H4("BTC Price Chart"),
        dcc.Graph(
            id="btc-candlestick-chart",
            figure={
                "data": [
                    go.Candlestick(
                        x=[],
                        open=[],
                        high=[],
                        low=[],
                        close=[],
                        name="BTC/USD"
                    )
                ],
                "layout": go.Layout(
                    xaxis=dict(title="Time"),
                    yaxis=dict(title="Price (USD)"),
                    height=300,
                    template="plotly_dark"
                )
            }
        )
    ])

def rsi_chart():
    return html.Div([
        html.H4("RSI Indicator"),
        dcc.Graph(
            id="rsi-chart",
            figure={
                "data": [go.Scatter(x=[], y=[], name="RSI")],
                "layout": go.Layout(height=150, template="plotly_dark")
            }
        )
    ])

def macd_chart():
    return html.Div([
        html.H4("MACD Indicator"),
        dcc.Graph(
            id="macd-chart",
            figure={
                "data": [go.Scatter(x=[], y=[], name="MACD")],
                "layout": go.Layout(height=150, template="plotly_dark")
            }
        )
    ])

def volume_chart():
    return html.Div([
        html.H4("Volume"),
        dcc.Graph(
            id="volume-chart",
            figure={
                "data": [go.Bar(x=[], y=[], name="Volume")],
                "layout": go.Layout(height=150, template="plotly_dark")
            }
        )
    ])

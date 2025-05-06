# components/chart.py

from dash import dcc, html

def build_price_chart():
    return html.Div(className="chart-container", children=[
        html.H2("BTC Price Chart"),
        dcc.Graph(
            id="btc-candlestick-chart",
            config={"displayModeBar": False},
            style={"height": "400px"}
        )
    ])

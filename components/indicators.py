# components/indicators.py

from dash import html, dcc
import plotly.graph_objs as go

def render_indicators(rsi_data=None, macd_data=None, volume_data=None):
    # Provide default empty lists if data isn't passed
    rsi_data = rsi_data or []
    macd_data = macd_data or []
    volume_data = volume_data or []

    return html.Div([
        html.Div([
            html.H5("RSI Indicator"),
            dcc.Graph(
                config={"displayModeBar": False},
                figure=go.Figure(
                    data=[go.Scatter(y=rsi_data, mode="lines", name="RSI")],
                    layout=go.Layout(
                        height=200,
                        margin=dict(l=30, r=30, t=30, b=30),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        yaxis_title="RSI"
                    )
                )
            )
        ]),
        html.Div([
            html.H5("MACD Indicator"),
            dcc.Graph(
                config={"displayModeBar": False},
                figure=go.Figure(
                    data=[go.Scatter(y=macd_data, mode="lines", name="MACD")],
                    layout=go.Layout(
                        height=200,
                        margin=dict(l=30, r=30, t=30, b=30),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        yaxis_title="MACD"
                    )
                )
            )
        ]),
        html.Div([
            html.H5("Volume"),
            dcc.Graph(
                config={"displayModeBar": False},
                figure=go.Figure(
                    data=[go.Bar(y=volume_data, name="Volume")],
                    layout=go.Layout(
                        height=200,
                        margin=dict(l=30, r=30, t=30, b=30),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        yaxis_title="Volume"
                    )
                )
            )
        ])
    ], style={"padding": "10px"})

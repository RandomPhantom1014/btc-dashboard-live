# components/layout.py

from dash import html, dcc
import plotly.graph_objs as go

def create_layout():
    return html.Div(
        id="main-container",
        children=[
            html.H1("BTC Signal Dashboard", style={"textAlign": "center"}),

            html.Div([
                html.Div([
                    html.Label("Theme:"),
                    dcc.RadioItems(
                        id="theme-toggle",
                        options=[
                            {"label": "Light", "value": "light"},
                            {"label": "Dark", "value": "dark"}
                        ],
                        value="light",
                        labelStyle={"display": "inline-block", "margin-right": "10px"}
                    ),
                ], style={"margin-bottom": "10px"}),

                html.Div([
                    html.Label("Signal Mode:"),
                    dcc.RadioItems(
                        id="mode-toggle",
                        options=[
                            {"label": "Live", "value": "live"},
                            {"label": "Backtest", "value": "backtest"}
                        ],
                        value="live",
                        labelStyle={"display": "inline-block", "margin-right": "10px"}
                    ),
                ], style={"margin-bottom": "10px"}),

                html.Div(id="price-display", style={"margin-bottom": "10px", "font-weight": "bold"}),

                dcc.Graph(id="candlestick-chart", style={"height": "400px"}),
            ], style={"padding": "0 20px"}),

            html.Div([
                html.Div(id="signal-5m", className="signal-box"),
                html.Div(id="signal-10m", className="signal-box"),
                html.Div(id="signal-15m", className="signal-box"),
            ], id="signals-container", style={"padding": "0 20px"}),

            html.Button("Export CSV", id="export-button", style={"margin": "20px"}),
            dcc.Download(id="download-dataframe-csv"),

            html.Div([
                dcc.Checklist(
                    options=[{"label": "Save Logs", "value": "save"}],
                    id="save-logs-toggle",
                    value=[],
                    style={"margin": "20px 0"}
                )
            ]),

            dcc.Interval(id="update-interval", interval=60 * 1000, n_intervals=0),  # update every 60s
        ]
    )
# components/layout.py

from dash import html, dcc
import plotly.graph_objs as go

def create_layout():
    return html.Div(
        id="main-container",
        children=[
            html.H1("BTC Signal Dashboard", style={"textAlign": "center"}),

            html.Div([
                html.Div([
                    html.Label("Theme:"),
                    dcc.RadioItems(
                        id="theme-toggle",
                        options=[
                            {"label": "Light", "value": "light"},
                            {"label": "Dark", "value": "dark"}
                        ],
                        value="light",
                        labelStyle={"display": "inline-block", "margin-right": "10px"}
                    ),
                ], style={"margin-bottom": "10px"}),

                html.Div([
                    html.Label("Signal Mode:"),
                    dcc.RadioItems(
                        id="mode-toggle",
                        options=[
                            {"label": "Live", "value": "live"},
                            {"label": "Backtest", "value": "backtest"}
                        ],
                        value="live",
                        labelStyle={"display": "inline-block", "margin-right": "10px"}
                    ),
                ], style={"margin-bottom": "10px"}),

                html.Div(id="price-display", style={"margin-bottom": "10px", "font-weight": "bold"}),

                dcc.Graph(id="candlestick-chart", style={"height": "400px"}),
            ], style={"padding": "0 20px"}),

            html.Div([
                html.Div(id="signal-5m", className="signal-box"),
                html.Div(id="signal-10m", className="signal-box"),
                html.Div(id="signal-15m", className="signal-box"),
            ], id="signals-container", style={"padding": "0 20px"}),

            html.Button("Export CSV", id="export-button", style={"margin": "20px"}),
            dcc.Download(id="download-dataframe-csv"),

            html.Div([
                dcc.Checklist(
                    options=[{"label": "Save Logs", "value": "save"}],
                    id="save-logs-toggle",
                    value=[],
                    style={"margin": "20px 0"}
                )
            ]),

            dcc.Interval(id="update-interval", interval=60 * 1000, n_intervals=0),  # update every 60s
        ]
    )


import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random
import datetime

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Simulated live price data
def get_live_btc_price():
    return round(93000 + random.uniform(-250, 250), 2)

# Simulated RSI, MACD, Volume data
def get_indicator_data():
    return {
        "rsi": round(random.uniform(30, 70), 2),
        "macd": round(random.uniform(-5, 5), 2),
        "volume": random.randint(5000, 20000)
    }

# Simulated signals
def get_signals():
    return {
        "5m": ("Long", random.randint(60, 99)),
        "10m": ("Hold", random.randint(50, 95)),
        "15m": ("Short", random.randint(55, 90))
    }

# Simulated signal strength color
def get_strength_color(conf):
    if conf >= 85:
        return "green"
    elif conf >= 70:
        return "orange"
    else:
        return "red"

# Light/Dark toggle setup
light_theme = {
    "background": "#ffffff",
    "text": "#000000"
}
dark_theme = {
    "background": "#000000",
    "text": "#00FFFF"
}

app.layout = html.Div(id="root", children=[
    dcc.Interval(id="interval-update", interval=5 * 1000, n_intervals=0),
    dcc.Store(id="theme", data="light"),

    html.Div([
        html.H1("BTC Signal Dashboard", id="title", style={"textAlign": "center"}),
        html.Button("Toggle Theme", id="theme-toggle", n_clicks=0)
    ]),

    html.Div([
        dcc.Graph(id="btc-price-chart")
    ], style={"marginBottom": "30px"}),

    html.Div(id="indicators"),

    html.Div(id="signals")
], style={"padding": "20px"})


@app.callback(
    Output("theme", "data"),
    Input("theme-toggle", "n_clicks"),
    prevent_initial_call=True
)
def toggle_theme(n):
    return "dark" if n % 2 else "light"


@app.callback(
    Output("btc-price-chart", "figure"),
    Output("indicators", "children"),
    Output("signals", "children"),
    Output("root", "style"),
    Output("title", "style"),
    Input("interval-update", "n_intervals"),
    Input("theme", "data")
)
def update_dashboard(n, theme_mode):
    price = get_live_btc_price()
    indicators = get_indicator_data()
    signals = get_signals()
    theme = dark_theme if theme_mode == "dark" else light_theme

    # BTC Price Chart
    chart = go.Figure(data=[
        go.Scatter(
            x=[datetime.datetime.now()],
            y=[price],
            mode="lines+markers",
            name="BTC Price"
        )
    ])
    chart.update_layout(
        title="Live BTC Price",
        paper_bgcolor=theme["background"],
        plot_bgcolor=theme["background"],
        font=dict(color=theme["text"]),
        margin={"t": 40, "b": 40, "l": 40, "r": 40}
    )

    # Indicators Display
    indicators_html = html.Div([
        html.Div(f"RSI: {indicators['rsi']}", style={"margin": "5px"}),
        html.Div(f"MACD: {indicators['macd']}", style={"margin": "5px"}),
        html.Div(f"Volume: {indicators['volume']}", style={"margin": "5px"})
    ], style={"marginBottom": "20px", "color": theme["text"]})

    # Signals Panel
    signals_html = html.Div([
        html.Div([
            html.Div(f"{tf.upper()} - {signal[0]}", style={
                "display": "inline-block",
                "width": "150px",
                "color": theme["text"]
            }),
            html.Div(f"Confidence: {signal[1]}%", style={
                "backgroundColor": get_strength_color(signal[1]),
                "color": "white",
                "padding": "5px",
                "borderRadius": "6px",
                "display": "inline-block",
                "marginLeft": "10px"
            })
        ]) for tf, signal in signals.items()
    ], style={"color": theme["text"]})

    return chart, indicators_html, signals_html, {"backgroundColor": theme["background"]}, {"color": theme["text"]}


if __name__ == "__main__":
    app.run_server(debug=True)


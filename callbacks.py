from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals

previous_price = None

def register_callbacks(app):
    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_btc_price(n):
        global previous_price
        price = fetch_live_btc_price()
        if price is None:
            return "Live BTC Price: Error"

        color = "white"
        if previous_price is not None:
            if price > previous_price:
                color = "limegreen"
            elif price < previous_price:
                color = "red"
        previous_price = price

        return html.Div([
            html.Span("Live BTC Price: ", style={"fontWeight": "bold", "marginRight": "8px"}),
            html.Span(f"${float(price):,.2f}", style={"color": color, "fontWeight": "bold"})
        ])

    @app.callback(
        [Output(f"signal-{key}", "children") for key in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]] +
        [Output(f"confidence-{key}", "children") for key in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]] +
        [Output(f"strength-{key}", "children") for key in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]],
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        timeframes = ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]
        signals, confidences, strengths = [], [], []

        current_price = df["close"].iloc[-1]

        for tf in timeframes:
            signal, confidence, strength = generate_signals(df, tf)
            signals.append(signal)
            confidences.append(f"Confidence: {confidence}%")
            strengths.append(strength)

            if save_logs:
                append_log(tf, signal, confidence, strength, current_price)

        return signals + confidences + strengths


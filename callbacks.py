from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from utils.data import get_btc_data, append_log
from utils.signals_logic import generate_signals
from datetime import datetime, timedelta

previous_price = None
signal_timestamps = {}

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

        color = "black"
        if previous_price is not None:
            if price > previous_price:
                color = "limegreen"
            elif price < previous_price:
                color = "red"
        previous_price = price

        return html.Span([
            html.Span("Live BTC Price: ", style={"fontWeight": "bold", "marginRight": "8px"}),
            html.Span(f"${float(price):,.2f}", style={"color": color})
        ])

    @app.callback(
        Output("signal-5m", "children"), Output("confidence-5m", "children"), Output("strength-5m", "children"),
        Output("signal-10m", "children"), Output("confidence-10m", "children"), Output("strength-10m", "children"),
        Output("signal-15m", "children"), Output("confidence-15m", "children"), Output("strength-15m", "children"),
        Output("signal-1h", "children"), Output("confidence-1h", "children"), Output("strength-1h", "children"),
        Output("signal-6h", "children"), Output("confidence-6h", "children"), Output("strength-6h", "children"),
        Output("signal-12h", "children"), Output("confidence-12h", "children"), Output("strength-12h", "children"),
        Output("signal-24h", "children"), Output("confidence-24h", "children"), Output("strength-24h", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value"),
        State("save-logs-toggle", "value")
    )
    def update_signals(n, mode, save_logs):
        df = get_btc_data(mode)
        if df is None or df.empty:
            raise PreventUpdate

        output = []
        for tf in ["5m", "10m", "15m", "1h", "6h", "12h", "24h"]:
            signal, conf, strength = generate_signals(df, tf)
            signal_time = datetime.now().strftime("%I:%M %p HST")
            signal_timestamps[tf] = datetime.now()

            countdown_target = signal_timestamps[tf] + get_timedelta_for(tf)
            remaining = countdown_target - datetime.now()
            minutes, seconds = divmod(max(0, int(remaining.total_seconds())), 60)

            signal_label = html.Div([
                html.Span(signal, style={"display": "block"}),
                html.Span(f"({signal_time})", style={"fontSize": "14px", "color": "#666"}),
                html.Br(),
                html.Span(f"⏳ {minutes}:{str(seconds).zfill(2)}", style={"fontSize": "14px", "color": "#888"})
            ])

            output.extend([
                signal_label,
                f"Confidence: {conf}%",
                strength
            ])

            if save_logs:
                price_now = df["close"].iloc[-1]
                append_log(tf, signal, conf, strength, price_now)

        return tuple(output)

def get_timedelta_for(timeframe):
    return {
        "5m": timedelta(minutes=5),
        "10m": timedelta(minutes=10),
        "15m": timedelta(minutes=15),
        "1h": timedelta(hours=1),
        "6h": timedelta(hours=6),
        "12h": timedelta(hours=12),
        "24h": timedelta(hours=24),
    }.get(timeframe, timedelta(minutes=5))

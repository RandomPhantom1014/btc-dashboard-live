from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from components.live_price import fetch_live_btc_price
from components.chart import render_candlestick_chart
from components.indicators import render_indicators
from utils.data import get_btc_data
import pandas as pd

previous_price = None

def generate_signals(df, interval):
    try:
        resampled = df['close'].resample(interval).last().dropna()
        signals = []
        for i in range(1, len(resampled)):
            if resampled[i] > resampled[i - 1]:
                signals.append(("Go Long", "Confidence: 70%", 5))
            elif resampled[i] < resampled[i - 1]:
                signals.append(("Go Short", "Confidence: 70%", 5))
            else:
                signals.append(("Wait", "Confidence: 50%", 5))
        return signals[-1] if signals else ("Wait", "Confidence: 50%", 5)
    except Exception as e:
        print(f"Signal generation error: {e}")
        return ("Wait", "Confidence: 50%", 5)

def register_callbacks(app):

    @app.callback(
        Output("live-btc-price", "children"),
        Input("interval-component", "n_intervals")
    )
    def update_btc_price(n):
        global previous_price
        current_price = fetch_live_btc_price()
        if current_price is None:
            return "Live BTC Price: N/A"
        
        color = "white"
        if previous_price is not None:
            if current_price > previous_price:
                color = "limegreen"
            elif current_price < previous_price:
                color = "red"
        previous_price = current_price

        return [
            "Live BTC Price: ",
            {
                "type": "span",
                "props": {
                    "style": {"color": color, "fontWeight": "bold"},
                    "children": f"${current_price:,.2f}"
                }
            }
        ]

    @app.callback(
        Output("candlestick-chart", "figure"),
        Output("indicators-container", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_chart_and_indicators(n, mode):
        df = get_btc_data()
        if df is None or df.empty:
            raise PreventUpdate

        fig = render_candlestick_chart(df)
        indicators = render_indicators(df)

        return fig, indicators

    @app.callback(
        Output("signal-5m", "children"),
        Output("confidence-5m", "children"),
        Output("signal-10m", "children"),
        Output("confidence-10m", "children"),
        Output("signal-15m", "children"),
        Output("confidence-15m", "children"),
        Input("interval-component", "n_intervals"),
        State("mode-toggle", "value")
    )
    def update_signals(n, mode):
        df = get_btc_data()
        if df is None or df.empty:
            raise PreventUpdate

        df = df.copy()
        df.index = pd.to_datetime(df.index)

        signal_5m, conf_5m, _ = generate_signals(df, '5T')
        signal_10m, conf_10m, _ = generate_signals(df, '10T')
        signal_15m, conf_15m, _ = generate_signals(df, '15T')

        return signal_5m, conf_5m, signal_10m, conf_10m, signal_15m, conf_15m


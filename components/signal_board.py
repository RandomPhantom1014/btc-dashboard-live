# components/signal_board.py

from dash import html

def signal_row(timeframe, signal, confidence, strength_color):
    return html.Div([
        html.Div(timeframe, className="signal-cell"),
        html.Div(signal, className="signal-cell"),
        html.Div(f"{confidence}%", className="signal-cell"),
        html.Div(className=f"signal-pill {strength_color}")
    ], className="signal-row")

def signal_board():
    return html.Div([
        html.H4("Signal Board"),
        html.Div(id="signal-output"),
        html.Div([
            signal_row("5 min", "Wait", 72, "yellow"),
            signal_row("10 min", "Long", 85, "green"),
            signal_row("15 min", "Short", 64, "red"),
        ])
    ], id="signal-board")

# components/signal_panel.py

from dash import html

def signal_row(timeframe, signal, confidence, strength_color):
    return html.Div(
        className="signal-row",
        children=[
            html.Div(f"{timeframe}", className="signal-cell timeframe"),
            html.Div(f"{signal}", className="signal-cell signal"),
            html.Div(f"{confidence}%", className="signal-cell confidence"),
            html.Div(
                className=f"signal-cell strength",
                children=[
                    html.Div(className="strength-pill", style={"backgroundColor": strength_color})
                ]
            )
        ]
    )

def signal_panel():
    return html.Div(
        className="signal-panel",
        children=[
            html.H4("Signal Output"),
            signal_row("5 min", "Waiting...", "0", "#888"),
            signal_row("10 min", "Waiting...", "0", "#888"),
            signal_row("15 min", "Waiting...", "0", "#888"),
        ]
    )

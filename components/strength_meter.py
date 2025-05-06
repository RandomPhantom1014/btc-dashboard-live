# components/strength_meter.py

from dash import html

def strength_meter(strength_label, color):
    return html.Div(
        className="strength-meter",
        children=[
            html.Span("Signal Strength:", className="meter-label"),
            html.Span(strength_label, className="meter-value", style={"color": color})
        ]
    )

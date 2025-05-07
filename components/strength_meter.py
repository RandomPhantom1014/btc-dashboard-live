# components/strength_meter.py

from dash import html

def render_strength_meter(timeframe_id):
    return html.Div(
        id=f"strength-meter-{timeframe_id}",
        className="strength-meter",
        children=[
            html.Div(id=f"strength-label-{timeframe_id}", className="strength-label"),
            html.Div(id=f"strength-bar-{timeframe_id}", className="strength-bar")
        ]
    )

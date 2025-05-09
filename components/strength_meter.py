# components/strength_meter.py

from dash import html

def render_strength_meter(timeframe):
    return html.Div(
        id=f"strength-meter-{timeframe}",
        className="strength-meter",
        children="Strength: —",
        style={
            "padding": "6px 12px",
            "borderRadius": "8px",
            "color": "white",
            "backgroundColor": "#444",
            "textAlign": "center",
            "fontWeight": "bold"
        }
    )

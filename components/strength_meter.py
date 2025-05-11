from dash import html

def render_strength_meter(timeframe):
    return html.Div(
        id=f"strength-{timeframe}",
        className="strength-meter",
        children="Strength: —"
    )

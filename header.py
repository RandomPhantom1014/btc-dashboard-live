from dash import html

def render_header():
    return html.Div(
        children=[
            html.H1("BTC Signal Dashboard", style={"textAlign": "center"})
        ],
        style={
            "padding": "10px",
            "borderBottom": "1px solid #ccc",
            "marginBottom": "20px"
        }
    )

from dash import html

def render_header():
    return html.Div(
        className="header",
        children=[
            html.H1("XRP Signal Dashboard", className="header-title")
        ]
    )

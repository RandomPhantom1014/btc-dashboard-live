from dash import html

def render_header():
    return html.Div(
        className="dashboard-header",
        children=[
            html.H2("📊 BTC Signal Dashboard", className="header-title")
        ]
    )

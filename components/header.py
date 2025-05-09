from dash import html

def render_header():
    return html.Div(
        className="dashboard-header",
        children=[
            html.H2("📊 BTC Signal Dashboard", style={
                "textAlign": "center",
                "color": "#000",  # black font for light background
                "paddingTop": "10px",
                "paddingBottom": "10px",
                "fontWeight": "bold"
            })
        ]
    )

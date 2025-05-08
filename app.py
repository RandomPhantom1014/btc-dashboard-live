# app.py

from dash import Dash, html, dcc, Output, Input
from components.layout import create_layout

# Initialize Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Main layout with theme routing support
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# Update layout based on theme in URL (light/dark)
@app.callback(
    Output("page-content", "children"),
    Input("url", "href")
)
def display_page(href):
    theme = "light"
    if href and "theme=dark" in href:
        theme = "dark"
    return create_layout(theme)

# Register all Dash callbacks
from callbacks import register_callbacks
register_callbacks(app)

# ✅ Expose WSGI server for Render/Gunicorn compatibility
server = app.server

# Run locally (ignored on Render)
if __name__ == "__main__":
    app.run_server(debug=True)

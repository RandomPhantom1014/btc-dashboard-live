# app.py

from dash import Dash, html, dcc, Output, Input
from components.layout import create_layout

app = Dash(__name__, suppress_callback_exceptions=True)

# Set base layout with theme switching support
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "href")
)
def display_page(href):
    theme = "light"
    if href and "theme=dark" in href:
        theme = "dark"
    return create_layout(theme)

# Register callbacks
from callbacks import register_callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)

import dash
from layout import serve_layout
from callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "XRP Signal Dashboard"
app.layout = serve_layout
server = app.server

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)

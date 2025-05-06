import dash
from dashboard import layout, register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "BTC Signal Dashboard"
app.layout = layout
server = app.server

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)


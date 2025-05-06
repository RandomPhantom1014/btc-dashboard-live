# app.py

from dashboard import app
from components.callbacks import register_callbacks
from components.layout import layout

# Set the layout
app.layout = layout()

# Register all callbacks
register_callbacks(app)

# Server exposure for deployment (e.g., Render)
server = app.server

# Local development entry point
if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8080)

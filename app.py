from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from layout import serve_layout
from callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

app.layout = html.Div([
    serve_layout(),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),

    html.Script("""
        function updateCountdowns() {
            const now = new Date();
            document.querySelectorAll("[id^='countdown-']").forEach(el => {
                const isoTime = el.getAttribute("data-time");
                const duration = parseInt(el.getAttribute("data-duration"));
                if (!isoTime || isNaN(duration)) return;

                const start = new Date(isoTime);
                const end = new Date(start.getTime() + duration * 1000);
                const remaining = Math.floor((end - now) / 1000);

                if (remaining <= 0) {
                    el.textContent = "• 0:00";
                    return;
                }

                const mins = Math.floor(remaining / 60);
                const secs = remaining % 60;
                const padded = `${mins}:${secs.toString().padStart(2, '0')}`;
                el.textContent = `• ${padded}`;
            });
        }

        setInterval(updateCountdowns, 1000);
    """)
])

register_callbacks(app)

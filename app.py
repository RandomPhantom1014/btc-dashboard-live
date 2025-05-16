from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from layout import serve_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

app.layout = html.Div([
    serve_layout(),

    html.Script('''
        function updateCountdowns() {
            const now = new Date();
            document.querySelectorAll("[id^='countdown-']").forEach(el => {
                const parent = el.parentNode;
                const timeText = Array.from(parent.childNodes).find(n => n.textContent.includes('Last updated'));
                if (!timeText) return;

                const match = timeText.textContent.match(/(\\d{2}:\\d{2}:\\d{2} [AP]M)/);
                if (!match) return;

                const hstTimeStr = match[1];
                const hstNow = new Date().toLocaleString("en-US", { timeZone: "Pacific/Honolulu" });
                const updatedTime = new Date(hstNow.split(",")[0] + " " + hstTimeStr);
                const secondsAgo = Math.floor((new Date(hstNow) - updatedTime) / 1000);

                let msg = secondsAgo < 60 ? `${secondsAgo}s ago`
                        : secondsAgo < 3600 ? `${Math.floor(secondsAgo / 60)}m ago`
                        : `${Math.floor(secondsAgo / 3600)}h ago`;

                el.textContent = `• ${msg}`;
            });
        }

        setInterval(updateCountdowns, 1000);
    ''')
])

# components/theme.py

from dash import Input, Output, State, ctx

def register_theme_callbacks(app):
    @app.callback(
        Output("theme-container", "className"),
        Input("theme-toggle", "n_clicks"),
        State("theme-container", "className"),
        prevent_initial_call=True
    )
    def toggle_theme(n, current_class):
        if current_class == "light-mode":
            return "dark-mode"
        return "light-mode"

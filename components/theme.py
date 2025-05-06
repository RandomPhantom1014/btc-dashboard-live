# components/theme.py

LIGHT_THEME = {
    "background": "#ffffff",
    "text": "#000000",
    "card": "#f8f9fa",
    "accent": "#007bff"
}

DARK_THEME = {
    "background": "#121212",
    "text": "#ffffff",
    "card": "#1e1e1e",
    "accent": "#0fffc1"
}

def get_theme(mode):
    return DARK_THEME if mode == "dark" else LIGHT_THEME

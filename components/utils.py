# components/utils.py

def format_price(value):
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return "--"

def get_signal_color(signal_type, theme):
    if signal_type == "Go Long":
        return theme["pill_go_long"]
    elif signal_type == "Go Short":
        return theme["pill_go_short"]
    elif signal_type == "Wait":
        return theme["pill_wait"]
    else:
        return theme["text"]

def get_confidence_color(confidence, theme):
    if confidence >= 80:
        return theme["pill_go_long"]
    elif confidence >= 50:
        return theme["accent"]
    else:
        return theme["pill_wait"]

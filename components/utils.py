# components/utils.py

def format_price(value):
    """Format price with commas and two decimal places."""
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def interpret_strength(confidence):
    """Interpret signal strength based on confidence %."""
    if confidence >= 80:
        return "Strong"
    elif confidence >= 60:
        return "Moderate"
    else:
        return "Weak"

def color_for_strength(strength):
    """Return color class based on signal strength label."""
    return {
        "Strong": "green",
        "Moderate": "orange",
        "Weak": "red"
    }.get(strength, "gray")

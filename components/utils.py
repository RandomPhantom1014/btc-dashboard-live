# components/utils.py

from datetime import datetime

def format_timestamp(ts: float) -> str:
    """Converts a UNIX timestamp to human-readable format."""
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S UTC')

def get_signal_color(signal: str) -> str:
    """Returns a CSS color class based on the signal type."""
    if signal.lower() == 'go long':
        return 'pill_go_long'
    elif signal.lower() == 'go short':
        return 'pill_go_short'
    else:
        return 'pill_wait'

def truncate_price(value: float) -> str:
    """Formats BTC price with commas and no decimals."""
    return f"{int(value):,}"

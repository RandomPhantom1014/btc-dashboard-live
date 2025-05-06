# components/signal_output.py

from dash import html

def build_signal_output(signal_data):
    output_components = []

    for timeframe, data in signal_data.items():
        signal = data.get("signal", "Hold")
        confidence = data.get("confidence", 0)
        strength = data.get("strength", "Neutral")

        output_components.append(
            html.Div(className="signal-row", children=[
                html.Div(timeframe, className="signal-timeframe"),
                html.Div(signal, className=f"signal-pill {signal.lower()}"),
                html.Div(f"{confidence}%", className="signal-confidence"),
                html.Div(strength, className=f"signal-strength {strength.lower()}")
            ])
        )

    return html.Div(className="signal-output", children=output_components)

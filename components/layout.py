# In create_layout(), near the bottom before the Interval:
dbc.Row([
    dbc.Col([
        dbc.Button("Export Logs", id="export-button", color="info", className="me-2"),
        html.Span(id="export-status", className="text-success ms-2")
    ])
]),

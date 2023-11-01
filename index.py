import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import webbrowser
from app import app
from apps import sidebar as sb

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=True),
        sb.sidebar,
        html.Div(id="page-content", style=CONTENT_STYLE),
    ]
)

@app.callback(
    [
        Output("page-content", "children")
    ],
    [
        Input("url", "pathname")
    ],
)
def displaypage(pathname):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]["prop_id"].split(".")[0]
        if eventid == "url":
            if pathname == "/" or pathname == "/home":
                returnlayout = "home"
            elif pathname == "/records":
                returnlayout = "records"
            elif pathname == "/user":
                returnlayout = "user"
            elif pathname == "/reports":
                returnlayout = "reports"
            elif pathname == "/help":
                returnlayout = "help"
            else:
                returnlayout = "error404"
            return [returnlayout]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050/", new=0, autoraise=True)
    app.run_server(debug=False)
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
from apps.records import existingpatient, newpatient, viewrecords, editrecords, viewusers

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "width": "100%",
}

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=True),
        html.Div(
            [
                sb.sidebar,
                html.Div(id="page-content", style=CONTENT_STYLE),
            ],
            style = {'display':'flex'},
        )
    ],
    style={'width':'100%'}
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
                returnlayout = "This is the homepage"
            elif pathname == "/newrecord" or pathname == "/newrecord/newpatient":
                returnlayout = newpatient.layout
            elif pathname == "/newrecord/existingpatient":
                returnlayout = existingpatient.layout
            elif pathname == "/viewrecord":
                returnlayout = viewrecords.layout
            elif pathname == "/editrecord":
                returnlayout = editrecords.layout
            elif pathname == "/newuser":
                returnlayout = "Create new users here"
            elif pathname == "/viewuser":
                returnlayout = viewusers.layout
            elif pathname == "/managedata":
                returnlayout = "Manage the lists of veterinarian, clinician, clinical exam types, lab exam types, vaccines, and deworming medicines here"
            elif pathname == "/newreport":
                returnlayout = "Generate reports here"
            elif pathname == "/viewreport":
                returnlayout = "View previously generated reports here"
            elif pathname == "/help":
                returnlayout = "The user manual can be found here"
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
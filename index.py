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
from apps.records import general

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
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
                returnlayout = "This is the homepage"
            elif pathname == "/newrecord" or pathname == "/newrecord/patient":
                returnlayout = general.layout
            elif pathname == "/viewrecord":
                returnlayout = "View existing records here"
            elif pathname == "/newuser":
                returnlayout = "Create new users here"
            elif pathname == "/viewuser":
                returnlayout = "View existing users here"
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
    
@app.callback(
    [
        Output(link_id, 'style') for link_id in sb.newrecord_hidden_links
    ],
    [
        Input('url', 'pathname'),
    ]
)
def show_more_link(pathname):
    styles={'display':'none'}
    if pathname in ['/newrecord', '/newrecord/patient', '/newrecord/visit']:
        styles={'display':'block'}
    else:
        styles={'display':'none'}
    return [styles.copy() for _ in sb.newrecord_hidden_links]

    
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050/", new=0, autoraise=True)
    app.run_server(debug=False)

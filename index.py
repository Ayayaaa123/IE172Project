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
from apps import login, signup
from apps.records import existingpatient, newpatient, viewrecords, editrecords, viewusers, newusers, generatereports, editusers, home

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "width": "100%",
}

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=True),
        
        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=True, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),
        
        
        
        html.Div(
            sb.sidebar,
            id='sidebar_div'
        ),

        html.Div(
            [
                # sb.sidebar,
                html.Div(id="page-content", style=CONTENT_STYLE),
            ],
            style = {'display':'flex'},
        )
    ],
    style={'width':'100%'}
)

@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
        Output('sidebar_div', 'className'), # navbar changed to sidebar haha tama ba??
    ],
    [
        # If the path (i.e. part after the website name; 
        # in url = youtube.com/watch, path = '/watch') changes, 
        # the callback is triggered
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]
)
def displaypage(pathname, sessionlogout, userid):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]["prop_id"].split(".")[0]
        if eventid == "url":
            if userid < 0: # if logged out
                if pathname == '/':
                    returnlayout = login.layout
                elif pathname == '/signup':
                    returnlayout = signup.layout
                else:
                    returnlayout = '404: request not found'

            else:
                if pathname == '/logout':
                        returnlayout = login.layout
                        sessionlogout = True

                elif pathname == "/" or pathname == "/home":
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
                    returnlayout = "Parang same sa Sign Up page, tanggalin na ba?"
                elif pathname == "/viewuser":
                    returnlayout = viewusers.layout
                elif pathname == "/edituser":
                    returnlayout = editusers.layout
                elif pathname == "/managedata":
                    returnlayout = "Manage the lists of veterinarian, clinician, clinical exam types, lab exam types, vaccines, and deworming medicines here"
                elif pathname == "/newreport":
                    returnlayout = generatereports.layout
                elif pathname == "/viewreport":
                    returnlayout = "View previously generated reports here"
                elif pathname == "/help":
                    returnlayout = "The user manual can be found here"
                else:
                    returnlayout = "error404"
            # return [returnlayout]
        
            # decide sessionlogout value
            logout_conditions = [
                pathname in ['/', '/logout'],
                userid == -1,
                not userid
            ]
            sessionlogout = any(logout_conditions)
        
            sidebar_classname = 'd-none' if sessionlogout else ''
        
        
        else:
            raise PreventUpdate
    
        return [returnlayout, sessionlogout, sidebar_classname]
    else:
        raise PreventUpdate

    
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050/", new=0, autoraise=True)
    app.run_server(debug=False)
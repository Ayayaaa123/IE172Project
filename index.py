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
from apps import login
from apps.records import clinicalname, labname, existingpatient, newpatient, viewclinicians, viewrecords, editrecords, editvaccine, editdeworm, editproblem, viewusers, generatereports, editusers, home_visit, purpose, managedata, help, vaccname, dewormname, newclinician, editclinicians, newuser

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "width": "100%",
}

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        
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
        Output('sidebar_div', 'className'), 
    ],
    [
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
                    returnlayout = newuser.layout
                else:
                    returnlayout = '404: request not found'

            else:
                if pathname == '/logout':
                        returnlayout = login.layout
                        sessionlogout = True

                elif pathname == "/home_visit" or pathname == "/":
                    returnlayout = home_visit.layout
                elif pathname == "/purpose" or pathname == "/home_visit/purpose":
                    returnlayout = purpose.layout
                elif pathname == "/newrecord" or pathname == "/newrecord/newpatient":
                    returnlayout = newpatient.layout
                elif pathname == "/newrecord/existingpatient":
                    returnlayout = existingpatient.layout
                elif pathname == "/viewrecord":
                    returnlayout = viewrecords.layout
                elif pathname == "/editrecord":
                    returnlayout = editrecords.layout
                elif pathname == "/editvaccine":
                    returnlayout = editvaccine.layout
                elif pathname == "/editdeworm":
                    returnlayout = editdeworm.layout
                elif pathname == "/editproblem":
                    returnlayout = editproblem.layout
                elif pathname == "/newuser":
                    returnlayout = newuser.layout
                elif pathname == "/viewuser":
                    returnlayout = viewusers.layout
                elif pathname == "/edituser":
                    returnlayout = editusers.layout
                elif pathname == "/managedata":
                    returnlayout = managedata.layout
                elif pathname == "/managedata/newclinicians":
                    returnlayout = newclinician.layout
                elif pathname == "/managedata/existingclinicians":
                    returnlayout = viewclinicians.layout
                elif pathname == "/editclinician":
                    returnlayout = editclinicians.layout
                elif pathname == "/editclinicalexam":
                    returnlayout = clinicalname.layout
                elif pathname == "/editlabexamtype":
                    returnlayout = labname.layout
                elif pathname == "/editvaccinename":
                    returnlayout = vaccname.layout
                elif pathname == "/editdewormtype":
                    returnlayout = dewormname.layout        
                elif pathname == "/newreport":
                    returnlayout = generatereports.layout
                elif pathname == "/help":
                    returnlayout = help.layout
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
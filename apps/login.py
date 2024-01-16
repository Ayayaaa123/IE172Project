import hashlib
import dash_bootstrap_components as dbc
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db
import datetime
from dash import ALL, MATCH


layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardImg(src="assets/logo.webp", top=True, style={'width': '200px', 'height': 'auto', 'margin': 'auto'}),
           
                dbc.CardBody(
                    [  
                        html.Hr(),
                        html.H2('Please Login', style = {'font size': '24px'}),
                        html.Hr(),
                        dbc.Alert('Username or password is incorrect.', color="danger", id='login_alert',
                                is_open=False),
                        dbc.Row(
                            [
                                dbc.Label("Username", width=2, style={'font-size': '16px'}),
                                dbc.Col(
                                    dbc.Input(
                                        type="text", id="login_username", placeholder="Enter your username",
                                        style={'font-size': '16px'}),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Password", width=2, style={'font-size': '16px'}),
                                dbc.Col(
                                    dbc.Input(
                                        type="password", id="login_password", placeholder="Enter your password",
                                        style={'font-size': '16px'}),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                    ),
                    dbc.Button('Login', color="secondary", id='login_loginbtn'),
                    html.Hr(),
                    html.A('No Account Yet? Signup Here', href='/signup'),
                ]
            ),
        ],
        style={'max-width': '1024px', 'margin': 'auto', 'border': 0}
        ),
    ]
)




@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
    ],
    [
        Input('login_loginbtn', 'n_clicks'), # begin login query via button click
        Input('sessionlogout', 'modified_timestamp'), # reset session userid to -1 if logged out
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'),  
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
        State('url', 'pathname'),
    ]
)
def loginprocess(loginbtn, sessionlogout_time,
                 
                 username, password,
                 sessionlogout, currentuserid,
                 pathname):
   
    ctx = callback_context
   
    if ctx.triggered:
        openalert = False
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
   
   
    if eventid == 'login_loginbtn': # trigger for login process
   
        if loginbtn and username and password:
            sql = """SELECT vet_id
            FROM vet
            WHERE
                vet_email = %s AND
                vet_user_pw = %s AND
                NOT vet_delete_ind"""
           
            # we match the encrypted input to the encrypted password in the db
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
           
            values = [username, encrypt_string(password)]
            cols = ['vet_id']
            df = db.querydatafromdatabase(sql, values, cols)


            print(f"SQL Query: {sql}")
            print(f"Values: {values}")


            print(f"Result DataFrame: {df}")


            if df.shape[0]: # if query returns rows
                currentuserid = df['vet_id'][0]
            else:
                currentuserid = -1
                openalert = True
               
    elif eventid == 'sessionlogout' and pathname == '/logout': # reset the userid if logged out
        currentuserid = -1
       
    else:
        raise PreventUpdate
   
    return [openalert, currentuserid]




@app.callback(
    [
        Output('url', 'pathname'),
    ],
    [
        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('currentuserid', 'data'),
    ]
)
def routelogin(logintime, userid):
    ctx = callback_context
    if ctx.triggered:
        if userid > 0:
        # if userid and userid.startswith('USER'):
            url = '/home'
        else:
            url = '/'
    else:
        raise PreventUpdate
    return [url]
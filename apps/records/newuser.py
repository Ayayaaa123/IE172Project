import hashlib
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db


layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardImg(src="assets/logo.webp", top=True, style={'width': '200px', 'height': 'auto', 'margin': 'auto'}),
                dbc.CardBody(
                    [
                        html.H2('Create User Profile', style={'text-align': 'center'}),
                        html.Hr(),
                        dbc.Alert('Please supply the necessary details.', color="danger", id='signup_alert', is_open=False),
                       
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("First Name"),
                                dbc.Input(id='vet_fn', type='text', placeholder="Enter First Name"),
                            ],
                            className="mb-3",
                        ),
                       
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Last Name"),
                                dbc.Input(id='vet_ln', type='text', placeholder="Enter Last Name"),
                            ],
                            className="mb-3",
                        ),


                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Middle Initial"),
                                dbc.Input(id='vet_mi', type='text', placeholder="Enter MI"),
                                dbc.InputGroupText("Suffix (leave blank if none)"),
                                dbc.Input(id='vet_suffix', type='text', placeholder="e.g. Jr."),
                            ],
                            className="mb-3",
                        ),
                       
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Contact Number"),
                                dbc.Input(id='vet_cn', type='text', placeholder="09XXXXXXXXX"),
                            ],
                            className="mb-3",
                        ),


                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Username"),
                                dbc.Input(type="text", id="signup_username", placeholder="exampleusername@gmail.com"),
                            ],
                            className="mb-3",
                        ),
                       
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Password"),
                                dbc.Input(type="password", id="signup_password", placeholder="Enter a password"),
                            ],
                            className="mb-3",
                        ),
                       
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Confirm Password"),
                                dbc.Input(type="password", id="signup_passwordconf", placeholder="Re-type the password"),
                            ],
                            className="mb-3",
                        ),
                       
                        dbc.Button('Sign up', color="secondary", id='signup_signupbtn'),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Account Saved")),
                                dbc.ModalBody("Your Profile has been successfully created!", id='signup_confirmation', style={'font-size': '18px'}),
                                dbc.ModalFooter(
                                    dbc.Button("Okay", href='/viewuser')
                                ),
                            ],
                            id="signup_modal",
                            is_open=False,
                        ),
                    ]
                ),
            ],
            style={'max-width': '900px', 'margin': 'auto', 'border': 0}
        ),
    ]
)




# @app.callback(
#     Output('signup_modal', 'is_open'),
#     [
#         Input('signup_modal', 'n_clicks'),
#     ]
# )
# def redirect_to_home(n_clicks_modal):
#     if n_clicks_modal:
#         return True
#     return False




# disable the signup button if passwords do not match
@app.callback(
    [
        Output('signup_signupbtn', 'disabled'),
    ],
    [
        Input('signup_password', 'value'),
        Input('signup_passwordconf', 'value'),
    ]
)
def deactivatesignup(password, passwordconf):
   
    # enable button if password exists and passwordconf exists
    #  and password = passwordconf
    enablebtn = password and passwordconf and password == passwordconf


    return [not enablebtn]

# To save the user
@app.callback(
    [
        Output('signup_alert', 'is_open'),
        Output('signup_modal', 'is_open')  
    ],
    [
        Input('signup_signupbtn', 'n_clicks'),
    ],
    [
        State('vet_fn', 'value'),
        State('vet_ln', 'value'),
        State('vet_mi', 'value'),
        State('vet_suffix', 'value'),
        State('vet_cn', 'value'),
        State('signup_username', 'value'),
        State('signup_password', 'value'),
        State('signup_passwordconf', 'value')
    ]
)
def saveuser(signup_signupbtn, vet_fn, vet_ln, vet_mi, vet_suffix, vet_cn, username, password, passwordconf):
    openalert = openmodal = False
    if signup_signupbtn:
        if username and password:
            sql = """INSERT INTO vet (vet_fn, vet_ln, vet_mi, vet_suffix, vet_cn, vet_email, vet_user_pw)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""  
           
            # This lambda fcn encrypts the password before saving it
            # for security purposes, not even database admins should see
            # user passwords
            #encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
           
            values = [vet_fn, vet_ln, vet_mi, vet_suffix, vet_cn, username, password]
            db.modifydatabase(sql, values)
           
            openmodal = True
        else:
            openalert = True
    else:
        raise PreventUpdate


    return [openalert, openmodal]
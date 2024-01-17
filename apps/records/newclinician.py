from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_mantine_components as dmc
from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H2('Create Clinicians Profile', style={'text-align': 'center'}),
                        html.Hr(),
                        dbc.Alert('Please supply the necessary details.', color="danger", id='signup_alert', is_open=False),
                       
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("First Name"),
                                dbc.Input(id='clinician_fn', type='text', placeholder="Enter First Name"),
                            ],
                            className="mb-3",
                        ),
                       
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Last Name"),
                                dbc.Input(id='clinician_ln', type='text', placeholder="Enter Last Name"),
                            ],
                            className="mb-3",
                        ),


                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Middle Initial"),
                                dbc.Input(id='clinician_mi', type='text', placeholder="Enter MI"),
                                dbc.InputGroupText("Suffix (N/A if none)"),
                                dbc.Input(id='clinician_suffix', type='text', placeholder="e.g. Jr."),
                            ],
                            className="mb-3",
                        ),
                       
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Contact Number"),
                                dbc.Input(id='clinician_cn', type='text', placeholder="Enter Contact Number"),
                            ],
                            className="mb-3",
                        ),


                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Email"),
                                dbc.Input(type="text", id="clinician_email", placeholder="exampleusername@gmail.com"),
                            ],
                            className="mb-3",
                        ),
                       
            
                       
                        dbc.Button('Submit', color="secondary", id='clinician_submitbtn'),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Account Saved")),
                                dbc.ModalBody("Clinician Profile has been successfully created!", id='submit_confirmation', style={'font-size': '18px'}),
                                dbc.ModalFooter(
                                    dbc.Button("Okay", href='/managedata/existingclinicians')
                                ),
                            ],
                            id="cliniciansubmit_modal",
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
#     [
#         Output('cliniciansubmit_modal', 'is_open'),
#         Output('submit_confirmation', 'children')
#     ],
#     [
#         Input('clinician_submitbtn', 'n_clicks')
#     ],
#     [
#         State('clinician_fn', 'value'),
#         State('clinician_ln', 'value'),
#         State('clinician_mi', 'value'),
#         State('clinician_suffix', 'value'),
#         State('clinician_cn', 'value'),
#         State('clinician_email', 'value'),
#     ]
# )

# def saveclinician(clinician_submitbtn, n_clicks, clinician_fn, clinician_ln, clinician_mi, clinician_suffix, clinician_cn, clinician_email):
#     if n_clicks:
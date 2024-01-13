from dash import dcc #interpreter recommended to replace 'import dash_core_components as dcc' with 'from dash import dcc'
from dash import html #interpreter recommended to replace 'import dash_html_components as html' with 'from dash import html'
import dash_bootstrap_components as dbc
from dash import dash_table #interpreter recommended to replace 'import dash_table' with 'from dash import dash_table'
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_mantine_components as dmc
from app import app
from apps import dbconnect as db
import datetime
from dash import ALL, MATCH

layout = html.Div(
    [
        html.H1("Register New User"),
        html.Hr(),
        dbc.Alert(id='newuserprofile_alert', is_open=False), # For feedback purposes
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Personal Information")
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Last Name"),
                                        dbc.Input(id='vet_ln', type='text', placeholder='Enter Last Name', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("First Name"),
                                        dbc.Input(id='vet_fn', type='text', placeholder='Enter First Name', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Middle Initial"),
                                        dbc.Input(id='vet_mi', type='text', placeholder='Enter Middle Initial', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Suffix (N/A if none)"),
                                        dbc.Input(id='vet_suffix', type='text', placeholder='Enter Suffix', style={'width':'80%'})
                                        
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ), # end of row for owner name
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        # dbc.InputGroupText("@"), dbc.Input(placeholder='Enter Username')
                                        dbc.Label("Email Address"),
                                        dbc.Input(id='vet_email', type='text', placeholder='Enter Email Address', style={'width':'80%'}),
                                        dbc.FormText(
                                            "example@gmail.com",
                                            color = "secondary",
                                        )
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Contact Number"),
                                        dbc.Input(id='vet_cn', type='text', placeholder='Enter Contact Number', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ), # end of row of email address, contact num, province    
                    ],
                )
            ],
            style={'width':'100%'}
        ), # end of card for owner information
        
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Account Information")
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Username"),
                                        dbc.Input(id='vet_user_name', type='text', placeholder='Create Account Username', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Create Password"),
                                        dbc.Input(id='vet_user_password', type='password', placeholder='Enter Password', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className = "mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Confirm Password"),
                                        dbc.Input(id='vet_user_confirm_password', type='password', placeholder='Re-Enter Password', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className = "mb-3",
                        ),
                    ]
                )
            ]
        
        ),
        html.Br(),
        dbc.Button(
            'Submit',
            id = 'newuserprofile_submit',
            n_clicks = 0, #initialization 
            className='custom-submitbutton',
        ),
        dbc.Modal( # dialog box for successful saving of profile
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    'Edit this message',
                    id = 'newuserprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Submit",
                        href = '/home', # bring user back to homepage
                        id = 'newuserprofile_btn_modal',
                    )                    
                )
            ],
            centered=True,
            id='newuserprofile_successmodal',
            backdrop='static' # dialog box does not go away if you click at the background
        )






        # dbc.Button(
        #     'Submit',
        #     id = 'newuserprofile_submit',
        #     n_clicks=0
        # ),
        # dbc.Modal(
        #     [
        #         dbc.ModalHeader(
        #             'Message here'
        #         ),
        #         dbc.ModalFooter(
        #             "Submit",
        #             href = '/'
        #         )
        #     ]
        # )
    ]
)


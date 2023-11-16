import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_mantine_components as dmc
from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("General Information"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3("Owner Information")
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Last Name"),
                                        dbc.Input(id='owner_ln', type='text', placeholder='Enter Last Name', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("First Name"),
                                        dbc.Input(id='owner_fn', type='text', placeholder='Enter First Name', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Middle Initial"),
                                        dbc.Input(id='owner_mi', type='text', placeholder='Enter Middle Initial', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Email Address"),
                                        dbc.Input(id='owner_email', type='text', placeholder='Enter Email Address', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Contact Number"),
                                        dbc.Input(id='owner_cn', type='text', placeholder='Enter Contact Number', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Province"),
                                        dbc.Input(id='province', type='text', placeholder='Enter Province', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("City"),
                                        dbc.Input(id='city', type='text', placeholder='Enter City', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Barangay"),
                                        dbc.Input(id='barangay', type='text', placeholder='Enter Barangay', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                                 dbc.Col(
                                    [
                                        dbc.Label("Street"),
                                        dbc.Input(id='street', type='text', placeholder='Enter Street', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                            ],
                            className="mb-3",
                        )
                    ],
                )
            ],
            style={'width':'100%'}
        ),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3("Patient Information")
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Name"),
                                        dbc.Input(id='patient_m', type='text', placeholder='Enter Patient Name', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Sex"),
                                        dcc.Dropdown(
                                            id='patient_sex',
                                            options=[
                                                {'label':'Male', 'value':'male'},
                                                {'label':'Female', 'value':'female'},
                                            ],
                                            placeholder='Select Sex',
                                            style={'width':'75%'},
                                        ),
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Breed"),
                                        dbc.Input(id='patient_breed', type='text', placeholder='Enter Breed', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Birthdate"),
                                        dmc.DatePicker(
                                            id='patient_bd',
                                            style={'width':'75%'},
                                            inputFormat='MMM DD, YYYY',
                                        ),
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Idiosyncrasies"),
                                        dbc.Input(id='patient_idiosync', type='text', placeholder='Enter Idiosyncrasies', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Color Markings"),
                                        dbc.Input(id='patient_color', type='text', placeholder='Enter Color Markings', style={'width':'75%'})
                                    ],
                                    width=4
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                )
            ],
            style={'width':'100%'}
        ),
    ]
)

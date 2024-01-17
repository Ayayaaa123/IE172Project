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
from urllib.parse import urlparse, parse_qs




layout = html.Div(
    [
        html.H1("Edit Clinician Profile"),
        html.Hr(),
        dbc.Alert(id='editclinicianprofile_alert', is_open=False), # For feedback purposes
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
                                        dbc.Input(id='clinician_ln', type='text', placeholder='Enter Last Name', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("First Name"),
                                        dbc.Input(id='clinician_fn', type='text', placeholder='Enter First Name', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Middle Initial"),
                                        dbc.Input(id='clinician_mi', type='text', placeholder='Enter Middle Initial', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Suffix (N/A if none)"),
                                        dbc.Input(id='clinician_suffix', type='text', placeholder='Enter Suffix', style={'width':'80%'})
                                       
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
                                        dbc.Label("Email"),
                                        dbc.Input(id='clinician_email', type='text', placeholder='Enter Email Address', style={'width':'80%'}),
                                        # dbc.FormText(
                                        #     "example@gmail.com",
                                        #     color = "secondary",
                                        # )
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Contact Number"),
                                        dbc.Input(id='clinician_cn', type='text', placeholder='Enter Contact Number', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ),  # end of row
                    ],
                )
            ],
            style={'width':'100%'}
        ), # end
       
        html.Br(),
        html.Br(),
        dbc.Button(
            'Save',
            id = 'editclinician_savebtn',
            n_clicks = 0, #initialization
            className='custom-submitbutton',
        ),
        dbc.Modal( # dialog box for successful saving of profile
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    'Clinician profile has been updated',
                    id = 'editclinicianrprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay",
                        href = '/managedata/existingclinicians', # bring user back to table
                        id = 'editclinicianprofile_btn_modal',
                    )                    
                )
            ],
            centered=True,
            id='editclinicianprofile_successmodal',
            backdrop='static' # dialog box does not go away if you click at the background


        )
    ]
)


#CALLBACK TO LOAD EDIT PAGE
@app.callback(
    [
        Output('clinician_fn', 'value'),
        Output('clinician_ln', 'value'),
        Output('clinician_mi', 'value'),
        Output('clinician_suffix', 'value'),
        Output('clinician_email', 'value'),
        Output('clinician_cn', 'value'),  # Corrected column name here
    ],
    [
        Input('url', 'search'),
    ],
)
def current_values(url_search):
    parsed = urlparse(url_search)
    query_clinician_id = parse_qs(parsed.query)

    if 'id' in query_clinician_id:
        clinician_id = query_clinician_id['id'][0]
        sql = """
            SELECT clinician_fn, clinician_ln, clinician_mi, clinician_suffix, clinician_email, clinician_cn  
            FROM clinician
            WHERE clinician_id = %s
        """
        values = [clinician_id]
        col = ['clinician_fn', 'clinician_ln', 'clinician_mi', 'clinician_suffix', 'clinician_email', 'clinician_cn']

        df = db.querydatafromdatabase(sql, values, col)
       
        clinician_fn = df['clinician_fn'][0]
        clinician_ln = df['clinician_ln'][0]
        clinician_mi = df['clinician_mi'][0]
        clinician_suffix = df['clinician_suffix'][0]
        clinician_email = df['clinician_email'][0]
        clinician_cn = df['clinician_cn'][0]

        print(clinician_fn, clinician_ln, clinician_mi, clinician_suffix, clinician_email, clinician_cn)

        return [clinician_fn, clinician_ln, clinician_mi, clinician_suffix, clinician_email, clinician_cn]
    else:
        raise PreventUpdate

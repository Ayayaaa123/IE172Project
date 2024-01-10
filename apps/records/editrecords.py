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
        html.H1(id='patientname'),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Owner Information")
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Last Name"),
                                        dbc.Input(id='client_ln', type='text', placeholder='Enter Last Name', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("First Name"),
                                        dbc.Input(id='client_fn', type='text', placeholder='Enter First Name', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Middle Initial"),
                                        dbc.Input(id='client_mi', type='text', placeholder='Enter Middle Initial', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Suffix (N/A if none)"),
                                        dbc.Input(id='client_suffix', type='text', placeholder='Enter Suffix', style={'width':'80%'})
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
                                        dbc.Label("Email Address"),
                                        dbc.Input(id='client_email', type='text', placeholder='Enter Email Address', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Contact Number"),
                                        dbc.Input(id='client_cn', type='text', placeholder='Enter Contact Number', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Province"),
                                        dbc.Input(id='client_province', type='text', placeholder='Enter Province', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("City"),
                                        dbc.Input(id='client_city', type='text', placeholder='Enter City', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ), # end of row of email address, contact num, province
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Barangay"),
                                        dbc.Input(id='client_barangay', type='text', placeholder='Enter Barangay', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Street"),
                                        dbc.Input(id='client_street', type='text', placeholder='Enter Street', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("House Number"),
                                        dbc.Input(id='client_house_no', type='text', placeholder='Enter House Number', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ) # end of address row part 2
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
                        html.H2("Patient Information")
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
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Sex"),
                                        dcc.Dropdown(
                                            id='patient_sex',
                                            options=[
                                                {'label':'Male', 'value':'Male'},
                                                {'label':'Female', 'value':'Female'},
                                            ],
                                            placeholder='Select Sex',
                                            style={'width':'86.5%'},
                                        ),
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Type"),
                                        dbc.Input(id='patient_type', type='text', placeholder='Enter Type', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Breed"),
                                        dbc.Input(id='patient_breed', type='text', placeholder='Enter Breed', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ), # end of row for name, sex, breed
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Birthdate"),
                                        dmc.DatePicker(
                                            id='patient_bd',
                                            placeholder="Select Birthdate",
                                            style={'width':'75%'},
                                            inputFormat='MMM DD, YYYY',
                                            dropdownType='modal',
                                        ),
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Idiosyncrasies"),
                                        dbc.Input(id='patient_idiosync', type='text', placeholder='Enter Idiosyncrasies', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Color Markings"),
                                        dbc.Input(id='patient_color', type='text', placeholder='Enter Color Markings', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ), # end of row for birthdate, idiosyncrasies, color markings
                    ],  
                ) 
            ],
            style={'width':'100%'}
        ), # end of card for patient information    
        html.Br(),
        dbc.Button(
            'Save',
            id = 'profile_save',
            n_clicks = 0,
            className='custom-submitbutton',
        )
    ]
)


@app.callback(
    [
        Output('client_ln', 'value'),
        Output('client_fn', 'value'),
        Output('client_mi', 'value'),
        Output('client_suffix', 'value'),
        Output('client_email', 'value'),
        Output('client_cn', 'value'),
        Output('client_province', 'value'),
        Output('client_city', 'value'),
        Output('client_barangay', 'value'),
        Output('client_street', 'value'),
        Output('client_house_no', 'value'),
        Output('patient_m', 'value'),
        Output('patient_sex', 'value'),
        Output('patient_type', 'value'),
        Output('patient_breed', 'value'),
        Output('patient_bd', 'value'),
        Output('patient_idiosync', 'value'),
        Output('patient_color', 'value'),
    ],
    [
        Input('url', 'search'),
    ],
)
def initial_values(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]
        sql = """
            SELECT client_ln, client_fn, client_mi, client_suffix, client_email, client_cn, client_province, client_city, client_barangay, client_street, client_house_no,
            patient_m, patient_sex, patient_type, patient_breed, patient_bd, patient_idiosync, patient_color

            FROM patient
            INNER JOIN client ON patient.client_id = client.client_id

            WHERE patient_id = %s
        """
        values = [patient_id]
        col = ['client_ln', 'client_fn', 'client_mi', 'client_suffix', 'client_email', 'client_cn', 'client_province', 'client_city', 'client_barangay', 'client_street', 'client_house_no',
            'patient_m', 'patient_sex', 'patient_type', 'patient_breed', 'patient_bd', 'patient_idiosync', 'patient_color']
        
        df = db.querydatafromdatabase(sql, values, col)
        
        client_ln = df['client_ln'][0]
        client_fn = df['client_fn'][0]
        client_mi = df['client_mi'][0]
        client_suffix = df['client_suffix'][0]
        client_email = df['client_email'][0]
        client_cn = df['client_cn'][0]
        client_province = df['client_province'][0]
        client_city = df['client_city'][0]
        client_barangay = df['client_barangay'][0]
        client_street = df['client_street'][0]
        client_house_no = df['client_house_no'][0]
        patient_m = df['patient_m'][0]
        patient_sex = df['patient_sex'][0]
        patient_type = df['patient_type'][0]
        patient_breed = df['patient_breed'][0]
        patient_bd = df['patient_bd'][0]
        patient_idiosync = df['patient_idiosync'][0]
        patient_color = df['patient_color'][0]

        return [client_ln, client_fn, client_mi, client_suffix, client_email, client_cn, client_province, client_city, client_barangay, client_street, client_house_no, 
            patient_m, patient_sex, patient_type, patient_breed, patient_bd, patient_idiosync, patient_color]
    
    else:
        raise PreventUpdate
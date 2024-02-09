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
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="/viewrecord", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        dbc.Row([ #Client and Patient Information
            dbc.Col( #Patient Information (1st Column)
                dbc.Card([ #Patient Information Card
                    dbc.CardHeader(
                        html.Div([
                            html.H3("Patient Information", className = "flex-grow-1"),
                            dbc.Button("Edit Info", id = 'editrecords_patientdetails', n_clicks = 0),
                        ], className = "d-flex align-items-center justify-content-between"),
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.H6('Name:'), width = 3),
                            dbc.Col(html.H3(id='patient_m')),
                        ], style={"align-items": "center", "border-bottom": "1px solid #ccc"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Species:'), width = 3),
                            dbc.Col(html.H6(id='patient_species'), width = 4),
                            dbc.Col(html.H6('Breed:'), width = 2),
                            dbc.Col(html.H6(id='patient_breed'), width = 3),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Color Marks:'), width = 3),
                            dbc.Col(html.H6(id='patient_color'), width = 4),
                            dbc.Col(html.H6('Sex:'), width = 2),
                            dbc.Col(html.H6(id='patient_sex'), width = 3),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Birth date:'), width = 3),
                            dbc.Col(html.H6(id='patient_bd'), width = 4),
                            dbc.Col(html.H6('Age:'), width = 2),
                            dbc.Col(html.H6(id='patient_age'), width = 3),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Idiosyncracies:'), width = 3),
                            dbc.Col(html.H6(id='patient_idiosync')),
                        ], style={"align-items": "center"}),
                    ]),
                ]), width = 7,
            ),
            dbc.Col( #Client Information (2nd column)
                dbc.Card([ #Client Information Card
                    dbc.CardHeader(
                        html.Div([
                            html.H3("Client Information", className = "flex-grow-1"),
                            dbc.Button("Edit Info", id = 'editrecords_clientdetails', n_clicks = 0),
                        ], className = "d-flex align-items-center justify-content-between"),
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.H6('Name:'), width = 3),
                            dbc.Col(html.H3(id='client_name')),
                        ], style={"align-items": "center", "border-bottom": "1px solid #ccc"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Email:'), width = 3),
                            dbc.Col(html.H6(id='client_email')),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Contact No:'), width = 3),
                            dbc.Col(html.H6(id='client_cn')),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Address:'), width = 3),
                            dbc.Col(html.H6(id='client_address1')),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(width = 3),
                            dbc.Col(html.H6(id='client_address2')),
                        ], style={"align-items": "center"}),
                    ]),
                ]), width = 5,
            ),
        ]),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H2('Vaccine History')
                                ]
                            ),
                            dbc.CardBody(
                                [
                                    html.Div(  # create section to show list of records
                                        [
                                            html.Div(id='vaccine-table'),   
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    width=6  
                ), #vaccine history

                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H2('Deworming History')
                                ]
                            ),
                            dbc.CardBody(
                                [
                                    html.Div(  # create section to show list of records
                                        [
                                            html.Div(id='deworming-table'),   
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    width=6  
                ),#deworming history
            ]
        ), 
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Problem History")
                    ]
                ),
                dbc.CardBody(
                    [
                        html.Div([
                            html.Div(id='problem-table'),
                        ])
                    ]
                )
            ]
        ),
    ]
)


@app.callback(
    [
        Output('client_name', 'children'),
        Output('client_email', 'children'),
        Output('client_cn', 'children'),
        Output('client_address1', 'children'),
        Output('client_address2', 'children'),
        Output('patient_m', 'children'),
        Output('patient_sex', 'children'),
        Output('patient_species', 'children'),
        Output('patient_breed', 'children'),
        Output('patient_bd', 'children'),
        Output('patient_age', 'children'),
        Output('patient_idiosync', 'children'),
        Output('patient_color', 'children'),
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
            SELECT 
                client_fn || ' ' || COALESCE(client_mi, '') || '. ' || client_ln || ' ' || COALESCE(client_suffix, '') AS client_name,
                client_email, 
                client_cn, 
                COALESCE(client_house_no || ' ', '') || client_street || ' ' || client_barangay AS client_address1, 
                client_city || ', ' || client_region AS client_address2,
                patient_m, 
                patient_sex, 
                patient_species, 
                patient_breed, 
                patient_bd, 
                floor(extract(year from age(current_date, patient_bd))), 
                patient_idiosync, 
                patient_color
            FROM 
                patient
            INNER JOIN client ON patient.client_id = client.client_id
            WHERE patient_id = %s
        """
        values = [patient_id]
        col = ['client_name', 'client_email', 'client_cn', 'client_address1', 'client_address2',
            'patient_m', 'patient_sex', 'patient_species', 'patient_breed', 'patient_bd', 'patient_age', 'patient_idiosync', 'patient_color']
        
        df = db.querydatafromdatabase(sql, values, col)
        
        client_name = df['client_name'][0]
        client_email = df['client_email'][0]
        client_cn = df['client_cn'][0]
        client_address1 = df['client_address1'][0]
        client_address2 = df['client_address2'][0]
        patient_m = df['patient_m'][0]
        patient_sex = df['patient_sex'][0]
        patient_species = df['patient_species'][0]
        patient_breed = df['patient_breed'][0]
        patient_bd = df['patient_bd'][0]
        patient_age_number = df['patient_age'][0]
        patient_age = str(patient_age_number) + " years old"
        patient_idiosync = df['patient_idiosync'][0]
        patient_color = df['patient_color'][0]

        return [client_name, client_email, client_cn, client_address1, client_address2, 
            patient_m, patient_sex, patient_species, patient_breed, patient_bd, patient_age, patient_idiosync, patient_color]
    
    else:
        raise PreventUpdate
    

@app.callback(
    Output('vaccine-table', 'children'),
    Input('url', 'search'),
)
def vaccine_table(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]
        sql = """
        SELECT 
            vacc_m, vacc_dose, vacc_date_administered, vacc_exp, vacc_id, patient.patient_id
        FROM 
            vacc
        INNER JOIN visit ON vacc.visit_id = visit.visit_id
        INNER JOIN patient ON visit.patient_id = patient.patient_id
        INNER JOIN vacc_m ON vacc.vacc_m_id = vacc_m.vacc_m_id
        WHERE patient.patient_id = %s
        """
        values = [patient_id]
        sql += "ORDER BY vacc_date_administered DESC"
        col = ['Vaccine Name', 'Dose', 'Date Administered', 'Expiration Date', 'Vacc_ID', 'Patient_ID']
        df = db.querydatafromdatabase(sql, values, col)

        if df.shape:
            buttons = []
            for vacc_id, patient_id_query in zip(df['Vacc_ID'], df['Patient_ID']):
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editvaccine?mode=edit&vacc_id={vacc_id}&patient_id={patient_id_query}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Vaccine Name', 'Dose', 'Date Administered', 'Expiration Date', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate

@app.callback(
    Output('deworming-table', 'children'),
    Input('url', 'search'),
)

def deworm_table(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]
        sql = """
        SELECT 
            deworm_m, deworm_dose, deworm_administered, deworm_exp, deworm_id, patient.patient_id
        FROM 
            deworm
        INNER JOIN visit ON deworm.visit_id = visit.visit_id
        INNER JOIN patient ON visit.patient_id = patient.patient_id
        INNER JOIN deworm_m ON deworm.deworm_m_id = deworm_m.deworm_m_id
        WHERE patient.patient_id = %s 
        """
        values = [patient_id]
        sql += "ORDER BY deworm_administered DESC"
        col = ['Medicine Name', 'Dose', 'Date Administered', 'Expiration Date', 'Deworm_ID', 'Patient_ID']
        df = db.querydatafromdatabase(sql, values, col)

        if df.shape:
            buttons = []
            for deworm_id, patient_id_query in zip(df['Deworm_ID'], df['Patient_ID']):
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editdeworm?mode=edit&deworm_id={deworm_id}&patient_id={patient_id_query}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Medicine Name', 'Dose', 'Date Administered', 'Expiration Date', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate
    

@app.callback(
    Output('problem-table', 'children'),
    Input('url', 'search'),
)

def problem_table(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]
        sql = """
        SELECT DISTINCT
            problem_chief_complaint, problem_diagnosis, problem_prescription, problem_client_educ, problem_status_m, problem_date_created, problem_date_resolved, problem.problem_id, patient.patient_id
        FROM 
            problem
        INNER JOIN problem_status ON problem.problem_status_id = problem_status.problem_status_id
        INNER JOIN visit ON problem.problem_id = visit.problem_id
        INNER JOIN patient ON visit.patient_id = patient.patient_id
        WHERE patient.patient_id = %s 
        """
        values = [patient_id]
        sql += "ORDER BY problem.problem_id DESC"
        col = ['Chief Complaint', 'Diagnosis', 'Prescription', 'Patient Instructions', 'Problem Status', 'Start Date', 'Resolved Date', 'Problem_ID', 'Patient_ID']
        df = db.querydatafromdatabase(sql, values, col)

        if df.shape:
            buttons = []
            for problem_id, patient_id_query in zip(df['Problem_ID'], df['Patient_ID']):
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editproblem?mode=edit&problem_id={problem_id}&patient_id={patient_id_query}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Chief Complaint', 'Diagnosis', 'Prescription', 'Patient Instructions', 'Problem Status', 'Start Date', 'Resolved Date', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate
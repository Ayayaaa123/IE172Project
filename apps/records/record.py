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
from datetime import datetime

layout = html.Div(
    [
        html.H1("New Visit"),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.H4("Select Patient"),
                            dcc.Dropdown(
                                id="searchfilter_patientvisit",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ]
                    )
                ),
            ]
        ),
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.H4("Select Veterinarian"),
                            dcc.Dropdown(
                                id="searchfilter_vetvisit",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ]
                    )
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Visit Date"),
                        dmc.DatePicker(
                            id='visit_date',
                            placeholder="Select Visit Date",
                            value=datetime.now().date(),
                            inputFormat='MMM DD, YYYY',
                            dropdownType='modal',
                            ),
                    ],
                ),    
            ]
        ),
        html.Br(),
        dbc.Col(html.H4("Visit Purpose")),
        dcc.Checklist(
            options=[
                {"label": "New Problem", "style":{"flex-grow": 1}, "value": "new_problem"},
                {"label": "Follow up to a Problem", "style":{"flex-grow": 1}, "value": "follow_up"},
                {"label": "Vaccination", "style":{"flex-grow": 1}, "value": "vaccination"},
                {"label": "Deworming", "style":{"flex-grow": 1}, "value": "deworming"},
            ],
            id="visit_purpose",
            inline=True,
            style={"display": "flex", 
                   "justify-content": "space-between", 
                   "fontSize":"1.2rem",
                   "align-items":"center"},
        ),
        html.Div(id="additional-inputs"),
    ]
)


@app.callback(
    Output("additional-inputs", "children"),
    [Input("visit_purpose", "value")],
    [State("visit_purpose", "value")]
)
def update_additional_inputs(_, selected_services):
    if selected_services is None:
        return []
    
    inputs = []
    if 'vaccination' in selected_services:
        inputs.extend([
            html.Br(),
            html.H4("Select Vaccine/s and Dose Number"),
            dcc.Dropdown(
                id="vaccine_list",
                searchable=True,
                options=[],
                value=None,
                multi=True,
            ),
        ])
    if 'deworming' in selected_services:
        inputs.extend([
            html.Br(),
            html.H4("Select Deworming and Dose Number"),
            dcc.Dropdown(
                id="deworm_list",
                searchable=True,
                options=[],
                value=None,
                multi=True,
            ),
        ])
    if 'new_problem' in selected_services:
        inputs.extend([
            html.Br(),
            html.H4("Chief Complaint"),
            dcc.Input(
                id='new-problem-input',
                type='text',
                placeholder='Enter Problem',
                style={'width':'50%'},
            ),
            html.Br(),
        ])
    if 'follow_up' in selected_services:
        inputs.extend([
            html.Br(),
            html.H4("Select Problem"),
            dcc.Dropdown(
                id="problem_list",
                searchable=True,
                options=[],
                value=None,
            ),
            html.Br(),
            dcc.Checklist(
                id='follow-up-options',
                options=[
                    {'label': 'Create Progress Notes', 'value': 'progress_notes'},
                    {'label': 'Create Lab Exam Records', 'value': 'lab_exam_records'}
                ],
                style={"fontSize":"1.15rem"},
                value=[]
            )
        ])
    return inputs


@app.callback(
    [
        Output('searchfilter_patientvisit', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('searchfilter_patientvisit', 'value'),
    ]
)
def newvisit_loadpatient(pathname, searchterm):
    if pathname == "/newrecord/visit" and not searchterm:
        sql = """ 
            SELECT 
                patient_id,
                COALESCE(patient_m, '') || ' - ' || COALESCE(client_ln, '') || ', ' || COALESCE(client_fn, '') || ' ' || COALESCE(client_mi, '') AS patient_name
            FROM 
                patient
            INNER JOIN 
                client ON patient.client_id = client.client_id  
            WHERE 
                NOT patient_delete_ind 
                AND NOT client_delete_ind 
            """
        values = []
        cols = ['patient_id', 'patient_name']
        if searchterm:
            sql += """ AND (
                patient_m ILIKE %s 
                OR client_ln ILIKE %s 
                OR client_fn ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['patient_name'], 'value': row['patient_id']} for _, row in result.iterrows()]
    return options, 


@app.callback(
    [
        Output('searchfilter_vetvisit', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('searchfilter_vetvisit', 'value'),
    ]
)
def newvisit_loadpatient(pathname, searchterm):
    if pathname == "/newrecord/visit" and not searchterm:
        sql = """ 
            SELECT 
                vet_id,
                COALESCE(vet_ln, '') || ', ' || COALESCE(vet_fn, '') || ' ' || COALESCE(vet_mi, '') AS vet_name
            FROM 
                vet 
            WHERE 
                NOT vet_delete_ind 
            """
        values = []
        cols = ['vet_id', 'vet_name']
        if searchterm:
            sql += """ AND ( 
                vet_ln ILIKE %s 
                OR vet_fn ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['vet_name'], 'value': row['vet_id']} for _, row in result.iterrows()]
    return options, 


@app.callback(
    [
        Output('vaccine_list', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('vaccine_list', 'value'),
    ]
)
def newvisit_loadvaccines(pathname, searchterm):
    if pathname == "/newrecord/visit" and not searchterm:
        sql = """ 
            SELECT 
                vacc_m_id,
                vacc_m
            FROM 
                vacc_m 
            WHERE 
                NOT vacc_m_delete_ind 
            """
        values = []
        cols = ['vacc_id', 'vacc_m']
        if searchterm:
            sql += """ AND vacc_m ILIKE %s
            """
            values = [f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['vacc_m'], 'value': row['vacc_id']} for _, row in result.iterrows()]
    return options, 


@app.callback(
    [
        Output('deworm_list', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('deworm_list', 'value'),
    ]
)
def newvisit_loaddeworm(pathname, searchterm):
    if pathname == "/newrecord/visit" and not searchterm:
        sql = """ 
            SELECT 
                deworm_m_id,
                deworm_m
            FROM 
                deworm_m
            WHERE 
                NOT deworm_m_delete_ind 
            """
        values = []
        cols = ['deworm_id', 'deworm_m']
        if searchterm:
            sql += """ AND deworm_m ILIKE %s
            """
            values = [f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['deworm_m'], 'value': row['deworm_id']} for _, row in result.iterrows()]
    return options, 


@app.callback(
    [
        Output('problem_list', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('problem_list', 'value'),
        Input('searchfilter_patientvisit', 'value'),
    ]
)
def newvisit_loadproblems(pathname, searchterm, selected_patient):
    if pathname == "/newrecord/visit" and not searchterm:
        sql = """ 
            SELECT DISTINCT
                problem.problem_id,
                COALESCE(problem_no, '') || '.) ' || COALESCE(problem_chief_complaint, '') AS problem_name
            FROM 
                problem 
            INNER JOIN problem_status ON problem.problem_status_id = problem_status.problem_status_id
            INNER JOIN note ON problem.problem_id = note.problem_id
            INNER JOIN visit ON note.visit_id = visit.visit_id
            INNER JOIN patient ON visit.patient_id = patient.patient_id
            WHERE 
                NOT problem_delete_ind
                AND NOT problem_status_m = 'RESOLVED'
                AND patient.patient_id = %s
            """
        values = [selected_patient]
        cols = ['problem_id', 'problem_name']
        if searchterm:
            sql += """ AND problem.problem_chief_complaint ILIKE %s
            """
            values = [f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['problem_name'], 'value': row['problem_id']} for _, row in result.iterrows()]
    return options, 
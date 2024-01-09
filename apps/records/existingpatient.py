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
from dash import ALL, MATCH

layout = html.Div(
    [
        html.H1("Existing Patient"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Visit Information")
                    ]
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(html.H3("Select Patient"), width=3),
                        dbc.Col(
                                dcc.Dropdown(
                                    id="patientlist_existingpatient",
                                    placeholder="Select Patient",
                                    searchable=True,
                                    options=[],
                                    value=None,
                                ),
                        ),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.H3("Select Veterinarian"), width=3),
                        dbc.Col(
                                dcc.Dropdown(
                                    id="vetlist_existingpatient",
                                    placeholder="Select Veterinarian",
                                    searchable=True,
                                    options=[],
                                    value=None,
                                ),
                        ),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.H3("Visit Date"), width=3),
                        dbc.Col(
                                dmc.DatePicker(
                                id='visitdate_existingpatient',
                                placeholder="Select Visit Date",
                                value=datetime.now().date(),
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                                ),
                        ),    
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.H3("Visit Purpose"), width=3),
                        dbc.Col(
                            dcc.Checklist(
                            options=[
                                {"label": " New Problem", "style":{"flex-grow": 1}, "value": "new_problem"},
                                {"label": " Follow up to a Problem", "style":{"flex-grow": 1}, "value": "follow_up"},
                                {"label": " Vaccination", "style":{"flex-grow": 1}, "value": "vaccination"},
                                {"label": " Deworming", "style":{"flex-grow": 1}, "value": "deworming"},
                            ],
                            id="visitpurpose_existingpatient",
                            inline=True,
                            style={"display": "flex", 
                                "justify-content": "space-between", 
                                "fontSize":"1.2rem",
                                "align-items":"center"},
                            ),
                            width=9,
                        )
                    ]),
                ]),
            ],
        ),
        html.Div(id="visitinputs_existingpatient"),
        html.Br(),
        dbc.Button(
            'Submit',
            id = 'existingpatientprofile_submit',
            n_clicks = 0, #initialization 
            className='custom-submitbutton',
        ),
    ]
)


@app.callback( #callback for list of existing patients in the database
    [
        Output('patientlist_existingpatient', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('patientlist_existingpatient', 'value'),
    ]
)
def existingpatient_loadpatient(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
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


@app.callback(#callback for list of veterinarians
    [
        Output("vetlist_existingpatient", 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input("vetlist_existingpatient", 'value'),
    ]
)
def existingpatient_loadvet(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
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
            sql += """ AND vet_name ILIKE %s
            """
            values = [f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['vet_name'], 'value': row['vet_id']} for _, row in result.iterrows()]
    return options, 



@app.callback( #callback to add inputs depending on the selected visit purpose
    Output("visitinputs_existingpatient", "children"),
    Input("visitpurpose_existingpatient", "value"),
    State("visitpurpose_existingpatient", "value"),
)
def update_additional_inputs(_, selected_services):
    if selected_services is None:
        return []
    
    inputs = []
    if 'vaccination' in selected_services:
        inputs.extend([
            html.Div([
                html.Br(),
                dbc.Card(
                    [
                        dbc.CardHeader(
                            [
                                dbc.Row([
                                    dbc.Col(html.H2("Vaccine"), width=2),
                                    dbc.Col(dbc.Button("+", id='vaccine-addbutton_existingpatient', className='custom-button', n_clicks=0), width=2),
                                    dbc.Col(dbc.Button("-", id='vaccine-deletebutton_existingpatient', className='custom-button', n_clicks=0), width=2),
                                ]),
                            ]
                        ),
                        dbc.CardBody([
                            html.Div(id='vaccine-line-items_existingpatient'),
                        ]),
                    ],
                ),
            ])
        ]),
    if 'deworming' in selected_services:
        inputs.extend([
            html.Div([
                html.Br(),
                dbc.Card(
                    [
                        dbc.CardHeader(
                            [
                                dbc.Row([
                                    dbc.Col(html.H2("Deworming"), width=2),
                                    dbc.Col(dbc.Button("+", id='deworming-addbutton_existingpatient', className='custom-button', n_clicks=0), width=2),
                                    dbc.Col(dbc.Button("-", id='deworming-deletebutton_existingpatient', className='custom-button', n_clicks=0), width=2),
                                ]),
                            ]
                        ),
                        dbc.CardBody([
                            html.Div(id='deworming-line-items_existingpatient'),
                        ]),
                    ],
                ),
            ])
        ]),
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


vaccine_lineitem_existingpatient = []
deworming_lineitem_existingpatient = []

@app.callback( #callback for adding a row for vaccines administered
    [
        Output("vaccine-line-items_existingpatient", "children"),
    ],
    [
        Input("vaccine-addbutton_existingpatient", "n_clicks"),
        Input("vaccine-deletebutton_existingpatient", "n_clicks"),
    ],
)
def manage_vaccine_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "vaccine-addbutton_existingpatient" in triggered_id:
        if len(vaccine_lineitem_existingpatient) < addclick:
            i = len(vaccine_lineitem_existingpatient)
            vaccine_lineitem_existingpatient.extend([
                html.Div([
                    html.Div(style={'height':'5px'}),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id={"type": "patient_vaccine_existingpatient", "index": i},
                                placeholder='Select Vaccine',
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                            width = 4,
                        ),
                        dbc.Col(
                            dbc.Input(id={"type": "vaccine_dose_existingpatient", "index": i}, type='text', placeholder='Enter Dose'),
                            width = 2,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "vaccine_date_existingpatient", "index": i},
                                placeholder="Select Date Administered",
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                            ),
                            width = 3,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "vaccine_expdate_existingpatient", "index": i},
                                placeholder="Select Expiration Date",
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                            ),
                            width = 3,
                        ),
                    ]),
                    html.Div(style={'height':'5px'}),        
                ])
            ])  

    elif triggered_id and "vaccine-deletebutton_existingpatient" in triggered_id:
        if len(vaccine_lineitem_existingpatient) > 0:
            vaccine_lineitem_existingpatient.pop()
    
    else:
        raise PreventUpdate
    
    return [vaccine_lineitem_existingpatient]


@app.callback( #callback for adding a row for deworming medicines administered
    [
        Output("deworming-line-items_existingpatient", "children"),
    ],
    [
        Input("deworming-addbutton_existingpatient", "n_clicks"),
        Input("deworming-deletebutton_existingpatient", "n_clicks"),
    ],
)
def manage_deworming_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "deworming-addbutton_existingpatient" in triggered_id:
        if len(deworming_lineitem_existingpatient) < addclick:
            i = len(deworming_lineitem_existingpatient)
            deworming_lineitem_existingpatient.extend([
                html.Div([
                    html.Div(style={'height':'5px'}),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id={"type": "patient_deworming_existingpatient", "index": i},
                                placeholder='Select Deworming Medicine Used',
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                            width = 4,
                        ),
                        dbc.Col(
                            dbc.Input(id={"type": "deworm_dose_existingpatient", "index": i}, type='text', placeholder='Enter Dose'),
                            width = 2,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "deworming_date_existingpatient", "index": i},
                                placeholder="Select Date Administered",
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                            ),
                            width = 3,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "deworming_expdate_existingpatient", "index": i},
                                placeholder="Select Expiration Date",
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                            ),
                            width = 3,
                        ),
                    ]),
                    html.Div(style={'height':'5px'}),    
                ])
            ]) 

    elif triggered_id and "deworming-deletebutton_existingpatient" in triggered_id:
        if len(deworming_lineitem_existingpatient) > 0:
            deworming_lineitem_existingpatient.pop()

    else:
        raise PreventUpdate

    return [deworming_lineitem_existingpatient]



@app.callback( #callback to provide the list of vaccines on the dropdown
    [
        Output({"type": "patient_vaccine_existingpatient", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "patient_vaccine_existingpatient", "index": MATCH}, "value"),
    ]
)
def existingpatient_loadvaccines(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
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


@app.callback( #callback to provide the list of deworming medicines on the dropdown
    [
        Output({"type": "patient_deworming_existingpatient", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "patient_deworming_existingpatient", "index": MATCH}, 'value'),
    ]
)
def existingpatient_loaddeworm(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
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



# @app.callback(
#     [
#         Output('problem_list', 'options'),
#     ],
#     [
#         Input('url', 'pathname'),
#         Input('problem_list', 'value'),
#         Input('searchfilter_patientvisit', 'value'),
#     ]
# )
# def newvisit_loadproblems(pathname, searchterm, selected_patient):
#     if pathname == "/newrecord/visit" and not searchterm:
#         sql = """ 
#             SELECT DISTINCT
#                 problem.problem_id,
#                 COALESCE(problem_no, '') || '.) ' || COALESCE(problem_chief_complaint, '') AS problem_name
#             FROM 
#                 problem 
#             INNER JOIN problem_status ON problem.problem_status_id = problem_status.problem_status_id
#             INNER JOIN note ON problem.problem_id = note.problem_id
#             INNER JOIN visit ON note.visit_id = visit.visit_id
#             INNER JOIN patient ON visit.patient_id = patient.patient_id
#             WHERE 
#                 NOT problem_delete_ind
#                 AND NOT problem_status_m = 'RESOLVED'
#                 AND patient.patient_id = %s
#             """
#         values = [selected_patient]
#         cols = ['problem_id', 'problem_name']
#         if searchterm:
#             sql += """ AND problem.problem_chief_complaint ILIKE %s
#             """
#             values = [f"%{searchterm}%"]
#     else:
#         raise PreventUpdate  
     
#     result = db.querydatafromdatabase(sql, values, cols)
#     options = [{'label': row['problem_name'], 'value': row['problem_id']} for _, row in result.iterrows()]
#     return options, 
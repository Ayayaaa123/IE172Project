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
                            dbc.Checklist(
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
                                    dbc.Col(dbc.Button("+", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='vaccine-addbutton_existingpatient', className='custom-button', n_clicks=0), width=2),
                                    dbc.Col(dbc.Button("-", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='vaccine-deletebutton_existingpatient', className='custom-button', n_clicks=0), width=2),
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
                                    dbc.Col(dbc.Button("+", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='deworming-addbutton_existingpatient', className='custom-button', n_clicks=0), width=2),
                                    dbc.Col(dbc.Button("-", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='deworming-deletebutton_existingpatient', className='custom-button', n_clicks=0), width=2),
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
            html.Div([
                html.Br(),
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("New Problem")),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(html.H3("Problem"), width=3),
                                dbc.Col(
                                    dbc.Input(id="newproblem", type='text', placeholder='Enter Problem'),
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Health & food intake"), width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Relevant Medical History"),
                                        dbc.Textarea(id='newproblem_medhistory', placeholder='Enter Any Relevant Medical History', style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Diet"),
                                        dbc.Textarea(id='newproblem_diet', placeholder="Enter Patient's Diet", style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Water Source"),
                                        dbc.Textarea(id='newproblem_water', placeholder="Enter Patient's Water Source", style={"height":75})
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Health Assessment"), width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Temperature"),
                                        dbc.Input(id='newproblem_temp', type='text', placeholder='Enter Temperature')
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Pulse Rate"),
                                        dbc.Input(id='newproblem_pr', type='text', placeholder="Enter Pulse Rate")
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Respiration Rate"),
                                        dbc.Input(id='newproblem_rr', type='text', placeholder="Enter Respiration Rate")
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Weight"),
                                        dbc.Input(id='newproblem_weight', type='text', placeholder='Enter Weight')
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Body Condition Score"),
                                        dbc.Input(id='newproblem_bodyconditionscore', type='text', placeholder="Enter Body Condition Score")
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Notes"), width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Differential Diagnosis"),
                                        dbc.Textarea(id='newnote_differentialdiagnosis', placeholder='Enter Differential Diagnosis', style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Possible Treatment"),
                                        dbc.Textarea(id='newnote_treatment', placeholder='Enter Treatment Options', style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Tests Needed"),
                                        dbc.Textarea(id='newnote_tests', placeholder='Enter Tests Needed', style={"height":75})
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Tests Completed?"),
                                        dbc.RadioItems(
                                            options=[
                                                {"label": "Yes", "value": "true"},
                                                {"label": " No", "value": "false"},
                                            ],
                                            id="newnote_havebeentested",
                                            inline=False,
                                            style={
                                                "display": "flex",
                                                "justify-content": "between",
                                                "gap": "15px",
                                            },
                                        ),
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("OR No."),
                                        dbc.Input(id='newnote_OR_no', type='text', placeholder="Enter OR Number")
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Bill"),
                                        dbc.Input(id='newnote_bill', type='text', placeholder="Enter Bill")
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Clinical Exam"), width=3),
                                dbc.Col(dbc.Button("+", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='newclinicalexam-addbutton', className='custom-button', n_clicks=0), width=2),
                                dbc.Col(dbc.Button("-", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='newclinicalexam-deletebutton', className='custom-button', n_clicks=0), width=2),
                            ]),
                            html.Div(id='newclinicalexam-lineitems'),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Laboratory Exam"), width=3),
                                dbc.Col(dbc.Button("+", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='newlabexam-addbutton', className='custom-button', n_clicks=0), width=2),
                                dbc.Col(dbc.Button("-", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='newlabexam-deletebutton', className='custom-button', n_clicks=0), width=2),
                            ]),
                            html.Div(id='newlabexam-lineitems'),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Diagnosis & Prescription"), width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Diagnosis"),
                                        dbc.Textarea(id='newproblem_diagnosis', placeholder='Enter Diagnosis', style={"height":100})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Prescription"),
                                        dbc.Textarea(id='newproblem_prescription', placeholder="Enter Prescription", style={"height":100})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Patient instructions"),
                                        dbc.Textarea(id='newproblem_clienteduc', placeholder="Enter instructions", style={"height":100})
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Problem Status"), width=3),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='newproblem_status',
                                        options=[
                                            {'label':'Resolved', 'value':'resolved'},
                                            {'label':'Ongoing', 'value':'ongoing'},
                                            {'label':'Pending Diagnosis', 'value':'pending_diagnosis'},
                                            {'label':'For Follow-Up', 'value':'follow_up'},
                                            {'label':'Critical Condition', 'value':'critical_condition'},
                                            {'label':'For Surgery', 'value':'for_surgery'},
                                            {'label':'Post Surgery', 'value':'post_surgery'},
                                            {'label':'Under Observation', 'value':'under_observation'},
                                            {'label':'Deceased', 'value':'deceased'},
                                            {'label':'Unknown', 'value':'unknown'},
                                            {'label':'Waiting For Test Results', 'value':'pending_testresults'},
                                        ],
                                        placeholder='Select Problem Status',
                                    ),
                                    width = 9
                                )
                            ])
                        ]),
                    ],
                ),
            ])
        ]),
    if 'follow_up' in selected_services:
        inputs.extend([
            html.Div([
                html.Br(),
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Follow up to a Problem")),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(html.H3("Problem"), width=3),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="followupproblem",
                                        placeholder="Select Problem",
                                        searchable=True,
                                        options=[],
                                        value=None,
                                    ),
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Health & food intake"), width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Relevant Medical History"),
                                        dbc.Textarea(id='followupproblem_medhistory', placeholder='Enter Any Relevant Medical History', style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Diet"),
                                        dbc.Textarea(id='followupproblem_diet', placeholder="Enter Patient's Diet", style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Water Source"),
                                        dbc.Textarea(id='followupproblem_water', placeholder="Enter Patient's Water Source", style={"height":75})
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Health Assessment"), width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Temperature"),
                                        dbc.Input(id='followupproblem_temp', type='text', placeholder='Enter Temperature')
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Pulse Rate"),
                                        dbc.Input(id='followupproblem_pr', type='text', placeholder="Enter Pulse Rate")
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Respiration Rate"),
                                        dbc.Input(id='followupproblem_rr', type='text', placeholder="Enter Respiration Rate")
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Weight"),
                                        dbc.Input(id='followupproblem_weight', type='text', placeholder='Enter Weight')
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Body Condition Score"),
                                        dbc.Input(id='followupproblem_bodyconditionscore', type='text', placeholder="Enter Body Condition Score")
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Notes"), width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Differential Diagnosis"),
                                        dbc.Textarea(id='followupnote_differentialdiagnosis', placeholder='Enter Differential Diagnosis', style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Possible Treatment"),
                                        dbc.Textarea(id='followupnote_treatment', placeholder='Enter Treatment Options', style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Tests Needed"),
                                        dbc.Textarea(id='followupnote_tests', placeholder='Enter Tests Needed', style={"height":75})
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Tests Completed?"),
                                        dbc.RadioItems(
                                            options=[
                                                {"label": "Yes", "value": "true"},
                                                {"label": " No", "value": "false"},
                                            ],
                                            id="followupnote_havebeentested",
                                            inline=False,
                                            style={
                                                "display": "flex",
                                                "justify-content": "between",
                                                "gap": "15px",
                                            },
                                        ),
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("OR No."),
                                        dbc.Input(id='followupnote_OR_no', type='text', placeholder="Enter OR Number")
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Bill"),
                                        dbc.Input(id='followupnote_bill', type='text', placeholder="Enter Bill")
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Clinical Exam"), width=3),
                                dbc.Col(dbc.Button("+", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='followupclinicalexam-addbutton', className='custom-button', n_clicks=0), width=2),
                                dbc.Col(dbc.Button("-", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='followupclinicalexam-deletebutton', className='custom-button', n_clicks=0), width=2),
                            ]),
                            html.Div(id='followupclinicalexam-lineitems'),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Laboratory Exam"), width=3),
                                dbc.Col(dbc.Button("+", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='followuplabexam-addbutton', className='custom-button', n_clicks=0), width=2),
                                dbc.Col(dbc.Button("-", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='followuplabexam-deletebutton', className='custom-button', n_clicks=0), width=2),
                            ]),
                            html.Div(id='followuplabexam-lineitems'),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Diagnosis & Prescription"), width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Diagnosis"),
                                        dbc.Textarea(id='followupproblem_diagnosis', placeholder='Enter Diagnosis', style={"height":100})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Prescription"),
                                        dbc.Textarea(id='followupproblem_prescription', placeholder="Enter Prescription", style={"height":100})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Patient instructions"),
                                        dbc.Textarea(id='followupproblem_clienteduc', placeholder="Enter instructions", style={"height":100})
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Problem Status"), width=3),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='followupproblem_status',
                                        options=[
                                            {'label':'Resolved', 'value':'resolved'},
                                            {'label':'Ongoing', 'value':'ongoing'},
                                            {'label':'Pending Diagnosis', 'value':'pending_diagnosis'},
                                            {'label':'For Follow-Up', 'value':'follow_up'},
                                            {'label':'Critical Condition', 'value':'critical_condition'},
                                            {'label':'For Surgery', 'value':'for_surgery'},
                                            {'label':'Post Surgery', 'value':'post_surgery'},
                                            {'label':'Under Observation', 'value':'under_observation'},
                                            {'label':'Deceased', 'value':'deceased'},
                                            {'label':'Unknown', 'value':'unknown'},
                                            {'label':'Waiting For Test Results', 'value':'pending_testresults'},
                                        ],
                                        placeholder='Select Problem Status',
                                    ),
                                    width = 9
                                )
                            ])
                        ]),
                    ],
                ),
            ])
        ]),
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



newclinicalexam_lineitem = []
newlabexam_lineitem = []

@app.callback( #callback for adding a row for clinical exam line items
    [
        Output("newclinicalexam-lineitems", "children"),
    ],
    [
        Input("newclinicalexam-addbutton", "n_clicks"),
        Input("newclinicalexam-deletebutton", "n_clicks"),
    ],
)
def manage_clinicalexam_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "newclinicalexam-addbutton" in triggered_id:
        if len(newclinicalexam_lineitem) < addclick:
            i = len(newclinicalexam_lineitem)
            newclinicalexam_lineitem.extend([
                html.Div([
                    html.Hr(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Clinician"),
                            dcc.Dropdown(
                                id={"type": "newclinicianlist", "index": i},
                                placeholder="Select Clinician",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ]),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Clinical Exam Type"),
                            dcc.Dropdown(
                                id={"type": "newclinicalexamlist", "index": i},
                                placeholder="Select Clinical Exam Type",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ]),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Clinical Findings"),
                            dbc.Textarea(
                                id={"type": "newclinicalfindings", "index": i},
                                placeholder="Enter Findings",
                                style={'width':'100%', 'height':100}
                            ),
                        ]),
                    ]),
                    html.Br(),
                ])
            ]) 

    elif triggered_id and "newclinicalexam-deletebutton" in triggered_id:
        if len(newclinicalexam_lineitem) > 0:
            newclinicalexam_lineitem.pop()

    else:
        raise PreventUpdate

    return [newclinicalexam_lineitem]


@app.callback( #callback for adding a row for lab exam line items
    [
        Output("newlabexam-lineitems", "children"),
    ],
    [
        Input("newlabexam-addbutton", "n_clicks"),
        Input("newlabexam-deletebutton", "n_clicks"),
    ],
)
def manage_labexam_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "newlabexam-addbutton" in triggered_id:
        if len(newlabexam_lineitem) < addclick:
            i = len(newlabexam_lineitem)
            newlabexam_lineitem.extend([
                html.Div([
                    html.Hr(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Veterinarian In Charge"),
                            dcc.Dropdown(
                                id={"type": "newvetexaminerlist", "index": i},
                                placeholder="Select Veterinary Examiner",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ]),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Laboratory Exam Type"),
                            dcc.Dropdown(
                                id={"type": "newlabexamlist", "index": i},
                                placeholder="Select Laboratory Exam Type",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ]),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Laboratory Exam Findings"),
                            dbc.Textarea(
                                id={"type": "newlabfindings", "index": i},
                                placeholder="Enter Findings",
                                style={'width':'100%', 'height':100}
                            ),
                        ]),
                    ]),
                    html.Br(),
                ])
            ]) 

    elif triggered_id and "newlabexam-deletebutton" in triggered_id:
        if len(newlabexam_lineitem) > 0:
            newlabexam_lineitem.pop()

    else:
        raise PreventUpdate

    return [newlabexam_lineitem]


@app.callback( #callback to provide the list of clinicians on the dropdown
    [
        Output({"type": "newclinicianlist", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "newclinicianlist", "index": MATCH}, "value"),
    ]
)
def new_loadclinicians(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
        sql = """ 
            SELECT 
                clinician_id,
                COALESCE(clinician_ln, '') || ', ' || COALESCE(clinician_fn, '') AS clinician_name
            FROM 
                clinician 
            WHERE 
                NOT clinician_delete_ind
            """
        values = []
        cols = ['clinician_id', 'clinician_name']
        if searchterm:
            sql += """ AND clinician_name ILIKE %s
            """
            values = [f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinician_name'], 'value': row['clinician_id']} for _, row in result.iterrows()]
    return options, 


@app.callback( #callback to provide the list of clinical exam in the dropdown
    [
        Output({"type": "newclinicalexamlist", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "newclinicalexamlist", "index": MATCH}, "value"),
    ]
)
def new_loadclinicalexam(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
        sql = """ 
            SELECT 
                clinical_exam_type_id,
                clinical_exam_type_m
            FROM 
                clinical_exam_type
            WHERE 
                NOT clinical_exam_type_delete_ind
            """
        values = []
        cols = ['clinical_exam_type_id', 'clinical_exam_type_m']
        if searchterm:
            sql += """ AND clinical_exam_type_m ILIKE %s
            """
            values = [f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinical_exam_type_m'], 'value': row['clinical_exam_type_id']} for _, row in result.iterrows()]
    return options, 


@app.callback( #callback to provide the list of veterinarians to be in charge for lab exam on the dropdown
    [
        Output({"type": "newvetexaminerlist", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "newvetexaminerlist", "index": MATCH}, "value"),
    ]
)
def newvisit_loadvetlabexam(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
        sql = """ 
            SELECT 
                vet_id,
                COALESCE(vet_ln, '') || ', ' || COALESCE(vet_fn, '') AS vet_name
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


@app.callback( #callback to provide the list of clinical exam in the dropdown
    [
        Output({"type": "newlabexamlist", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "newlabexamlist", "index": MATCH}, "value"),
    ]
)
def new_loadlabexam(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
        sql = """ 
            SELECT 
                lab_exam_type_id,
                lab_exam_type_m
            FROM 
                lab_exam_type
            WHERE 
                NOT lab_exam_type_delete_ind
            """
        values = []
        cols = ['lab_exam_type_id', 'lab_exam_type_m']
        if searchterm:
            sql += """ AND lab_exam_type_m ILIKE %s
            """
            values = [f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['lab_exam_type_m'], 'value': row['lab_exam_type_id']} for _, row in result.iterrows()]
    return options, 




followupclinicalexam_lineitem = []
followuplabexam_lineitem = []

@app.callback( #callback for adding a row for clinical exam line items
    [
        Output("followupclinicalexam-lineitems", "children"),
    ],
    [
        Input("followupclinicalexam-addbutton", "n_clicks"),
        Input("followupclinicalexam-deletebutton", "n_clicks"),
    ],
)
def manage_followupclinicalexam_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "followupclinicalexam-addbutton" in triggered_id:
        if len(followupclinicalexam_lineitem) < addclick:
            i = len(followupclinicalexam_lineitem)
            followupclinicalexam_lineitem.extend([
                html.Div([
                    html.Hr(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Clinician"),
                            dcc.Dropdown(
                                id={"type": "followupclinicianlist", "index": i},
                                placeholder="Select Clinician",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ]),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Clinical Exam Type"),
                            dcc.Dropdown(
                                id={"type": "followupclinicalexamlist", "index": i},
                                placeholder="Select Clinical Exam Type",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ]),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Clinical Findings"),
                            dbc.Textarea(
                                id={"type": "followupclinicalfindings", "index": i},
                                placeholder="Enter Findings",
                                style={'width':'100%', 'height':100}
                            ),
                        ]),
                    ]),
                    html.Br(),
                ])
            ]) 

    elif triggered_id and "followupclinicalexam-deletebutton" in triggered_id:
        if len(followupclinicalexam_lineitem) > 0:
            followupclinicalexam_lineitem.pop()

    else:
        raise PreventUpdate

    return [followupclinicalexam_lineitem]


@app.callback( #callback for adding a row for lab exam line items
    [
        Output("followuplabexam-lineitems", "children"),
    ],
    [
        Input("followuplabexam-addbutton", "n_clicks"),
        Input("followuplabexam-deletebutton", "n_clicks"),
    ],
)
def manage_followuplabexam_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "followuplabexam-addbutton" in triggered_id:
        if len(followuplabexam_lineitem) < addclick:
            i = len(followuplabexam_lineitem)
            followuplabexam_lineitem.extend([
                html.Div([
                    html.Hr(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Veterinarian In Charge"),
                            dcc.Dropdown(
                                id={"type": "followupvetexaminerlist", "index": i},
                                placeholder="Select Veterinary Examiner",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ]),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Laboratory Exam Type"),
                            dcc.Dropdown(
                                id={"type": "followuplabexamlist", "index": i},
                                placeholder="Select Laboratory Exam Type",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ]),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Laboratory Exam Findings"),
                            dbc.Textarea(
                                id={"type": "followuplabfindings", "index": i},
                                placeholder="Enter Findings",
                                style={'width':'100%', 'height':100}
                            ),
                        ]),
                    ]),
                    html.Br(),
                ])
            ]) 

    elif triggered_id and "followuplabexam-deletebutton" in triggered_id:
        if len(followuplabexam_lineitem) > 0:
            followuplabexam_lineitem.pop()

    else:
        raise PreventUpdate

    return [followuplabexam_lineitem]


@app.callback( #callback to provide the list of clinicians on the dropdown
    [
        Output({"type": "followupclinicianlist", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "followupclinicianlist", "index": MATCH}, "value"),
    ]
)
def followup_loadclinicians(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
        sql = """ 
            SELECT 
                clinician_id,
                COALESCE(clinician_ln, '') || ', ' || COALESCE(clinician_fn, '') AS clinician_name
            FROM 
                clinician 
            WHERE 
                NOT clinician_delete_ind
            """
        values = []
        cols = ['clinician_id', 'clinician_name']
        if searchterm:
            sql += """ AND clinician_name ILIKE %s
            """
            values = [f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinician_name'], 'value': row['clinician_id']} for _, row in result.iterrows()]
    return options, 


@app.callback( #callback to provide the list of clinical exam in the dropdown
    [
        Output({"type": "followupclinicalexamlist", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "followupclinicalexamlist", "index": MATCH}, "value"),
    ]
)
def followup_loadclinicalexam(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
        sql = """ 
            SELECT 
                clinical_exam_type_id,
                clinical_exam_type_m
            FROM 
                clinical_exam_type
            WHERE 
                NOT clinical_exam_type_delete_ind
            """
        values = []
        cols = ['clinical_exam_type_id', 'clinical_exam_type_m']
        if searchterm:
            sql += """ AND clinical_exam_type_m ILIKE %s
            """
            values = [f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinical_exam_type_m'], 'value': row['clinical_exam_type_id']} for _, row in result.iterrows()]
    return options, 


@app.callback( #callback to provide the list of veterinarians to be in charge for lab exam on the dropdown
    [
        Output({"type": "followupvetexaminerlist", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "followupvetexaminerlist", "index": MATCH}, "value"),
    ]
)
def followupvisit_loadvetlabexam(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
        sql = """ 
            SELECT 
                vet_id,
                COALESCE(vet_ln, '') || ', ' || COALESCE(vet_fn, '') AS vet_name
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


@app.callback( #callback to provide the list of clinical exam in the dropdown
    [
        Output({"type": "followuplabexamlist", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "followuplabexamlist", "index": MATCH}, "value"),
    ]
)
def followup_loadlabexam(pathname, searchterm):
    if pathname == "/newrecord/existingpatient" and not searchterm:
        sql = """ 
            SELECT 
                lab_exam_type_id,
                lab_exam_type_m
            FROM 
                lab_exam_type
            WHERE 
                NOT lab_exam_type_delete_ind
            """
        values = []
        cols = ['lab_exam_type_id', 'lab_exam_type_m']
        if searchterm:
            sql += """ AND lab_exam_type_m ILIKE %s
            """
            values = [f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['lab_exam_type_m'], 'value': row['lab_exam_type_id']} for _, row in result.iterrows()]
    return options, 


@app.callback( #callback to load problem list of selected patient
    [
        Output('followupproblem', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('followupproblem', 'value'),
        Input('patientlist_existingpatient', 'value'),
    ]
)
def newvisit_loadproblems(pathname, searchterm, selected_patient):
    if pathname == "/newrecord/existingpatient" and not searchterm:
        sql = """ 
            SELECT DISTINCT
                problem.problem_id,
                COALESCE(problem_no, '') || '.) ' || COALESCE(problem_chief_complaint, '') || ' - ' || COALESCE(problem_status_m, '') AS problem_name
            FROM 
                problem 
            INNER JOIN problem_status ON problem.problem_status_id = problem_status.problem_status_id
            INNER JOIN note ON problem.problem_id = note.problem_id
            INNER JOIN visit ON note.visit_id = visit.visit_id
            INNER JOIN patient ON visit.patient_id = patient.patient_id
            WHERE 
                NOT problem_delete_ind
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
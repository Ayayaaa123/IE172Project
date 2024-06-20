from dash import dcc #interpreter recommended to replace 'import dash_core_components as dcc' with 'from dash import dcc'
from dash import html #interpreter recommended to replace 'import dash_html_components as html' with 'from dash import html'
import dash_bootstrap_components as dbc
from dash import dash_table #interpreter recommended to replace 'import dash_table' with 'from dash import dash_table'
import dash
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_mantine_components as dmc
from app import app
from apps import dbconnect as db
from datetime import datetime
from dash import ALL, MATCH
from urllib.parse import urlparse, parse_qs
import json


layout = html.Div([
        #html.H1("reCreP"),
        dbc.Alert(id = 'visitrecord_alert_reCreP', is_open = False),
        html.Br(),
        dbc.Card( # Main Visits Info
            [
                dbc.CardHeader(
                    html.Div([
                            html.H2("Record Visits", className = "flex-grow-1"),
                            html.Div([
                                dbc.Button("Returning Patient", href= '/home_reCreP',className = "me-2",n_clicks = 0),
                                dbc.Button("New Patient", href= '/home_reCnewP',n_clicks = 0),
                            ], className = "ml-2 d-flex")
                        ], className = "d-flex align-items-center justify-content-between")
                ),

                dbc.CardBody([
                    dbc.Row([

                        dbc.Col(html.H4("Select Client"), width = 3),

                        dbc.Col(
                            dcc.Dropdown(
                                id = "re_clientlist_reCreP",
                                placeholder = "Search Client",
                                searchable = True,
                                options = [],
                                value = None,
                            ), width = 3),

                        dbc.Col(html.H4("Select Patient"), width = 3),
                        
                        dbc.Col(
                            dcc.Dropdown(
                                id = "patientlist_reCreP",
                                placeholder="Search Patient",
                                searchable=True,
                                options=[],
                                value=None,
                            ), width = 3), 

                    ], id = 'for_returning_patients'),
                    
                    html.Br(),

                    dbc.Row([ #Select Veterinarian
                            
                        dbc.Col(html.H4("Veterinarian Assigned"), width=3),

                        dbc.Col(
                            dcc.Dropdown(
                                id="vetlist_reCreP",
                                placeholder="Select Veterinarian",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ),
                    ]),

                    html.Br(),

                    dbc.Row([ #Visit Date
                        dbc.Col(html.H4("Visit Date"), width=3),
                        dbc.Col(
                            dmc.DatePicker(
                            id='visitdate_reCreP',
                            placeholder="Select Visit Date",
                            value=datetime.now().date(),
                            inputFormat='MMM DD, YYYY',
                            dropdownType='modal',
                            ),
                        ),    
                    ]),
                    
                    html.Br(),
                    
                    dbc.Row([
                        dbc.Col(html.H4("Visit Purpose"), width=3),
                        dbc.Col(
                            dbc.Checklist(
                            options=[
                                {"label": " New Problem", "style":{"flex-grow": 1}, "value": "new_problem"},
                                {"label": " Follow up to a Problem", "style":{"flex-grow": 1}, "value": "follow_up"},
                                {"label": " Vaccination", "style":{"flex-grow": 1}, "value": "vaccination"},
                                {"label": " Deworming", "style":{"flex-grow": 1}, "value": "deworming"},
                            ],
                            id="visitpurpose_reCreP",
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
        html.Div(id="visitinputs_reCreP"),
        html.Br(),
        dbc.Button(
                    'Submit',
                    id = 'visitrecord_submit_reCreP',
                    n_clicks = 0, #initialization 
                    className='custom-submitbutton',
                ),
        dbc.Modal([
            dbc.ModalHeader(html.H4('Visit Recorded Successfully!')),
        ],
        centered = True, id = 'visitrecord_successmodal_reCreP',
        backdrop = 'static'
        ),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Administered Vaccine Details")),
            dbc.ModalBody([
                dbc.Alert(id = 'vaccinevisitrecord_alert_reCreP', is_open = False),
                dbc.Row([
                    dbc.Col(html.H5("Vaccine Name"), width =6),
                    dbc.Col(html.H5("Vaccine Dose"), width =3),
                    dbc.Col(html.H5("From VetMed?"), width =3),
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(
                            id="vaccine_name_reCreP",
                            placeholder='Select Vaccine',
                            searchable=True,
                            options=[],
                            value=None,
                        )],
                        width = 6,
                    ),
                    dbc.Col([
                        dbc.Col(
                            dcc.Dropdown(
                                id="vaccine_dose_reCreP",
                                options=[
                                    {'label':'1st', 'value':'1st'},
                                    {'label':'2nd', 'value':'2nd'},
                                    {'label':'3rd', 'value':'3rd'},
                                    {'label':'4th', 'value':'4th'},
                                    {'label':'Booster', 'value':'Booster'},
                                ],
                                placeholder='Enter Dose',
                            ),
                        )], 
                        width = 3,
                    ),
                    dbc.Col([
                        dbc.RadioItems(
                            options=[
                                {"label": "Yes", "value": "true"},
                                {"label": " No", "value": "false"},
                            ],
                            id="vacc_from_vetmed",
                            inline=False,
                            style={
                                "display": "flex",
                                "justify-content": "between",
                                "gap": "15px",
                            },
                        )],
                        width=3,
                    ),
                ]),
                html.Br(),
                dbc.Row([  
                    dbc.Col(html.H5("Date Administered"), width =3),
                    dbc.Col([
                        dcc.DatePickerSingle(
                            id="vaccine_admin_reCreP",
                            date = None,
                            placeholder="Select Date",
                            display_format='MMM DD, YYYY',
                        )],
                        width = 3,
                    ),  
                    dbc.Col(html.H5("Vaccine Expiration"), width =3),
                    dbc.Col([
                        dcc.DatePickerSingle(
                            id="vaccine_exp_reCreP",
                            date = None,
                            placeholder="Select Date",
                            display_format='MMM DD, YYYY',
                        )],
                        width = 3,
                    ),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Details", id="vaccine_submit_btn", className="ms-auto", n_clicks=0),
                #dbc.Button("Close", id="close-modal-btn", className="ml-auto", n_clicks=0),
            ]),
        ], centered = True, id="vaccine_modal", is_open=False, backdrop = "static", size = "lg"),
    ])


# MODAL CALLBACKS

@app.callback( #opens modal form for vaccine
    Output("vaccine_modal", "is_open"),
    Input("add_vaccine_form_btn", "n_clicks"),
    State("vaccine_modal", "is_open"),
)
def toggle_modal(add, is_open):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "add_vaccine_form_btn" and add:
            return not is_open
        return is_open


# SUBMISSION AND EDIT CALLBACKS
@app.callback( # Submit Button for visit
    [
        Output('visitrecord_alert_reCreP','color'),
        Output('visitrecord_alert_reCreP','children'),
        Output('visitrecord_alert_reCreP','is_open'),
        Output('visitrecord_successmodal_reCreP','is_open'),
    ],
    [
        Input('visitrecord_submit_reCreP','n_clicks'),
        Input('re_clientlist_reCreP', 'value'),
        Input('patientlist_reCreP','value'),
        Input('vetlist_reCreP','value'),
        Input('visitdate_reCreP', 'value')
    ],
    [
        State("visitpurpose_reCreP", "value"),
    ]
)
def visitrecord_save(submitbtn, client, patient, vet, date, selected_services):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        alert_open = False
        modal_open = False
        alert_color = ''
        alert_text = ''
        
        if eventid == 'visitrecord_submit_reCreP' and submitbtn:
            
            visit_for_vacc = 'vaccination' in selected_services
            visit_for_deworm = 'deworming' in selected_services
            visit_for_problem = any(service in selected_services for service in ['new_problem', 'follow_up'])

            if not client:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please choose a client'
            elif not patient:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please choose a patient'
            elif not vet:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please choose the Veterinarian assigned'
            elif not date:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please select the date of visit'
            elif not selected_services:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please select purpose of visit'
            else:
                sql = '''
                INSERT INTO visit(
                                patient_id,
                                vet_id,
                                visit_for_vacc,
                                visit_for_deworm,
                                visit_for_problem,
                                visit_delete_ind
                            )
                            VALUES(%s, %s, %s, %s, %s, %s)
                    '''
                values = [patient, vet, visit_for_vacc, visit_for_deworm, visit_for_problem, False]

                db.modifydatabase(sql, values)

                modal_open = True
            
            return [alert_color, alert_text, alert_open, modal_open]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback( # Submit button for vaccine details
    [
        Output('vaccinevisitrecord_alert_reCreP','color'),
        Output('vaccinevisitrecord_alert_reCreP','children'),
        Output('vaccinevisitrecord_alert_reCreP','is_open'),
    ],
    [
        Input('vaccine_submit_btn', 'n_clicks'),
        Input('vaccine_name_reCreP', 'value'),
        Input('vaccine_dose_reCreP', 'value'),
        Input('vaccine_admin_reCreP', 'date'),
        Input('vaccine_exp_reCreP', 'date'),
        Input('vacc_from_vetmed', 'value'),
    ]
)
def vaccinevisitrecord_save(submitbtn, name, dose, admin, exp, from_vetmed):
    
    sql = """
        SELECT MAX(visit_id) + 1
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])
    
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        alert_open = False
        modal_open = False
        alert_color = ''
        alert_text = ''

        if eventid == 'vaccine_submit_btn' and submitbtn:

            if not name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please choose the name of administered vaccine'
            elif not dose:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please choose the dose of administered vaccine'
            elif not admin:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please fill the date the vaccine was administered'
            elif not exp:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please fill the expiration date of administered vaccine'
            elif not from_vetmed:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please answer if the administered vaccine was from VetMed or not'
            else:
                sql = '''
                INSERT INTO vacc(
                                vacc_m_id,
                                vacc_dose,
                                vacc_date_administered,
                                vacc_exp,
                                vacc_from_vetmed,
                                vacc_delete_ind,
                                visit_id
                            )
                            VALUES(%s, %s, %s, %s, %s, %s, %s)
                    '''
                values = [name, dose, admin, exp, from_vetmed, False, visit_id]

                db.modifydatabase(sql,values)

            return[alert_color, alert_text, alert_open]
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate



#LAYOUT CALLBACKS

@app.callback( #callback to add inputs depending on the selected visit purpose
    Output("visitinputs_reCreP", "children"),
    Input("visitpurpose_reCreP", "value"),
    State("visitpurpose_reCreP", "value"),
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
                            html.Div([
                                html.H2("Vaccination", className = 'flex-grow-1'),
                                html.Div(dbc.Button("Add Administered Vaccine Medication", id = "add_vaccine_form_btn"), className = "ml-2 d-flex"),
                            ], className = "d-flex align-items-center justify-content-between")
                        ),
                        dbc.CardBody([
                            html.Div(id = "visit_vaccine_list")
                        ]),
                    ], 
                ),
            ]),
        ]),
    if 'deworming' in selected_services:
        inputs.extend([
            html.Div([
                html.Br(),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Row([
                            dbc.Col(html.H2("Deworming"), width="auto"),
                            dbc.Col(
                                [
                                    dbc.Button("+", id='deworm-addbutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                    dbc.Button("-", id='deworm-deletebutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                ],
                                width="auto", 
                                className="text-right"
                            ),
                        ], justify= "between"),
                    ),
                    dbc.CardBody([
                        html.Div([
                            html.Div(style={'height':'5px'}),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Deworming Medication"),
                                    dcc.Dropdown(
                                        id="deworm_name_reCreP",
                                        placeholder='Select Deworming Medication',
                                        searchable=True,
                                        options=[],
                                        value=None,
                                    )],
                                    width = 4,
                                ),
                                dbc.Col([
                                    dbc.Label("Deworming Dosage"),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="deworm_dose_reCreP",
                                            options=[
                                                {'label':'1st', 'value':'resolved'},
                                                {'label':'2nd', 'value':'ongoing'},
                                                {'label':'3rd', 'value':'pending_diagnosis'},
                                                {'label':'4th', 'value':'follow_up'},
                                                {'label':'Booster', 'value':'critical_condition'},
                                            ],
                                            placeholder='Enter Dose',
                                        ),
                                    ),
                                ], width = 2,),   
                                dbc.Col([
                                    dbc.Label("Date Administered"),
                                    dmc.DatePicker(
                                        id={"type": "deworming_date_reCreP", "index": 1},
                                        placeholder="Select Date Administered",
                                        inputFormat='MMM DD, YYYY',
                                        dropdownType='modal',
                                    )],
                                    width = 3,
                                ),
                                dbc.Col([
                                    dbc.Label("Medication Expiration"),
                                    dmc.DatePicker(
                                        id={"type": "deworming_medication_expdate_reCreP", "index": 1},
                                        placeholder="Select Expiration Date",
                                        inputFormat='MMM DD, YYYY',
                                        dropdownType='modal',
                                    )],
                                    width = 3,
                                ),
                            ]),
                            html.Div(style={'height':'5px'}),        
                        ]),
                        html.Div(id='deworm-line-items_reCreP'),
                    ]),
                ]), 
            ])
        ]),
    if 'new_problem' in selected_services:
        inputs.extend([
            html.Div([
                html.Br(),
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([                                
                            html.H2("New Problem", className = 'flex-grow-1'),

                            html.Div([
                                html.Div("Problem Status", className = 'me-2', style = {'white-space': 'nowrap','flex': '0 0 auto'}),
                                dcc.Dropdown(
                                    id = "newproblem_status_reCreP",
                                    placeholder = "Select Problem Status",
                                    searchable = True,
                                    options = [],
                                    value = None,
                                    style = {'flex': '1'},
                                ),
                            ], className = "d-flex align-items-center", style = {'flex-grow': '1'}),
                        ], className = "d-flex align-items-center justify-content-between")
                    ),
                    dbc.CardBody([

                        dbc.Row( #Problem
                            [
                                dbc.Col(html.H3("Problem"), width=2),
                                dbc.Col(dbc.Input(id="newproblem_reCreP", type='text', placeholder='Enter Problem')),
                            ],
                        ),
                        html.Br(),

                        dbc.Row(dbc.Col(html.H3("Health & Nutrients Intake"))),

                        dbc.Row([ # Under health and nutrients
                            dbc.Col(
                                [
                                    dbc.Label("Relevant Medical History"),
                                    dbc.Textarea(id='newproblem_reCreP_medhistory', placeholder='Enter Any Relevant Medical History', style={"height":75})
                                ],
                                width=6
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Diet"),
                                    dbc.Textarea(id='newproblem_reCreP_diet', placeholder="Enter Patient's Diet", style={"height":75})
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Water Source"),
                                    dbc.Textarea(id='newproblem_reCreP_water', placeholder="Enter Patient's Water Source", style={"height":75})
                                ],
                                width=3
                            ),
                        ]),
                        html.Br(),

                        dbc.Row(dbc.Col(html.H3("Health Assessment"))),
                        
                        dbc.Row([ # Under health assessment
                            dbc.Col(
                                [
                                    dbc.Label("Temperature"),
                                    dbc.Input(id='newproblem_reCreP_temp', type='text', placeholder='Enter Temperature')
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Pulse Rate"),
                                    dbc.Input(id='newproblem_reCreP_pr', type='text', placeholder="Enter Pulse Rate")
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Weight"),
                                    dbc.Input(id='newproblem_reCreP_weight', type='text', placeholder='Enter Weight')
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Respiration Rate"),
                                    dbc.Input(id='newproblem_reCreP_rr', type='text', placeholder="Enter Respiration Rate")
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Body Condition Score"),
                                    dbc.Input(id='newproblem_reCreP_bodyconditionscore', type='text', placeholder="Enter Body Condition Score")
                                ],
                                width=3
                            ),
                        ]),
                        html.Br(),
                        html.Br(),

                        html.Hr(), #line

                        dbc.Row([ # Clinical Exam Add/Delete button
                            dbc.Col(html.H3("Clinical Exam"), width=3),
                            dbc.Col(
                                [
                                    dbc.Button("+", id='newproblem_clinicalexam-addbutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                    dbc.Button("-", id='newproblem_clinicalexam-deletebutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                ],
                                width = 'auto',
                                className = 'text-right'
                            ),
                        ], justify = 'between'),

                        html.Hr(), #line

                        dbc.Container([ #Clinical Exam Content
                            html.Div(
                                [
                                    dbc.Row([ # Clinical Exam 1st Clinician and Exam

                                        dbc.Col(
                                            [
                                                dbc.Label("Clinical Exam Type"),
                                                dcc.Dropdown(
                                                    id= "newproblem_clinical_exam_list_reCreP",
                                                    placeholder="Select Clinical Exam Type",
                                                    searchable=True,
                                                    options=[],
                                                    value=None,
                                                ), 
                                            ],    
                                            width = 3
                                        ), 

                                        dbc.Col(
                                            [
                                                dbc.Label("Clinical Exam Findings"),
                                                dbc.Textarea(
                                                    id="newproblem_clinicalfindings_reCreP",
                                                    placeholder="Enter Findings",
                                                    style={'width':'100%', 'height':25}
                                                ),
                                            ],
                                            width = 6
                                        ), 
                                        
                                        dbc.Col(
                                            [
                                                dbc.Label("Clinician"),
                                                dcc.Dropdown(
                                                    id="newproblem_clinician_list_reCreP",
                                                    placeholder="Select Clinician",
                                                    searchable=True,
                                                    options=[],
                                                    value=None,
                                                ), 
                                            ],
                                            width = 3
                                        ),
                                    ]),
                                    
                                    html.Br(),
                                ],
                            ),
                            html.Div(id = "newproblem_clinical_exam_content_reCreP")
                        ]),
                        html.Br(),
                        
                        html.Hr(), #line
                        
                        dbc.Row(html.H3("Progress Notes")),

                        html.Hr(), #line

                        dbc.Container([ # Progress Notes Content
                            html.Div([
                                html.Div(
                                    dbc.Row([ # Laboratory Result Add/Delete button
                                        dbc.Col(html.H5("Add Laboratory Results:"), width=6),
                                        dbc.Col(
                                            [
                                                dbc.Button("+", id='newproblem_labresult-addbutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                                dbc.Button("-", id='newproblem_labresult-deletebutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                            ],
                                            width = 'auto',
                                            className = 'text-right'
                                        ),
                                    ], justify = 'between'),
                                ),
                                html.Div(id='newproblem_labresult_lineitems_reCreP'),

                                html.Br(),

                                dbc.Row([ #under progress notes
                                    dbc.Col([
                                        dbc.Label("Differential Diagnosis"),
                                        dbc.Textarea(
                                            id="newproblem_differentialdiagnosis_reCreP",
                                            placeholder="Enter Differential Diagnosis",
                                            style={'width':'100%', 'height':100}
                                        ),
                                    ]),
                                    dbc.Col([
                                        dbc.Label("Possible Treatment"),
                                        dbc.Textarea(
                                            id="newproblem_possibletreatment_reCreP",
                                            placeholder="Enter Treatment Options",
                                            style={'width':'100%', 'height':100}
                                        ),
                                    ]),
                                    dbc.Col([
                                        dbc.Row([
                                            dbc.Label("OR Number"),
                                            dbc.Textarea(
                                            id="newproblem_ornumber_reCreP",
                                            placeholder="Enter OR No.",
                                            style={'width':'100%', 'height':25}
                                            ),
                                        ]),
                                        dbc.Row([
                                            dbc.Label("Bill"),
                                            dbc.Textarea(
                                            id="newproblem_bill_reCreP",
                                            placeholder="Enter Bill Amount",
                                            style={'width':'100%', 'height':25}
                                            ),
                                        ]),
                                    ], width=3)
                                ]),

                                html.Br(),

                                html.Div( # Request Laboratory Examination
                                    dbc.Row([ 
                                    dbc.Col(html.H5("Request Laboratory Examination:"), width=6),
                                    dbc.Col(
                                        [
                                            dbc.Button("+", id='newproblem_labreq-addbutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                            dbc.Button("-", id='newproblem_labreq-deletebutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                        ],
                                        width = 'auto',
                                        className = 'text-right'
                                    ),
                                ], justify = 'between'),),
                                html.Div(id='newproblem_labreq_lineitems_reCreP'),
                                html.Br(),
                            ]), 
                        ]),
                        html.Br(),
                        
                        html.Hr(), #line                            

                        dbc.Row(dbc.Col(html.H4("Diagnosis and Treatment"))),
                        dbc.Row([ # Under Diagnosis
                            dbc.Col(
                                [
                                    dbc.Label("Diagnosis"),
                                    dbc.Textarea(id='newproblem_reCreP_diagnosis', placeholder='Enter Diagnosis', style={"height":50})
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Prescription"),
                                    dbc.Textarea(id='newproblem_reCreP_prescription', placeholder="Enter Prescription", style={"height":50})
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Patient instructions"),
                                    dbc.Textarea(id='newproblem_reCreP_clienteduc', placeholder="Enter instructions", style={"height":50})
                                ],
                                width=4
                            ),
                        ]),
                    ]),
                ])
            ])
        ]),
    if 'follow_up' in selected_services:
        inputs.extend([
            html.Div([
                html.Br(),
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([                                
                            html.H2("Problem Follow-up", className = 'flex-grow-1'),

                            html.Div([
                                html.Div("Problem Status", className = 'me-2', style = {'white-space': 'nowrap','flex': '0 0 auto'}),
                                dcc.Dropdown(
                                    id = "followproblem_status_reCreP",
                                    placeholder = "Select Problem Status",
                                    searchable = True,
                                    options = [],
                                    value = None,
                                    style = {'flex': '1'},
                                ),
                            ], className = "d-flex align-items-center", style = {'flex-grow': '1'}),
                        ], className = "d-flex align-items-center justify-content-between")
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.H3("Problem"), width=2),
                            dbc.Col(
                                dcc.Dropdown(
                                    id="problem_list_reCreP",
                                    placeholder="Select Problem",
                                    searchable=True,
                                    options=[],
                                    value=None,
                                ),
                            ),
                        ]),
                        html.Br(),
                        dbc.Row(dbc.Col(html.H3("Health & Nutrients Intake"))),

                        dbc.Row([ # Under health and nutrients
                            dbc.Col(
                                [
                                    dbc.Label("Relevant Medical History"),
                                    dbc.Textarea(id='followproblem_reCreP_medhistory', placeholder='Enter Any Relevant Medical History', style={"height":75})
                                ],
                                width=6
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Diet"),
                                    dbc.Textarea(id='followproblem_reCreP_diet', placeholder="Enter Patient's Diet", style={"height":75})
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Water Source"),
                                    dbc.Textarea(id='followproblem_reCreP_water', placeholder="Enter Patient's Water Source", style={"height":75})
                                ],
                                width=3
                            ),
                        ]),
                        html.Br(),

                        dbc.Row(dbc.Col(html.H3("Health Assessment"))),
                        
                        dbc.Row([ # Under health assessment
                            dbc.Col(
                                [
                                    dbc.Label("Temperature"),
                                    dbc.Input(id='followproblem_reCreP_temp', type='text', placeholder='Enter Temperature')
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Pulse Rate"),
                                    dbc.Input(id='followproblem_reCreP_pr', type='text', placeholder="Enter Pulse Rate")
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Weight"),
                                    dbc.Input(id='followproblem_reCreP_weight', type='text', placeholder='Enter Weight')
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Respiration Rate"),
                                    dbc.Input(id='followproblem_reCreP_rr', type='text', placeholder="Enter Respiration Rate")
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Body Condition Score"),
                                    dbc.Input(id='followproblem_reCreP_bodyconditionscore', type='text', placeholder="Enter Body Condition Score")
                                ],
                                width=3
                            ),
                        ]),
                        html.Br(),
                        html.Br(),

                        html.Hr(), #line

                        dbc.Row([ # Clinical Exam Add/Delete button
                            dbc.Col(html.H3("Clinical Exam"), width=3),
                            dbc.Col(
                                [
                                    dbc.Button("+", id='followproblem_clinicalexam-addbutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                    dbc.Button("-", id='followproblem_clinicalexam-deletebutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                ],
                                width = 'auto',
                                className = 'text-right'
                            ),
                        ], justify = 'between'),

                        html.Hr(), #line

                        dbc.Container([ #Clinical Exam Content
                            html.Div(
                                [
                                    dbc.Row([ # Clinical Exam 1st Clinician and Exam

                                        dbc.Col(
                                            [
                                                dbc.Label("Clinical Exam Type"),
                                                dcc.Dropdown(
                                                    id="followproblem_clinical_exam_list_reCreP",
                                                    placeholder="Select Clinical Exam Type",
                                                    searchable=True,
                                                    options=[],
                                                    value=None,
                                                ), 
                                            ],    
                                            width = 3
                                        ), 

                                        dbc.Col(
                                            [
                                                dbc.Label("Clinical Exam Findings"),
                                                dbc.Textarea(
                                                    id="followproblem_newclinicalfindings_reCreP",
                                                    placeholder="Enter Findings",
                                                    style={'width':'100%', 'height':25}
                                                ),
                                            ],
                                            width = 6
                                        ), 
                                        
                                        dbc.Col(
                                            [
                                                dbc.Label("Clinician"),
                                                dcc.Dropdown(
                                                    id = "followproblem_clinician_list_reCreP",
                                                    placeholder="Select Clinician",
                                                    searchable=True,
                                                    options=[],
                                                    value=None,
                                                ), 
                                            ],
                                            width = 3
                                        ),
                                    ]),
                                    
                                    html.Br(),
                                ],
                            ),
                            html.Div(id = "followproblem_clinical_exam_content_reCreP")
                        ]),
                        html.Br(),
                        
                        html.Hr(), #line
                        
                        dbc.Row(html.H3("Progress Notes")),

                        html.Hr(), #line

                        dbc.Container([ # Progress Notes Content
                            html.Div([
                                html.Div(
                                    dbc.Row([ # Laboratory Result Add/Delete button
                                        dbc.Col(html.H5("Add Laboratory Results:"), width=6),
                                        dbc.Col(
                                            [
                                                dbc.Button("+", id='followproblem_labresult-addbutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                                dbc.Button("-", id='followproblem_labresult-deletebutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                            ],
                                            width = 'auto',
                                            className = 'text-right'
                                        ),
                                    ], justify = 'between'),
                                ),
                                html.Div(id='followproblem_labresult_lineitems_reCreP'),

                                html.Br(),

                                dbc.Row([ #under progress notes
                                    dbc.Col([
                                        dbc.Label("Differential Diagnosis"),
                                        dbc.Textarea(
                                            id="followproblem_differentialdiagnosis_reCreP",
                                            placeholder="Enter Differential Diagnosis",
                                            style={'width':'100%', 'height':100}
                                        ),
                                    ]),
                                    dbc.Col([
                                        dbc.Label("Possible Treatment"),
                                        dbc.Textarea(
                                            id="followproblem_possibletreatment_reCreP",
                                            placeholder="Enter Treatment Options",
                                            style={'width':'100%', 'height':100}
                                        ),
                                    ]),
                                    dbc.Col([
                                        dbc.Row([
                                            dbc.Label("OR Number"),
                                            dbc.Textarea(
                                            id="followproblem_ornumber_reCreP",
                                            placeholder="Enter OR No.",
                                            style={'width':'100%', 'height':25}
                                            ),
                                        ]),
                                        dbc.Row([
                                            dbc.Label("Bill"),
                                            dbc.Textarea(
                                            id="followproblem_bill_reCreP",
                                            placeholder="Enter Bill Amount",
                                            style={'width':'100%', 'height':25}
                                            ),
                                        ]),
                                    ], width=3)
                                ]),

                                html.Br(),

                                html.Div( # Request Laboratory Examination
                                    dbc.Row([ 
                                    dbc.Col(html.H5("Request Laboratory Examination:"), width=6),
                                    dbc.Col(
                                        [
                                            dbc.Button("+", id='followproblem_labreq-addbutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                            dbc.Button("-", id='followproblem_labreq-deletebutton_reCreP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                        ],
                                        width = 'auto',
                                        className = 'text-right'
                                    ),
                                ], justify = 'between'),),
                                html.Div(id='followproblem_labreq_lineitems_reCreP'),
                                html.Br(),
                            ]), 
                        ]),
                        html.Br(),
                        
                        html.Hr(), #line                            

                        dbc.Row(dbc.Col(html.H4("Diagnosis and Treatment"))),
                        dbc.Row([ # Under Diagnosis
                            dbc.Col(
                                [
                                    dbc.Label("Diagnosis"),
                                    dbc.Textarea(id='followproblem_reCreP_diagnosis', placeholder='Enter Diagnosis', style={"height":50})
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Prescription"),
                                    dbc.Textarea(id='followproblem_reCreP_prescription', placeholder="Enter Prescription", style={"height":50})
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Patient instructions"),
                                    dbc.Textarea(id='followproblem_reCreP_clienteduc', placeholder="Enter instructions", style={"height":50})
                                ],
                                width=4
                            ),
                        ]),
                    ]),
                        ])
            ])
        ]),
    return inputs

@app.callback( # to make the new and follow up problem options mutually exclusive
    Output('visitpurpose_reCreP','value'),
    [
        Input('visitpurpose_reCreP','value'),
        Input('vaccine_submit_btn', 'n_clicks'),
    ],
    State('visitpurpose_reCreP', 'value')
)
def update_checklist(selected_options, submit, current_value):
    if selected_options is None:
        return []
    
    last_option = selected_options[-1] if selected_options else None
    
    if last_option in ['new_problem', 'follow_up']:
        mutually_exclusive_option = 'follow_up' if last_option == 'new_problem' else 'new_problem'
        if mutually_exclusive_option in selected_options:
            selected_options.remove(mutually_exclusive_option)

    return selected_options

@app.callback(
        [
            Output("visit_vaccine_list", "children"),
        ],
        [
            Input("url", "pathname"),
        ]
)
def visit_vaccine_list(pathname):

    sql = """
        SELECT MAX(visit_id) + 1
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])

    try:  
        if pathname == "/home_reCreP":

            sql = """
                SELECT
                    vacc_m,
                    vacc_dose,
                    vacc_date_administered,
                    vacc_exp,
                    vacc_from_vetmed,
                    v.vacc_id
                FROM vacc v 
                    INNER JOIN vacc_m m on v.vacc_m_id = m.vacc_m_id
                WHERE NOT vacc_delete_ind
                    AND visit_id = %s
            """
            values = [visit_id]
            cols = ["Vaccine Name", "Vaccine Dose", "Date Administered", "Expiration Date", "Vaccine from VetMed?", "ID"]

            df = db.querydatafromdatabase(sql, values, cols)

            if not df.empty:

                buttons = []
                for vacc_id in df["ID"]:
                    buttons += [
                        html.Div(
                            dbc.Button("Edit", size = 'sm', color = 'success'),
                            style = {'text-align': 'center'}
                        )
                    ]
                df['Action'] = buttons
                df = df[["Vaccine Name", "Vaccine Dose", "Date Administered", "Expiration Date", "Vaccine from VetMed?", "Action"]]
                df["Vaccine from VetMed?"] = df["Vaccine from VetMed?"].apply(lambda x: 'Yes' if x else 'No')


                table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align': 'center'})
                return [table]
            else:
                empty_df = pd.DataFrame(columns=["Vaccine Name", "Vaccine Dose", "Date Administered", "Expiration Date", "Vaccine from VetMed?", "Action"])
                table = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'}, header=True, index=False)
                return [table]
        else:
            return [html.Div()]
    except Exception as e:
        print(f"An error occurred: {e}")
        return [html.Div()]


@app.callback( #callback for adding clinical exam content
    [
        Output('newproblem_clinical_exam_content_reCreP', 'children'),
    ],
    [
        Input('newproblem_clinicalexam-addbutton_reCreP', 'n_clicks'),
        Input('newproblem_clinicalexam-deletebutton_reCreP', 'n_clicks'),
    ],
)
def manage_clinical_exam_content_reCreP(addclick, deleteclick):
    ctx = dash.callback_context
 
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    newproblem_clinical_exam_lineitem = []
    
    if triggered_id and 'newproblem_clinicalexam-addbutton_reCreP' in triggered_id:
        if len(newproblem_clinical_exam_lineitem) < addclick:
            i = len(newproblem_clinical_exam_lineitem)
            newproblem_clinical_exam_lineitem.extend([
                html.Div(
                    [
                        dbc.Row([ # Clinical Exam 1st Clinician and Exam

                            dbc.Col([
                                    dbc.Label("Clinical Exam Type"),
                                    dcc.Dropdown(
                                        id={"type": "newproblem_clinical_exam_list_reCreP", "index": i},
                                        placeholder="Select Clinical Exam Type",
                                        searchable=True,
                                        options=[],
                                        value=None,
                                    ), 
                            ], width = 3), 

                            dbc.Col([
                                    dbc.Label("Clinical Exam Findings"),
                                    dbc.Textarea(
                                        id={"type": "newproblem_newclinicalfindings_reCreP", "index": i},
                                        placeholder="Enter Findings",
                                        style={'width':'100%', 'height':25}
                                    ),
                            ],width = 6), 
                            
                            dbc.Col([
                                    dbc.Label("Clinician"),
                                    dcc.Dropdown(
                                        id={"type": "newproblem_clinician_list_reCreP", "index": i},
                                        placeholder="Select Clinician",
                                        searchable=True,
                                        options=[],
                                        value=None,
                                    ), 
                             ],width = 3),
                        ]),
                        
                        html.Br(),
                    ],
                ),
            ])

    elif triggered_id and 'newproblem_clinicalexam-deletebutton_reCreP' in triggered_id:
        if len(newproblem_clinical_exam_lineitem) > 0:
            newproblem_clinical_exam_lineitem.pop()

    else:
        raise PreventUpdate
    
    return [newproblem_clinical_exam_lineitem]

@app.callback( #callback for adding clinical exam content
    [
        Output('followproblem_clinical_exam_content_reCreP', 'children'),
    ],
    [
        Input('followproblem_clinicalexam-addbutton_reCreP', 'n_clicks'),
        Input('followproblem_clinicalexam-deletebutton_reCreP', 'n_clicks'),
    ],
)
def manage_clinical_exam_content_reCreP(addclick, deleteclick):
    ctx = dash.callback_context
 
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    followproblem_clinical_exam_lineitem = []

    if triggered_id and 'followproblem_clinicalexam-addbutton_reCreP' in triggered_id:
        if len(followproblem_clinical_exam_lineitem) < addclick:
            i = len(followproblem_clinical_exam_lineitem)
            followproblem_clinical_exam_lineitem.extend([
                html.Div(
                    [
                        dbc.Row([ # Clinical Exam 1st Clinician and Exam

                            dbc.Col([
                                    dbc.Label("Clinical Exam Type"),
                                    dcc.Dropdown(
                                        id={"type": "followproblem_clinical_exam_list_reCreP", "index": i},
                                        placeholder="Select Clinical Exam Type",
                                        searchable=True,
                                        options=[],
                                        value=None,
                                    ), 
                            ], width = 3), 

                            dbc.Col([
                                    dbc.Label("Clinical Exam Findings"),
                                    dbc.Textarea(
                                        id={"type": "followproblem_newclinicalfindings_reCreP", "index": i},
                                        placeholder="Enter Findings",
                                        style={'width':'100%', 'height':25}
                                    ),
                            ],width = 6), 
                            
                            dbc.Col([
                                    dbc.Label("Clinician"),
                                    dcc.Dropdown(
                                        id={"type": "followproblem_clinician_list_reCreP", "index": i},
                                        placeholder="Select Clinician",
                                        searchable=True,
                                        options=[],
                                        value=None,
                                    ), 
                             ],width = 3),
                        ]),
                        
                        html.Br(),
                    ],
                ),
            ])

    elif triggered_id and 'followproblem_clinicalexam-deletebutton_reCreP' in triggered_id:
        if len(followproblem_clinical_exam_lineitem) > 0:
            followproblem_clinical_exam_lineitem.pop()

    else:
        raise PreventUpdate
    
    return [followproblem_clinical_exam_lineitem]

@app.callback( #callback for adding lab result content
    [
        Output('newproblem_labresult_lineitems_reCreP', 'children'),
    ],
    [
        Input('newproblem_labresult-addbutton_reCreP', 'n_clicks'),
        Input('newproblem_labresult-deletebutton_reCreP', 'n_clicks'),
    ],
    [
        State('newproblem_labresult_lineitems_reCreP', 'children'),
    ],
)
def newproblem_manage_labresult_content(addclick, deleteclick, existing_items):
    
    newproblem_lab_result_lineitem = existing_items or []
    
    ctx = dash.callback_context
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id and 'labresult-addbutton_reCreP' in triggered_id:
        if len(newproblem_lab_result_lineitem) < addclick:
            i = len(newproblem_lab_result_lineitem)
            newproblem_lab_result_lineitem.extend([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Lab Exam Type"),
                            dcc.Dropdown(
                            id={"type": "lab_exam_list_reCreP", "index": i},
                            placeholder="Select Laboratory Exam Type",
                            searchable=True,
                            options=[],
                            value=None,
                            ),
                        ], width = 5),
                        dbc.Col([
                                dbc.Label("Test from VetMed ?"),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Yes", "value": "true"},
                                        {"label": " No", "value": "false"},
                                    ],
                                    id="newnote_havebeentested_reCreP",
                                    inline=False,
                                    style={
                                        "display": "flex",
                                        "justify-content": "between",
                                        "gap": "15px",
                                    },
                                ),
                        ],width=2),
                        dbc.Col([
                            dbc.Label("Veterinarian In Charge"),
                            dcc.Dropdown(
                                id={"type": "veterinarian_list_reCreP", "index": i},
                                placeholder="Select Veterinary Examiner",
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                        ], width = 5),
                    ]),
                    dbc.Row([
                        dbc.Col(
                            [
                                dbc.Label("Laboratory Exam Findings"),
                                dbc.Textarea(
                                    id="newproblem_Labexamfindings_reCreP",
                                    placeholder="Enter Findings",
                                    style={'width':'100%', 'height':25}
                                ),
                            ],
                            width = 12
                        ), 
                    ]),
                    html.Br(),
                ])
            ])
    elif triggered_id and 'newproblem_labresult-deletebutton_reCreP' in triggered_id:
        if len(newproblem_lab_result_lineitem) > 0:
            newproblem_lab_result_lineitem.pop()
    else:
        raise PreventUpdate
    return [newproblem_lab_result_lineitem]

@app.callback( #callback for adding lab request content
    [
        Output('newproblem_labreq_lineitems_reCreP', 'children'),
    ],
    [
        Input('newproblem_labreq-addbutton_reCreP', 'n_clicks'),
        Input('newproblem_labreq-deletebutton_reCreP', 'n_clicks'),
    ],
)
def manage_labreq_content(addclick, deleteclick):
    ctx = dash.callback_context
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    newproblem_lab_request_lineitem = []

    if triggered_id and 'newproblem_labreq-addbutton_reCreP' in triggered_id:
        if len(newproblem_lab_request_lineitem) < addclick:
            i = len(newproblem_lab_request_lineitem)
            newproblem_lab_request_lineitem.extend([
                html.Div([
                    dbc.Row([
                        dbc.Col(
                            [
                                dbc.Label("Laboratory Exam and Notes"),
                                dbc.Textarea(
                                    id="newproblem_Labexamfindings_reCreP",
                                    placeholder="Enter Laboratory Examination Request and Notes needed",
                                    style={'width':'100%', 'height':25}
                                ),
                            ],
                            width = 12
                        ), 
                    ]),
                ])
            ])
    elif triggered_id and 'newproblem_labreq-deletebutton_reCreP' in triggered_id:
        if len(newproblem_lab_request_lineitem) > 0:
            newproblem_lab_request_lineitem.pop()
    else:
        raise PreventUpdate
    return [newproblem_lab_request_lineitem]



#FUNCTIONAL CALLBACKS

@app.callback( #callback for list of existing clients for returning patient
    [
        Output('re_clientlist_reCreP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('re_clientlist_reCreP', 'value'),
    ]
)
def re_clientlist_reCreP(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                client_id,
                COALESCE(client_fn, '') || ' ' || COALESCE(client_mi, '') || ' ' || COALESCE(client_ln, '') || ' ' || COALESCE(client_suffix, '') AS client_name
            FROM 
                client
            WHERE 
                NOT client_delete_ind 
            """
        values = []
        cols = ['client_id', 'client_name']
        if searchterm:
            sql += """ AND (
                client_ln ILIKE %s 
                OR client_fn ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['client_name'], 'value': row['client_id']} for _, row in result.iterrows()]
    return options, 

#reCnewP
'''
@app.callback( #callback for list of existing clients for new patient
    [
        Output('new_clientlist', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('new_clientlist', 'options'),
    ]
)
def new_clientlist(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                client_id,
                COALESCE(client_fn, '') || ' ' || COALESCE(client_mi, '') || ' ' || COALESCE(client_ln, '') || ' ' || COALESCE(client_suffix, '') AS client_name
            FROM 
                client
            WHERE 
                NOT client_delete_ind 
            """
        values = []
        cols = ['client_id', 'client_name']
        if searchterm:
            sql += """ AND (
                client_ln ILIKE %s 
                OR client_fn ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['client_name'], 'value': row['client_id']} for _, row in result.iterrows()]
    return options, 
'''
    
@app.callback( #callback for list of existing patients in the database
    [
        Output('patientlist_reCreP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('re_clientlist_reCreP', 'value'),
        Input('patientlist_reCreP', 'value'),
    ]
)
def patientlist_reCreP(pathname, selected_client_id, searchterm):
    if pathname == "/home_reCreP" and not searchterm:
        sql = """ 
            SELECT 
                patient_id,
                COALESCE(patient_m, '') ||' - ' || COALESCE(patient_type,'') || ' (' || COALESCE(patient_color, '')|| ')' AS patient_name
            FROM 
                patient
            WHERE 
                NOT patient_delete_ind
            """
        values = []

        if selected_client_id:
            sql += 'AND client_id = %s'
            values.append(selected_client_id)

        if searchterm:
            sql += """ AND (
                patient_m ILIKE %s 
                OR patient_type ILIKE %s 
                OR patient_color ILIKE %s
                );
            """
            values.extend([f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"])

        cols = ['patient_id', 'patient_name']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['patient_name'], 'value': row['patient_id']} for _, row in result.iterrows()]
        return options, 
    else:
        raise PreventUpdate  

@app.callback( #callback for list of problem status
    [
        Output('newproblem_status_reCreP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('newproblem_status_reCreP', 'value'),
    ]
)
def newproblemstatuslist(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                problem_status_id,
                problem_status_m AS problem_status_name
            FROM 
                problem_status
            WHERE 
                NOT problem_status_delete_ind 
            """
        values = []
        cols = ['problem_status_id', 'problem_status_name']
        if searchterm:
            sql += """ AND (
                problem_status_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['problem_status_name'], 'value': row['problem_status_id']} for _, row in result.iterrows()]
    return options, 

@app.callback( #callback for list of problem status
    [
        Output('followproblem_status_reCreP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('followproblem_status_reCreP', 'value'),
    ]
)
def followproblemstatuslist(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                problem_status_id,
                problem_status_m AS problem_status_name
            FROM 
                problem_status
            WHERE 
                NOT problem_status_delete_ind 
            """
        values = []
        cols = ['problem_status_id', 'problem_status_name']
        if searchterm:
            sql += """ AND (
                problem_status_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['problem_status_name'], 'value': row['problem_status_id']} for _, row in result.iterrows()]
    return options, 

@app.callback( #list of problems for follow up 
    [
        Output('problem_list_reCreP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('patientlist_reCreP', 'value'),
        Input('problem_list_reCreP', 'value'),
    ]
)
def problem_list_reCreP(pathname, selected_patient_id,searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT DISTINCT
                p.problem_id, 
                p.problem_chief_complaint AS problem_name
            FROM
                visit v JOIN problem p
            ON v.problem_id = p.problem_id
            WHERE 
                v.problem_id IS NOT NULL
                AND NOT visit_delete_ind
                AND NOT problem_delete_ind
            """
        values = []

        if selected_patient_id:
            sql += 'AND patient_id = %s'
            values.append(selected_patient_id)
        
        if searchterm:
            sql += """ AND (
                problem_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
        
        cols = ['problem_id', 'problem_name']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['problem_name'], 'value': row['problem_id']} for _, row in result.iterrows()]
        return options, 
    
    else:
        raise PreventUpdate  
     
@app.callback(#list of veterinarian assigned for visit
    [
        Output("vetlist_reCreP", 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input("vetlist_reCreP", 'value'),
    ]
)
def vetlist_reCreP(pathname, searchterm):
    if pathname == "/home_reCreP" and not searchterm:
        sql = """ 
            SELECT 
                vet_id,
                COALESCE(vet_ln, '') || ' ' || COALESCE(vet_fn, '') || ' ' || COALESCE(vet_mi, '') AS vet_name
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

@app.callback(#list of veterinarians as examiner
    [
        Output({"type": "veterinarian_list_reCreP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "veterinarian_list_reCreP", "index": MATCH}, 'value'),
    ]
)
def vetlist_reCreP(pathname, searchterm):
    if pathname == "/home_reCreP" and not searchterm:
        sql = """ 
            SELECT 
                vet_id,
                COALESCE(vet_ln, '') || ' ' || COALESCE(vet_fn, '') || ' ' || COALESCE(vet_mi, '') AS vet_name
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
      
@app.callback( #list of vaccines on the fixed card
    [
        Output("vaccine_name_reCreP", "options"),
    ],
    [
        Input('url', 'pathname'),
        Input("vaccine_name_reCreP", "value"),
    ]
)
def vaccinelistfixed(pathname, searchterm):
    if pathname == "/home_reCreP" and not searchterm:
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

@app.callback( #list of deworming on the fixed card
    [
        Output("deworm_name_reCreP", 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input("deworm_name_reCreP", 'value'),
    ]
)
def dewormlistfixed(pathname, searchterm):
    if pathname == "/home_reCreP" and not searchterm:
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

@app.callback( #list of vaccines on the variable card
    [
        Output({"type": "vaccine_name_reCreP", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "vaccine_name_reCreP", "index": MATCH}, "value"),
    ]
)
def vaccinelistvariable(pathname, searchterm):
    if pathname == "/home_reCreP" and not searchterm:
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

@app.callback( #list of deworming on the variable card
    [
        Output({"type": "deworm_name_reCreP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "deworm_name_reCreP", "index": MATCH}, 'value'),
    ]
)
def dewormlistvariable(pathname, searchterm):
    if pathname == "/home_reCreP" and not searchterm:
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

@app.callback( #list of clinical exam on fixed card
    [
        Output('newproblem_clinical_exam_list_reCreP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('newproblem_clinical_exam_list_reCreP', 'value'),
    ]
)
def newproblem_clinicalexamlistfixed(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                clinical_exam_type_id,
                clinical_exam_type_m AS clinical_exam_type_name
            FROM 
                clinical_exam_type
            WHERE 
                NOT clinical_exam_type_delete_ind 
            """
        values = []
        cols = ['clinical_exam_type_id', 'clinical_exam_type_name']
        if searchterm:
            sql += """ AND (
                clinical_exam_type_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinical_exam_type_name'], 'value': row['clinical_exam_type_id']} for _, row in result.iterrows()]
    return options,

@app.callback( #list of clinical exam on variable card
    [
        Output({"type": "newproblem_clinical_exam_list_reCreP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "newproblem_clinical_exam_list_reCreP", "index": MATCH}, 'value'),
    ]
)
def newproblem_clinicalexamlistvariable(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                clinical_exam_type_id,
                clinical_exam_type_m AS clinical_exam_type_name
            FROM 
                clinical_exam_type
            WHERE 
                NOT clinical_exam_type_delete_ind 
        """
        values = []
        cols = ['clinical_exam_type_id', 'clinical_exam_type_name']
        if searchterm:
            sql += """ AND (
                clinical_exam_type_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinical_exam_type_name'], 'value': row['clinical_exam_type_id']} for _, row in result.iterrows()]
    return options,

@app.callback( #list of clinicians on fixed card
    [
        Output('newproblem_clinician_list_reCreP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('newproblem_clinician_list_reCreP', 'value'),
    ]
)
def newproblem_clinicianlistfixed(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                clinician_id,
                COALESCE(clinician_fn, '') || ' ' || COALESCE(clinician_mi, '') || ' ' || COALESCE(clinician_ln, '') || ' ' || COALESCE(clinician_suffix, '') AS clinician_name
            FROM 
                clinician
            WHERE 
                NOT clinician_delete_ind 
            """
        values = []
        cols = ['clinician_id', 'clinician_name']
        if searchterm:
            sql += """ AND (
                clinician_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinician_name'], 'value': row['clinician_id']} for _, row in result.iterrows()]
    return options, 

@app.callback( #list of clinicians on variable card
    [
        Output({"type": "newproblem_clinician_list_reCreP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "newproblem_clinician_list_reCreP", "index": MATCH}, 'value'),
    ]
)
def newproblem_clinicianlistfixed(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                clinician_id,
                COALESCE(clinician_fn, '') || ' ' || COALESCE(clinician_mi, '') || ' ' || COALESCE(clinician_ln, '') || ' ' || COALESCE(clinician_suffix, '') AS clinician_name
            FROM 
                clinician
            WHERE 
                NOT clinician_delete_ind 
            """
        values = []
        cols = ['clinician_id', 'clinician_name']
        if searchterm:
            sql += """ AND (
                clinician_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinician_name'], 'value': row['clinician_id']} for _, row in result.iterrows()]
    return options, 

@app.callback( #list of clinical exam on fixed card
    [
        Output('followproblem_clinical_exam_list_reCreP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('followproblem_clinical_exam_list_reCreP', 'value'),
    ]
)
def followproblem_clinicalexamlistfixed(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                clinical_exam_type_id,
                clinical_exam_type_m AS clinical_exam_type_name
            FROM 
                clinical_exam_type
            WHERE 
                NOT clinical_exam_type_delete_ind 
            """
        values = []
        cols = ['clinical_exam_type_id', 'clinical_exam_type_name']
        if searchterm:
            sql += """ AND (
                clinical_exam_type_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinical_exam_type_name'], 'value': row['clinical_exam_type_id']} for _, row in result.iterrows()]
    return options,

@app.callback( #list of clinical exam on variable card
    [
        Output({"type": "followproblem_clinical_exam_list_reCreP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "followproblem_clinical_exam_list_reCreP", "index": MATCH}, 'value'),
    ]
)
def followproblem_clinicalexamlistvariable(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                clinical_exam_type_id,
                clinical_exam_type_m AS clinical_exam_type_name
            FROM 
                clinical_exam_type
            WHERE 
                NOT clinical_exam_type_delete_ind 
        """
        values = []
        cols = ['clinical_exam_type_id', 'clinical_exam_type_name']
        if searchterm:
            sql += """ AND (
                clinical_exam_type_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinical_exam_type_name'], 'value': row['clinical_exam_type_id']} for _, row in result.iterrows()]
    return options,

@app.callback( #list of clinicians on fixed card
    [
        Output('followproblem_clinician_list_reCreP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('followproblem_clinician_list_reCreP', 'value'),
    ]
)
def followproblem_clinicianlistfixed(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                clinician_id,
                COALESCE(clinician_fn, '') || ' ' || COALESCE(clinician_mi, '') || ' ' || COALESCE(clinician_ln, '') || ' ' || COALESCE(clinician_suffix, '') AS clinician_name
            FROM 
                clinician
            WHERE 
                NOT clinician_delete_ind 
            """
        values = []
        cols = ['clinician_id', 'clinician_name']
        if searchterm:
            sql += """ AND (
                clinician_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinician_name'], 'value': row['clinician_id']} for _, row in result.iterrows()]
    return options, 

@app.callback( #list of clinicians on variable card
    [
        Output({"type": "followproblem_clinician_list_reCreP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "followproblem_clinician_list_reCreP", "index": MATCH}, 'value'),
    ]
)
def followproblem_clinicianlistfixed(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                clinician_id,
                COALESCE(clinician_fn, '') || ' ' || COALESCE(clinician_mi, '') || ' ' || COALESCE(clinician_ln, '') || ' ' || COALESCE(clinician_suffix, '') AS clinician_name
            FROM 
                clinician
            WHERE 
                NOT clinician_delete_ind 
            """
        values = []
        cols = ['clinician_id', 'clinician_name']
        if searchterm:
            sql += """ AND (
                clinician_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['clinician_name'], 'value': row['clinician_id']} for _, row in result.iterrows()]
    return options, 






@app.callback( #list of laboratory exam on variable card
    [
        Output({"type": "lab_exam_list_reCreP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "lab_exam_list_reCreP", "index": MATCH}, 'value'),
    ]
)
def labexamlistvariable(pathname, searchterm):
    if pathname == "/home_reCreP"  and not searchterm:
        sql = """ 
            SELECT 
                lab_exam_type_id,
                lab_exam_type_m AS lab_exam_type_name
            FROM 
                lab_exam_type
            WHERE 
                NOT lab_exam_type_delete_ind 
            """
        values = []
        cols = ['lab_exam_type_id', 'lab_exam_type_name']
        if searchterm:
            sql += """ AND (
                lab_exam_type_m ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
    else:
        raise PreventUpdate  
     
    result = db.querydatafromdatabase(sql, values, cols)
    options = [{'label': row['lab_exam_type_name'], 'value': row['lab_exam_type_id']} for _, row in result.iterrows()]
    return options,


"""    
@app.callback( # opens edit vaccine medication modal
    [
        Output('vacc_add_modal', 'is_open'),
    ],
    [
        Input({"type": "vacc_edit_btn", "index": ALL}, "n_clicks"),
        Input('edit_vaccine_submit_btn','n_clicks'),
    ],
    [
        State('vacc_add_modal', 'is_open'),
        State('edit_vaccine_name', 'value'),
        State('edit_vaccine_dose','value'),
        State('edit_vacc_from_vetmed','value'),
        State('edit_vaccine_admin', 'date'),
        State('edit_vaccine_exp', 'date'),
    ]
)
def toggle_vaccine_modal(vacc_add_btn, submitbtn, vacc_modal, name, dose, from_vetmed, admin, exp):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'add_vaccine_form_btn' and vacc_add_btn:
            return [not vacc_modal]
        
        if eventid == 'add_vaccine_submit_btn' and submitbtn and all([name, dose, from_vetmed, admin, exp]):
            return [not vacc_modal]
        
    return [vacc_modal]
"""  
@app.callback( # fills edit vaccine medication modal
    [
        Output('vacc_edit_modal', 'is_open'),
        Output('edit_vaccine_name', 'value'),
        Output('edit_vaccine_dose','value'),
        Output('edit_vacc_from_vetmed','value'),
        Output('edit_vaccine_admin', 'date'),
        Output('edit_vaccine_exp', 'date'),
    ],
    [
        Input({"type": "vacc_edit_btn", "index": ALL}, "n_clicks"),
        Input({"type": "edit_vaccine_submit_btn", "index": ALL}, "n_clicks"),
    ],
    [
        State('vacc_edit_modal', 'is_open'),
        State('edit_vaccine_name', 'value'),
        State('edit_vaccine_dose','value'),
        State('edit_vacc_from_vetmed','value'),
        State('edit_vaccine_admin', 'date'),
        State('edit_vaccine_exp', 'date'),
    ]
)
def toggle_vaccine_modal(vacc_add_btn, submitbtn, vacc_modal, name, dose, from_vetmed, admin, exp):
    ctx = dash.callback_context

    

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        value = ctx.triggered[0]['value']
        id_dictionary = json.loads(eventid)
        btn_id = id_dictionary["type"]
        vacc_id = id_dictionary["index"]
    
        sql ="""
            SELECT 
                vacc_m_id,
                vacc_dose,
                vacc_date_administered,
                vacc_exp,
                vacc_from_vetmed
            FROM vacc
            WHERE vacc_id = %s and vacc_delete_ind = False
            """
        value = [vacc_id]
        col = ['name', 'dose', 'admin', 'exp', 'from_vetmed']
        df = db.querydatafromdatabase(sql, value, col)

        name = int(df['name'][0])
        dose = df['dose'][0]
        admin = df['admin'][0]
        exp = df['exp'][0]
        from_vetmed = df['from_vetmed'][0]

        if btn_id == "vacc_edit_btn" and value:
            return [not vacc_modal, name, dose, from_vetmed, admin, exp]
        
        if btn_id == "edit_vaccine_submit_btn" and value and all([name, dose, from_vetmed, admin, exp]):
            return [not vacc_modal, None, None, None, None, None]
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback( #Add vaccine table in the layout
    Output("visit_vaccine_list", "children"),
    Input("url", "pathname")
)
def visit_deworm_list(pathname):

    sql = """
        SELECT MAX(visit_id)
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])
    visit_id = 18

    try:  
        if pathname == "/home_visit/purpose":

            sql = """
                SELECT
                    vacc_no,
                    vacc_m,
                    vacc_dose,
                    TO_CHAR(vacc_date_administered, 'Mon DD, YYYY'),
                    TO_CHAR(vacc_exp, 'Mon DD, YYYY'),
                    vacc_from_vetmed,
                    v.vacc_id
                FROM vacc v 
                    INNER JOIN vacc_m m on v.vacc_m_id = m.vacc_m_id
                WHERE NOT vacc_delete_ind
                    AND visit_id = %s
            """
            values = [visit_id]
            cols = ["No.", "Vaccine Name", "Vaccine Dose", "Date Administered", "Expiration Date", "Vaccine from VetMed?", "ID"]

            df = db.querydatafromdatabase(sql, values, cols)

            if not df.empty:

                buttons = []
                for vacc_id in df["ID"]:
                    buttons += [
                        html.Div(
                            dbc.Button("Edit", id={"type": "vacc_edit_btn", "index": vacc_id}, size = 'sm', color = 'success'),
                            style = {'text-align': 'center'}
                        )
                    ]
                df['Action'] = buttons
                df = df[["No.", "Vaccine Name", "Vaccine Dose", "Date Administered", "Expiration Date", "Vaccine from VetMed?", "Action"]]
                df["Vaccine from VetMed?"] = df["Vaccine from VetMed?"].apply(lambda x: 'Yes' if x else 'No')


                table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align': 'center'})
                return [table]
            else:
                empty_df = pd.DataFrame(columns=["No.", "Vaccine Name", "Vaccine Dose", "Date Administered", "Expiration Date", "Vaccine from VetMed?", "Action"])
                table = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'}, header=True, index=False)
                return [table]
        else:
            return [html.Div()]
    except Exception as e:
        print(f"An error occurred: {e}")
        return [html.Div()]
  
  
@app.callback( #update vaccine table in the layout
    [
        Output("visit_vaccine_list", "children"),
    ],
    [
        Input("url", "pathname"),
        Input("add_vaccine_submit_btn", "n_clicks"),
        Input('add_vaccine_name', 'value'),
        Input('add_vaccine_dose','value'),
        Input('add_vacc_from_vetmed','value'),
        Input('add_vaccine_admin', 'date'),
        Input('add_vaccine_exp', 'date'),
    ],
    [
        State("visit_vaccine_list", "children"),
    ],
)
def visit_vaccine_list(pathname, submitbtn, name, dose, from_vetmed, admin, exp, table):

    sql = """
        SELECT MAX(visit_id)
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])
    visit_id = 18

    sql = """
        SELECT MAX(vacc_no) + 1
        FROM vacc
        WHERE visit_id = %s
        """
    value = [visit_id]
    df = db.querydatafromdatabase(sql,value)
    vacc_no = int(df.loc[0,0])

    if pathname == "/home_visit/purpose":

        ctx = dash.callback_context
        
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        
            alert_open = False
            alert_color = ''
            alert_text = ''

            if eventid == 'add_vaccine_submit_btn' and submitbtn:

                if not name:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please select the administered vaccine medication'
                elif not dose:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please select the dose of the administered vaccine'
                elif not dose:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please select the dose of the administered vaccine'
                elif not from_vetmed:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please select whether the vaccine was administered in VetMed or not'
                elif not admin:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please fill the date when the vaccine was administered'
                elif not exp:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please fill the expiration date of the administered vaccine'
                else:
                    sql = '''
                    INSERT INTO vacc(
                                    vacc_no,
                                    vacc_m_id,
                                    vacc_dose,
                                    vacc_date_administered,
                                    vacc_exp,
                                    vacc_from_vetmed,
                                    vacc_delete_ind,
                                    visit_id
                                )
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                        '''
                    values = [vacc_no, name, dose, admin, exp, from_vetmed, False, visit_id]

                    db.modifydatabase(sql, values)

                if not all([name, dose, from_vetmed, admin, exp]):
                    return [table, alert_color, alert_text, alert_open, name, dose, from_vetmed, admin, exp]

        sql = """
            SELECT
                vacc_no,
                vacc_m,
                vacc_dose,
                TO_CHAR(vacc_date_administered, 'Mon DD, YYYY'),
                TO_CHAR(vacc_exp, 'Mon DD, YYYY'),
                vacc_from_vetmed,
                v.vacc_id
            FROM vacc v 
                INNER JOIN vacc_m m on v.vacc_m_id = m.vacc_m_id
            WHERE NOT vacc_delete_ind
                AND visit_id = %s
        """
        values = [visit_id]
        cols = ["No.", "Vaccine Name", "Vaccine Dose", "Date Administered", "Expiration Date", "Vaccine from VetMed?", "ID"]

        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:

            buttons = []
            for vacc_id in df["ID"]:
                buttons += [
                    html.Div(
                        dbc.Button("Edit", id={"type": "vacc_edit_btn", "index": vacc_id}, size = 'sm', color = 'success'),
                        style = {'text-align': 'center'}
                    )
                ]
            df['Action'] = buttons
            df = df[["No.", "Vaccine Name", "Vaccine Dose", "Date Administered", "Expiration Date", "Vaccine from VetMed?", "Action"]]
            df["Vaccine from VetMed?"] = df["Vaccine from VetMed?"].apply(lambda x: 'Yes' if x else 'No')


            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align': 'center'})
        else:
            empty_df = pd.DataFrame(columns=["No.", "Vaccine Name", "Vaccine Dose", "Date Administered", "Expiration Date", "Vaccine from VetMed?", "Action"])
            table = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'}, header=True, index=False)

        return [table, alert_color, alert_text, alert_open, None, None, None, None, None]
            
    else:
        raise PreventUpdate


@app.callback( # Submit Button for vaccine
    [
        Output('add_vaccinevisitrecord_alert','color'),
        Output('add_vaccinevisitrecord_alert','children'),
        Output('add_vaccinevisitrecord_alert','is_open'),
        Output('add_vaccine_name', 'value'),
        Output('add_vaccine_dose','value'),
        Output('add_vacc_from_vetmed','value'),
        Output('add_vaccine_admin', 'date'),
        Output('add_vaccine_exp', 'date'),
    ],
    [
        Input('add_vaccine_submit_btn','n_clicks'),
        Input('add_vaccine_name', 'value'),
        Input('add_vaccine_dose','value'),
        Input('add_vacc_from_vetmed','value'),
        Input('add_vaccine_admin', 'date'),
        Input('add_vaccine_exp', 'date'),
    ],
)
def vacc_add_submit(submitbtn, name, dose, from_vetmed, admin, exp):

    sql = """
        SELECT MAX(visit_id)
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])
    visit_id = 18

    sql = """
        SELECT MAX(vacc_no) + 1
        FROM vacc
        WHERE visit_id = %s
        """
    value = [visit_id]
    df = db.querydatafromdatabase(sql,value)
    vacc_no = int(df.loc[0,0])

    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        alert_open = False
        alert_color = ''
        alert_text = ''

        if eventid == 'add_vaccine_submit_btn' and submitbtn:

            if not name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please select the administered vaccine medication'
            elif not dose:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please select the dose of the administered vaccine'
            elif not dose:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please select the dose of the administered vaccine'
            elif not from_vetmed:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please select whether the vaccine was administered in VetMed or not'
            elif not admin:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please fill the date when the vaccine was administered'
            elif not exp:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please fill the expiration date of the administered vaccine'
            else:
                sql = '''
                INSERT INTO vacc(
                                vacc_no,
                                vacc_m_id,
                                vacc_dose,
                                vacc_date_administered,
                                vacc_exp,
                                vacc_from_vetmed,
                                vacc_delete_ind,
                                visit_id
                            )
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                values = [vacc_no, name, dose, admin, exp, from_vetmed, False, visit_id]

                db.modifydatabase(sql, values)

            if not all([name, dose, from_vetmed, admin, exp]):
                return [alert_color, alert_text, alert_open, name, dose, from_vetmed, admin, exp]

            return [alert_color, alert_text, alert_open, None, None, None, None, None]
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback( # fills edit vaccine medication modal
    [
        Output('edit_vaccine_name', 'value'),
        Output('edit_vaccine_dose','value'),
        Output('edit_vacc_from_vetmed','value'),
        Output('edit_vaccine_admin', 'date'),
        Output('edit_vaccine_exp', 'date'),
    ],
    [
        Input({"type": "vacc_edit_btn", "index": ALL}, "n_clicks"),
    ],
)
def fill_edit_vaccine_modal(vacc_add_btn): #, submitbtn, vacc_modal, name, dose, from_vetmed, admin, exp):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        value = ctx.triggered[0]['value']
        id_dictionary = json.loads(eventid)
        btn_id = id_dictionary["type"]
        vacc_id = id_dictionary["index"]
    
        sql ="""
            SELECT 
                vacc_m_id,
                vacc_dose,
                vacc_date_administered,
                vacc_exp,
                CASE 
                    WHEN vacc_from_vetmed THEN 'true' 
                    ELSE 'false' 
                END as vacc_from_vetmed
            FROM vacc
            WHERE vacc_id = %s and vacc_delete_ind = False
            """
        value = [vacc_id]
        col = ['name', 'dose', 'admin', 'exp', 'from_vetmed']
        df = db.querydatafromdatabase(sql, value, col)

        name = df['name'][0]
        dose = df['dose'][0]
        admin = df['admin'][0]
        exp = df['exp'][0]
        from_vetmed = df['from_vetmed'][0]

        if btn_id == "vacc_edit_btn" and value:
            return [name, dose, from_vetmed, admin, exp]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

"""
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import webbrowser
from app import app
from apps import sidebar as sb
from apps import login
from apps.records import existingpatient, newpatient, viewclinicians, viewrecords, editrecords, editvaccine, editdeworm, viewusers, generatereports, editusers, home_visit, purpose, managedata, help, newclinician, editclinicians, newuser

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "width": "100%",
}

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=True),
        
        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=True, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),
        
        html.Div(
            sb.sidebar,
            id='sidebar_div'
        ),

        html.Div(
            [
                # sb.sidebar,
                html.Div(id="page-content", style=CONTENT_STYLE),
            ],
            style = {'display':'flex'},
        )
    ],
    style={'width':'100%'}
)

@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
        Output('sidebar_div', 'className'), 
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]
)
def displaypage(pathname, sessionlogout, userid):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]["prop_id"].split(".")[0]
        if eventid == "url":
            if userid < 0: # if logged out
                if pathname == '/':
                    returnlayout = login.layout
                elif pathname == '/signup':
                    returnlayout = newuser.layout
                else:
                    returnlayout = '404: request not found'

            else:
                if pathname == '/logout':
                        returnlayout = login.layout
                        sessionlogout = True

                elif pathname == "/" or pathname == "/home_visit":
                    returnlayout = home_visit.layout
                elif pathname == "/purpose" or pathname == "/home_visit/purpose":
                    returnlayout = purpose.layout
                elif pathname == "/newrecord" or pathname == "/newrecord/newpatient":
                    returnlayout = newpatient.layout
                elif pathname == "/newrecord/existingpatient":
                    returnlayout = existingpatient.layout
                elif pathname == "/viewrecord":
                    returnlayout = viewrecords.layout
                elif pathname == "/editrecord":
                    returnlayout = editrecords.layout
                elif pathname == "/editvaccine":
                    returnlayout = editvaccine.layout
                elif pathname == "/editdeworm":
                    returnlayout = editdeworm.layout
                elif pathname == "/newuser":
                    returnlayout = newuser.layout
                elif pathname == "/viewuser":
                    returnlayout = viewusers.layout
                elif pathname == "/edituser":
                    returnlayout = editusers.layout
                elif pathname == "/managedata":
                    returnlayout = managedata.layout
                elif pathname == "/managedata/newclinicians":
                    returnlayout = newclinician.layout
                elif pathname == "/managedata/existingclinicians":
                    returnlayout = viewclinicians.layout
                elif pathname == "/editclinician":
                    returnlayout = editclinicians.layout
                elif pathname == "/newreport":
                    returnlayout = generatereports.layout
                elif pathname == "/help":
                    returnlayout = help.layout
                else:
                    returnlayout = "error404" 
            # return [returnlayout]
        
            # decide sessionlogout value
            logout_conditions = [
                pathname in ['/', '/logout'],
                userid == -1,
                not userid
            ]
            sessionlogout = any(logout_conditions)
        
            sidebar_classname = 'd-none' if sessionlogout else ''
        
        
        else:
            raise PreventUpdate
    
        return [returnlayout, sessionlogout, sidebar_classname]
    else:
        raise PreventUpdate

    
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050/", new=0, autoraise=True)
    app.run_server(debug=False)
"""

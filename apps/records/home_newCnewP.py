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


layout = html.Div([
        #html.H1("Homepage"),
        dbc.Alert(id = 'visitrecord_alert_newCnewP', is_open = False),
        html.Br(),
        dbc.Card( # Main Visits Info
            [
                dbc.CardHeader(
                    html.Div([
                            #html.H2(f"Visits for {datetime.now().strftime('%B %d, %Y')}")
                            html.H2("Record Visits", className = "flex-grow-1"),
                            html.Div([
                                dbc.Button("Returning Patient",href= '/home_reCreP',className = "me-2",n_clicks = 0),
                                dbc.Button("New Patient",href= '/home_reCnewP',n_clicks = 0),
                            ], className = "ml-2 d-flex")
                        ], className = "d-flex align-items-center justify-content-between")
                ),

                dbc.CardBody([
                    dbc.Row([
                        html.Div([
                            html.H4("Client Information", className = "flex-grow-1"),
                            html.Div([
                                dbc.Button("Returning Client", href= '/home_reCnewP',className = "me-2",n_clicks = 0), 
                                dbc.Button("New Client", href= '/home_newCnewP',n_clicks = 0),
                            ], className = "ml-2 d-flex")
                        ], className = "d-flex align-items-center justify-content-between"),
                    ], className = 'mb-3', id = 'owner_info1'),

                    dbc.Row([

                        dbc.Col(
                            [
                                dbc.Label("Last Name"),
                                dbc.Input(id='client_ln_newCnewP', type='text', placeholder='Enter Last Name', style={'width':'100%'})
                            ],
                            width=2
                        ),

                        dbc.Col(
                            [
                                dbc.Label("First Name"),
                                dbc.Input(id='client_fn_newCnewP', type='text', placeholder='Enter First Name', style={'width':'100%'})
                            ],
                            width=2
                        ),

                        dbc.Col(
                            [
                                dbc.Label("Middle Initial"),
                                dbc.Input(id='client_mi_newCnewP', type='text', placeholder='Enter MI', style={'width':'100%'})
                            ],
                            width=2
                        ),

                        dbc.Col(
                            [
                                dbc.Label("Suffix"),
                                dbc.Input(id='client_suffix_newCnewP', type='text', placeholder='N/A if none', style={'width':'75%'})
                            ],
                            width=2
                        ),

                        dbc.Col(
                            [
                                dbc.Label("Email Address"),
                                dbc.Input(id='client_email_newCnewP', type='text', placeholder='Enter Email Address', style={'width':'100%'})
                            ],
                            width=2
                        ),

                        dbc.Col(
                            [
                                dbc.Label("Contact Number"),
                                dbc.Input(id='client_cn_newCnewP', type='text', placeholder='Enter Contact Number', style={'width':'100%'})
                            ],
                            width=2
                        ),

                    ], className="mb-3", id = 'owner_info2'), # end of row for owner name

                    dbc.Row([      

                        dbc.Col(
                            [
                                dbc.Label("House Number"),
                                dbc.Input(id='client_house_no_newCnewP', type='text', placeholder='Enter House Number', style={'width':'100%'})
                            ],
                            width=2
                        ),

                        dbc.Col(
                            [
                                dbc.Label("Street"),
                                dbc.Input(id='client_street_newCnewP', type='text', placeholder='Enter Street', style={'width':'100%'})
                            ],
                            width = 3
                        ),
                            
                        dbc.Col(
                            [
                                dbc.Label("Barangay"),
                                dbc.Input(id='client_barangay_newCnewP', type='text', placeholder='Enter Barangay', style={'width':'100%'})
                            ],
                            width=2
                        ),

                        dbc.Col(
                            [
                                dbc.Label("City"),
                                dbc.Input(id='client_city_newCnewP', type='text', placeholder='Enter City', style={'width':'100%'})
                            ],
                            width=2
                        ),                    

                        dbc.Col(
                            [
                                dbc.Label("Province"),
                                dbc.Input(id='client_province_newCnewP', type='text', placeholder='Enter Province', style={'width':'100%'})
                            ],
                            width=3
                        ),
                    ], className="mb-4", id = 'owner_info3'), # end of row of email address, contact num, province

                    dbc.Row([dbc.Col(html.H4("Patient Information"), width = 3)], className = 'mb-3', id = 'patient_info1'),   

                    dbc.Row([
                            
                        dbc.Col(
                            [
                                dbc.Label("Name"),
                                dbc.Input(id='patient_m_newCnewP', type='text', placeholder='Enter Patient Name', style={'width':'100%'})
                            ],
                            width=2
                        ),

                        dbc.Col(
                            [
                                dbc.Label("Animal Type"),
                                dbc.Input(id='patient_type_newCnewP', type='text', placeholder='Ex: Dog or Cat', style={'width':'100%'})
                            ],
                            width=2
                        ),
                        
                        dbc.Col(
                            [
                                dbc.Label("Breed"),
                                dbc.Input(id='patient_breed_newCnewP', type='text', placeholder='Enter Breed', style={'width':'100%'})
                            ],
                            width=2
                        ),

                        dbc.Col(
                            [
                                dbc.Label("Color Markings"),
                                dbc.Input(id='patient_color_newCnewP', type='text', placeholder='Enter Color Markings', style={'width':'100%'})
                            ],
                            width=2
                        ),

                        dbc.Col(
                            [
                                dbc.Label("Sex"),
                                dcc.Dropdown(
                                    id='patient_sex_newCnewP',
                                    options=[
                                        {'label':'Male', 'value':'Male'},
                                        {'label':'Female', 'value':'Female'},
                                    ],
                                    placeholder='Select Sex',
                                    style={'width':'100%'},
                                ),
                            ],
                            width=2 
                        ),
                            
                        dbc.Col(
                            [
                                dbc.Label("Birthdate"),
                                dmc.DatePicker(
                                    id='patient_bd_newCnewP',
                                    placeholder="Select Birthdate",
                                    style={'width':'100%'},
                                    inputFormat='MMM DD, YYYY',
                                    dropdownType='modal',
                                ),
                            ],
                            width=2
                        ),
                    ], className="mb-3", id = 'patient_info2'), # end of row for name, sex, breed

                    dbc.Row([

                        dbc.Col(
                            [
                                dbc.Label("Idiosyncrasies"),
                                dbc.Input(id='patient_idiosync_newCnewP', type='text', placeholder='Enter Idiosyncrasies', style={'width':'100%'})
                            ],
                            width=12
                        ),
                    ], className="mb-3", id = 'patient_info3'), # end of row for birthdate, idiosyncrasies, color markings

                    html.Br(),

                    dbc.Row([ #Select Veterinarian
                            
                        dbc.Col(html.H4("Veterinarian Assigned"), width=3),

                        dbc.Col(
                            dcc.Dropdown(
                                id="vetlist_newCnewP",
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
                                id='visitdate_newCnewP',
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
                            id="visitpurpose_newCnewP",
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
        html.Div(id="visitinputs_newCnewP"),
        html.Br(),
        dbc.Button(
                    'Submit',
                    id = 'visitrecord_submit_newCnewP',
                    n_clicks = 0, #initialization 
                    className='custom-submitbutton',
                ),
        dbc.Modal([
            dbc.ModalHeader(html.H4('Visit Recorded Successfully!')),
        ],
        centered = True, id = 'visitrecord_successmodal_newCnewP',
        backdrop = 'static'
        ),
    ])

# SUBMISSION AND EDIT CALLBACKS
'''
@app.callback(
        [
            Output('visitrecord_alert_newCnewP','color'),
            Output('visitrecord_alert_newCnewP','children'),
            Output('visitrecord_alert_newCnewP','is_open'),
            Output('visitrecord_successmodal_newCnewP','is_open'),
        ],
        [
            Input('visitrecord_submit_newCnewP','n_clicks')
        ],
        [

        ]
)

def visitrecord_save(submitbtn):
    ctx.dash.callback_context
'''



#LAYOUT CALLBACKS

@app.callback( #callback to add inputs depending on the selected visit purpose
    Output("visitinputs_newCnewP", "children"),
    Input("visitpurpose_newCnewP", "value"),
    State("visitpurpose_newCnewP", "value"),
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
                            dbc.Row([
                                dbc.Col(html.H2("Vaccination"), width="auto"),
                                dbc.Col(
                                    [
                                        dbc.Button("+", id='vaccine-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                        dbc.Button("-", id='vaccine-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                    ],
                                    width="auto", 
                                    className="text-right"
                                ),
                            ], justify = "between"),
                        ),
                        dbc.CardBody([
                            html.Div([
                                html.Div(style={'height':'5px'}),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Vaccine Medication"),
                                        dcc.Dropdown(
                                            id="vaccine_name_newCnewP",
                                            placeholder='Select Vaccine',
                                            searchable=True,
                                            options=[],
                                            value=None,
                                        )],
                                        width = 4,
                                    ),
                                    dbc.Col([
                                        dbc.Label("Vaccine Dosage"),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="vaccine_dose_newCnewP",
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
                                            id={"type": "vaccine_date_newCnewP", "index": 0},
                                            placeholder="Select Date Administered",
                                            inputFormat='MMM DD, YYYY',
                                            dropdownType='modal',
                                        )],
                                        width = 3,
                                    ),
                                    dbc.Col([
                                        dbc.Label("Vaccine Expiration"),
                                        dmc.DatePicker(
                                            id={"type": "vaccine_expdate_newCnewP", "index": 0},
                                            placeholder="Select Expiration Date",
                                            inputFormat='MMM DD, YYYY',
                                            dropdownType='modal',
                                        )],
                                        width = 3,
                                    ),
                                ]),
                                html.Div(style={'height':'5px'}),        
                            ]),
                            html.Div(id='vaccine-line-items_newCnewP'),
                        ]),
                    ], 
                ),
            ])
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
                                    dbc.Button("+", id='deworm-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                    dbc.Button("-", id='deworm-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
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
                                        id="deworm_name_newCnewP",
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
                                            id="deworm_dose_newCnewP",
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
                                        id={"type": "deworming_date_newCnewP", "index": 1},
                                        placeholder="Select Date Administered",
                                        inputFormat='MMM DD, YYYY',
                                        dropdownType='modal',
                                    )],
                                    width = 3,
                                ),
                                dbc.Col([
                                    dbc.Label("Medication Expiration"),
                                    dmc.DatePicker(
                                        id={"type": "deworming_medication_expdate_newCnewP", "index": 1},
                                        placeholder="Select Expiration Date",
                                        inputFormat='MMM DD, YYYY',
                                        dropdownType='modal',
                                    )],
                                    width = 3,
                                ),
                            ]),
                            html.Div(style={'height':'5px'}),        
                        ]),
                        html.Div(id='deworm-line-items_newCnewP'),
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
                                    id = "problem_status_newCnewP",
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
                                dbc.Col(dbc.Input(id="newproblem_newCnewP", type='text', placeholder='Enter Problem')),
                            ],
                        ),
                        html.Br(),

                        dbc.Row(dbc.Col(html.H3("Health & Nutrients Intake"))),

                        dbc.Row([ # Under health and nutrients
                            dbc.Col(
                                [
                                    dbc.Label("Relevant Medical History"),
                                    dbc.Textarea(id='newproblem_newCnewP_medhistory', placeholder='Enter Any Relevant Medical History', style={"height":75})
                                ],
                                width=6
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Diet"),
                                    dbc.Textarea(id='newproblem_newCnewP_diet', placeholder="Enter Patient's Diet", style={"height":75})
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Water Source"),
                                    dbc.Textarea(id='newproblem_newCnewP_water', placeholder="Enter Patient's Water Source", style={"height":75})
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
                                    dbc.Input(id='newproblem_newCnewP_temp', type='text', placeholder='Enter Temperature')
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Pulse Rate"),
                                    dbc.Input(id='newproblem_newCnewP_pr', type='text', placeholder="Enter Pulse Rate")
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Weight"),
                                    dbc.Input(id='newproblem_newCnewP_weight', type='text', placeholder='Enter Weight')
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Respiration Rate"),
                                    dbc.Input(id='newproblem_newCnewP_rr', type='text', placeholder="Enter Respiration Rate")
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Body Condition Score"),
                                    dbc.Input(id='newproblem_newCnewP_bodyconditionscore', type='text', placeholder="Enter Body Condition Score")
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
                                    dbc.Button("+", id='clinicalexam-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                    dbc.Button("-", id='clinicalexam-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
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
                                                    id= "clinical_exam_list_newCnewP",
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
                                                    id={"type": "newclinicalfindings_newCnewP", "index": 1},
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
                                                    id="clinician_list_newCnewP",
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
                            html.Div(id = "clinical_exam_content_newCnewP")
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
                                                dbc.Button("+", id='labresult-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                                dbc.Button("-", id='labresult-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                            ],
                                            width = 'auto',
                                            className = 'text-right'
                                        ),
                                    ], justify = 'between'),
                                ),
                                html.Div(id='labresult_lineitems_newCnewP'),

                                html.Br(),

                                dbc.Row([ #under progress notes
                                    dbc.Col([
                                        dbc.Label("Differential Diagnosis"),
                                        dbc.Textarea(
                                            id={"type": "newdifferentialdiagnosis_newCnewP", "index": 1},
                                            placeholder="Enter Differential Diagnosis",
                                            style={'width':'100%', 'height':100}
                                        ),
                                    ]),
                                    dbc.Col([
                                        dbc.Label("Possible Treatment"),
                                        dbc.Textarea(
                                            id={"type": "newpossibletreatment_newCnewP", "index": 1},
                                            placeholder="Enter Treatment Options",
                                            style={'width':'100%', 'height':100}
                                        ),
                                    ]),
                                    dbc.Col([
                                        dbc.Row([
                                            dbc.Label("OR Number"),
                                            dbc.Textarea(
                                            id={"type": "newornumber_newCnewP", "index": 1},
                                            placeholder="Enter OR No.",
                                            style={'width':'100%', 'height':25}
                                            ),
                                        ]),
                                        dbc.Row([
                                            dbc.Label("Bill"),
                                            dbc.Textarea(
                                            id={"type": "newbill_newCnewP", "index": 1},
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
                                            dbc.Button("+", id='labreq-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                            dbc.Button("-", id='labreq-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                        ],
                                        width = 'auto',
                                        className = 'text-right'
                                    ),
                                ], justify = 'between'),),
                                html.Div(id='labreq_lineitems_newCnewP'),
                                html.Br(),
                            ]), 
                            html.Div(id = "progress_notes_content_newCnewP"),
                        ]),
                        html.Br(),
                        
                        html.Hr(), #line                            

                        dbc.Row(dbc.Col(html.H4("Diagnosis and Treatment"))),
                        dbc.Row([ # Under Diagnosis
                            dbc.Col(
                                [
                                    dbc.Label("Diagnosis"),
                                    dbc.Textarea(id='newproblem_newCnewP_diagnosis', placeholder='Enter Diagnosis', style={"height":50})
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Prescription"),
                                    dbc.Textarea(id='newproblem_newCnewP_prescription', placeholder="Enter Prescription", style={"height":50})
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Patient instructions"),
                                    dbc.Textarea(id='newproblem_newCnewP_clienteduc', placeholder="Enter instructions", style={"height":50})
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
                                    id = "problem_status_newCnewP",
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
                                    id="problem_list_newCnewP",
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
                                    dbc.Textarea(id='newproblem_newCnewP_medhistory', placeholder='Enter Any Relevant Medical History', style={"height":75})
                                ],
                                width=6
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Diet"),
                                    dbc.Textarea(id='newproblem_newCnewP_diet', placeholder="Enter Patient's Diet", style={"height":75})
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Water Source"),
                                    dbc.Textarea(id='newproblem_newCnewP_water', placeholder="Enter Patient's Water Source", style={"height":75})
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
                                    dbc.Input(id='newproblem_newCnewP_temp', type='text', placeholder='Enter Temperature')
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Pulse Rate"),
                                    dbc.Input(id='newproblem_newCnewP_pr', type='text', placeholder="Enter Pulse Rate")
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Weight"),
                                    dbc.Input(id='newproblem_newCnewP_weight', type='text', placeholder='Enter Weight')
                                ],
                                width=2
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Respiration Rate"),
                                    dbc.Input(id='newproblem_newCnewP_rr', type='text', placeholder="Enter Respiration Rate")
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Body Condition Score"),
                                    dbc.Input(id='newproblem_newCnewP_bodyconditionscore', type='text', placeholder="Enter Body Condition Score")
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
                                    dbc.Button("+", id='clinicalexam-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                    dbc.Button("-", id='clinicalexam-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
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
                                                    id="clinical_exam_list_newCnewP",
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
                                                    id={"type": "newclinicalfindings_newCnewP", "index": 1},
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
                                                    id = "clinician_list_newCnewP",
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
                            html.Div(id = "clinical_exam_content_newCnewP")
                        ]),
                        html.Br(),
                        
                        html.Hr(), #line
                        
                        dbc.Row([ # Progress Notes Add/Delete button
                            dbc.Col(html.H3("Progress Notes"), width=3),
                            dbc.Col(
                                [
                                    dbc.Button("+", id='notes-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                    dbc.Button("-", id='notes-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                ],
                                width = 'auto',
                                className = 'text-right'
                            ),
                        ], justify = 'between'),
                        html.Div(id='notes-lineitems'),

                        html.Hr(), #line

                        dbc.Container([ # Progress Notes Content
                            html.Div([
                                html.Div(
                                    dbc.Row([ # Laboratory Result Add/Delete button
                                        dbc.Col(html.H5("Add Laboratory Results:"), width=6),
                                        dbc.Col(
                                            [
                                                dbc.Button("+", id='labresult-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                                dbc.Button("-", id='labresult-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                            ],
                                            width = 'auto',
                                            className = 'text-right'
                                        ),
                                    ], justify = 'between'),
                                ),
                                html.Div(id='labresult_lineitems_newCnewP'),

                                html.Br(),

                                dbc.Row([ #under progress notes
                                    dbc.Col([
                                        dbc.Label("Differential Diagnosis"),
                                        dbc.Textarea(
                                            id={"type": "newdifferentialdiagnosis_newCnewP", "index": 1},
                                            placeholder="Enter Differential Diagnosis",
                                            style={'width':'100%', 'height':100}
                                        ),
                                    ]),
                                    dbc.Col([
                                        dbc.Label("Possible Treatment"),
                                        dbc.Textarea(
                                            id={"type": "newpossibletreatment_newCnewP", "index": 1},
                                            placeholder="Enter Treatment Options",
                                            style={'width':'100%', 'height':100}
                                        ),
                                    ]),
                                    dbc.Col([
                                        dbc.Row([
                                            dbc.Label("OR Number"),
                                            dbc.Textarea(
                                            id={"type": "newornumber_newCnewP", "index": 1},
                                            placeholder="Enter OR No.",
                                            style={'width':'100%', 'height':25}
                                            ),
                                        ]),
                                        dbc.Row([
                                            dbc.Label("Bill"),
                                            dbc.Textarea(
                                            id={"type": "newbill_newCnewP", "index": 1},
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
                                            dbc.Button("+", id='labreq-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                            dbc.Button("-", id='labreq-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                                        ],
                                        width = 'auto',
                                        className = 'text-right'
                                    ),
                                ], justify = 'between'),),
                                html.Div(id='labreq_lineitems_newCnewP'),
                                html.Br(),
                            ]), 
                            html.Div(id = "progress_notes_content_newCnewP"),
                        ]),
                        html.Br(),
                        
                        html.Hr(), #line                            

                        dbc.Row(dbc.Col(html.H4("Diagnosis and Treatment"))),
                        dbc.Row([ # Under Diagnosis
                            dbc.Col(
                                [
                                    dbc.Label("Diagnosis"),
                                    dbc.Textarea(id='newproblem_newCnewP_diagnosis', placeholder='Enter Diagnosis', style={"height":50})
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Prescription"),
                                    dbc.Textarea(id='newproblem_newCnewP_prescription', placeholder="Enter Prescription", style={"height":50})
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Patient instructions"),
                                    dbc.Textarea(id='newproblem_newCnewP_clienteduc', placeholder="Enter instructions", style={"height":50})
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
    Output('visitpurpose_newCnewP','value'),
    Input('visitpurpose_newCnewP','value')
)

def update_checklist(selected_options):
    if selected_options is None:
        return []
    
    last_option = selected_options[-1] if selected_options else None
    
    if last_option in ['new_problem', 'follow_up']:
        mutually_exclusive_option = 'follow_up' if last_option == 'new_problem' else 'new_problem'
        if mutually_exclusive_option in selected_options:
            selected_options.remove(mutually_exclusive_option)

    return selected_options

vaccine_lineitem_newCnewP = []

@app.callback( #callback for adding a row for vaccines administered
    [
        Output('vaccine-line-items_newCnewP', 'children'),
    ],
    [
        Input('vaccine-addbutton_newCnewP', 'n_clicks'),
        Input('vaccine-deletebutton_newCnewP', 'n_clicks'),
    ],
    [
        State('vaccine-line-items_newCnewP', 'children'),
    ],
)

def manage_vaccine_line_item(addclick, deleteclick, existing_items):

    vaccine_lineitem_newCnewP = existing_items or []

    ctx = dash.callback_context
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and 'vaccine-addbutton_newCnewP' in triggered_id:
        if len(vaccine_lineitem_newCnewP) < addclick:
            i = len(vaccine_lineitem_newCnewP)
            vaccine_lineitem_newCnewP.extend([
                html.Div([
                    html.Div(style={'height':'5px'}),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id={"type": "vaccine_name_newCnewP", "index": i},
                                placeholder='Select Vaccine',
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                            width = 4,
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id={"type": "vaccine_dose_newCnewP", "index": i},
                                options=[
                                        {'label':'1st', 'value':'1st'},
                                        {'label':'2nd', 'value':'2nd'},
                                        {'label':'3rd', 'value':'3rd'},
                                        {'label':'4th', 'value':'4th'},
                                        {'label':'Booster', 'value':'Booster'},
                                ],
                                placeholder='Enter Dose',
                            ),
                            width = 2,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "vaccine_date_newCnewP", "index": i},
                                placeholder="Select Date Administered",
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                            ),
                            width = 3,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "vaccine_expdate_newCnewP", "index": i},
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

    elif triggered_id and 'vaccine-deletebutton_newCnewP' in triggered_id:
        if len(vaccine_lineitem_newCnewP) > 0:
            vaccine_lineitem_newCnewP.pop()
    
    else:
        raise PreventUpdate
    
    return [vaccine_lineitem_newCnewP]

deworm_lineitem_newCnewP = []

@app.callback( #callback for adding a row for deworm administered
    [
        Output('deworm-line-items_newCnewP', 'children'),
    ],
    [
        Input('deworm-addbutton_newCnewP', 'n_clicks'),
        Input('deworm-deletebutton_newCnewP', 'n_clicks'),
    ],
    [
        State('deworm-line-items_newCnewP', 'children'),
    ]
)

def manage_deworm_line_item(addclick, deleteclick, existing_items):

    deworm_lineitem_newCnewP = existing_items or []
    
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and 'deworm-addbutton_newCnewP' in triggered_id:
        if len(deworm_lineitem_newCnewP) < addclick:
            i = len(deworm_lineitem_newCnewP)
            deworm_lineitem_newCnewP.extend([
                html.Div([
                    html.Div(style={'height':'5px'}),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id={"type": "deworm_name_newCnewP", "index": i},
                                placeholder='Select Deworming Medication',
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                            width = 4,
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id={"type": "deworm_dose_newCnewP", "index": i},
                                options=[
                                        {'label':'1st', 'value':'1st'},
                                        {'label':'2nd', 'value':'2nd'},
                                        {'label':'3rd', 'value':'3rd'},
                                        {'label':'4th', 'value':'4th'},
                                        {'label':'Booster', 'value':'Booster'},
                                ],
                                placeholder='Enter Dose',
                            ),
                            width = 2,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "deworming_date_newCnewP", "index": i},
                                placeholder="Select Date Administered",
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                            ),
                            width = 3,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "deworming_medication_expdate_newCnewP", "index": i},
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

    elif triggered_id and 'deworm-deletebutton_newCnewP' in triggered_id:
        if len(deworm_lineitem_newCnewP) > 0:
            deworm_lineitem_newCnewP.pop()
    
    else:
        raise PreventUpdate
    
    return [deworm_lineitem_newCnewP]

clinical_exam_lineitem = []

@app.callback( #callback for adding clinical exam content
    [
        Output('clinical_exam_content_newCnewP', 'children'),
    ],
    [
        Input('clinicalexam-addbutton_newCnewP', 'n_clicks'),
        Input('clinicalexam-deletebutton_newCnewP', 'n_clicks'),
    ],
)

def manage_clinical_exam_content_newCnewP(addclick, deleteclick):
    ctx = dash.callback_context
 
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and 'clinicalexam-addbutton_newCnewP' in triggered_id:
        if len(clinical_exam_lineitem) < addclick:
            i = len(clinical_exam_lineitem)
            clinical_exam_lineitem.extend([
                html.Div(
                    [
                        dbc.Row([ # Clinical Exam 1st Clinician and Exam

                            dbc.Col([
                                    dbc.Label("Clinical Exam Type"),
                                    dcc.Dropdown(
                                        id={"type": "clinical_exam_list_newCnewP", "index": i},
                                        placeholder="Select Clinical Exam Type",
                                        searchable=True,
                                        options=[],
                                        value=None,
                                    ), 
                            ], width = 3), 

                            dbc.Col([
                                    dbc.Label("Clinical Exam Findings"),
                                    dbc.Textarea(
                                        id={"type": "newclinicalfindings_newCnewP", "index": i},
                                        placeholder="Enter Findings",
                                        style={'width':'100%', 'height':25}
                                    ),
                            ],width = 6), 
                            
                            dbc.Col([
                                    dbc.Label("Clinician"),
                                    dcc.Dropdown(
                                        id={"type": "clinician_list_newCnewP", "index": i},
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

    elif triggered_id and 'clinicalexam-deletebutton_newCnewP' in triggered_id:
        if len(clinical_exam_lineitem) > 0:
            clinical_exam_lineitem.pop()

    else:
        raise PreventUpdate
    
    return [clinical_exam_lineitem]

progress_notes_lineitem = []

@app.callback( #callback for adding clinical exam content
    [
        Output('progress_notes_content_newCnewP', 'children'),
    ],
    [
        Input('notes-addbutton_newCnewP', 'n_clicks'),
        Input('notes-deletebutton_newCnewP', 'n_clicks'),
    ],
)

def manage_notes_content(addclick, deleteclick):
    ctx = dash.callback_context
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id and 'notes-addbutton_newCnewP' in triggered_id:
        if len(progress_notes_lineitem) < addclick:
            i = len(progress_notes_lineitem)
            progress_notes_lineitem.extend([
                html.Div([
                    html.Hr(),
                    dbc.Row([ # Laboratory Result Add/Delete button
                        dbc.Col(html.H5("Add Laboratory Results:"), width=6),
                        dbc.Col(
                            [
                                dbc.Button("+", id='labresult-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                dbc.Button("-", id='labresult-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                            ],
                            width = 'auto',
                            className = 'text-right'
                        ),
                    ], justify = 'between'),
                    html.Div(id='labresult-lineitems'),

                    html.Br(),

                    dbc.Row([ #under progress notes
                        dbc.Col([
                            dbc.Label("Differential Diagnosis"),
                            dbc.Textarea(
                                id={"type": "newdifferentialdiagnosis_newCnewP", "index": i},
                                placeholder="Enter Differential Diagnosis",
                                style={'width':'100%', 'height':100}
                            ),
                        ]),
                        dbc.Col([
                            dbc.Label("Possible Treatment"),
                            dbc.Textarea(
                                id={"type": "newpossibletreatment_newCnewP", "index": i},
                                placeholder="Enter Treatment Options",
                                style={'width':'100%', 'height':100}
                            ),
                        ]),
                        dbc.Col([
                            dbc.Row([
                                dbc.Label("OR Number"),
                                dbc.Textarea(
                                id={"type": "newornumber_newCnewP", "index": i},
                                placeholder="Enter OR No.",
                                style={'width':'100%', 'height':25}
                                ),
                            ]),
                            dbc.Row([
                                dbc.Label("Bill"),
                                dbc.Textarea(
                                id={"type": "newbill_newCnewP", "index": i},
                                placeholder="Enter Bill Amount",
                                style={'width':'100%', 'height':25}
                                ),
                            ]),
                        ], width=3)
                    ]),

                    html.Br(),

                    dbc.Row([ # Request Laboratory Examination
                        dbc.Col(html.H5("Request Laboratory Examination:"), width=6),
                        dbc.Col(
                            [
                                dbc.Button("+", id='labexamresult-addbutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'margin-right': '5px', 'border-radius': '5px'}),
                                dbc.Button("-", id='labexamrestul-deletebutton_newCnewP', className='custom-button', n_clicks=0, style={'width': '35px', 'height': '35px', 'border-radius': '5px'}),
                            ],
                            width = 'auto',
                            className = 'text-right'
                        ),
                    ], justify = 'between'),
                    html.Div(id='labexam-lineitems_newCnewP'),
                    html.Br(),
                ])
            ])

    elif triggered_id and 'notes-deletebutton_newCnewP' in triggered_id:
        if len(progress_notes_lineitem) > 0:
            progress_notes_lineitem.pop()

    else:
        raise PreventUpdate
    
    return [progress_notes_lineitem]

lab_result_lineitem = []

@app.callback( #callback for adding lab result content
    [
        Output('labresult_lineitems_newCnewP', 'children'),
    ],
    [
        Input('labresult-addbutton_newCnewP', 'n_clicks'),
        Input('labresult-deletebutton_newCnewP', 'n_clicks'),
    ],
    [
        State('labresult_lineitems_newCnewP', 'children'),
    ],
)

def manage_labresult_content(addclick, deleteclick, existing_items):
    
    lab_result_lineitem = existing_items or []
    
    ctx = dash.callback_context
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id and 'labresult-addbutton_newCnewP' in triggered_id:
        if len(lab_result_lineitem) < addclick:
            i = len(lab_result_lineitem)
            lab_result_lineitem.extend([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Lab Exam Type"),
                            dcc.Dropdown(
                            id={"type": "lab_exam_list_newCnewP", "index": i},
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
                                    id="newnote_havebeentested_newCnewP",
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
                                id={"type": "veterinarian_list_newCnewP", "index": i},
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
                                    id={"type": "Labexamfindings_newCnewP", "index": 1},
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
    elif triggered_id and 'labresult-deletebutton_newCnewP' in triggered_id:
        if len(lab_result_lineitem) > 0:
            lab_result_lineitem.pop()
    else:
        raise PreventUpdate
    return [lab_result_lineitem]

lab_request_lineitem = []

@app.callback( #callback for adding lab request content
    [
        Output('labreq_lineitems_newCnewP', 'children'),
    ],
    [
        Input('labreq-addbutton_newCnewP', 'n_clicks'),
        Input('labreq-deletebutton_newCnewP', 'n_clicks'),
    ],
)

def manage_labreq_content(addclick, deleteclick):
    ctx = dash.callback_context
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id and 'labreq-addbutton_newCnewP' in triggered_id:
        if len(lab_request_lineitem) < addclick:
            i = len(lab_request_lineitem)
            lab_request_lineitem.extend([
                html.Div([
                    dbc.Row([
                        dbc.Col(
                            [
                                dbc.Label("Laboratory Exam and Notes"),
                                dbc.Textarea(
                                    id={"type": "Labexamfindings_newCnewP", "index": 1},
                                    placeholder="Enter Laboratory Examination Request and Notes needed",
                                    style={'width':'100%', 'height':25}
                                ),
                            ],
                            width = 12
                        ), 
                    ]),
                ])
            ])
    elif triggered_id and 'labreq-deletebutton_newCnewP' in triggered_id:
        if len(lab_request_lineitem) > 0:
            lab_request_lineitem.pop()
    else:
        raise PreventUpdate
    return [lab_request_lineitem]



#FUNCTIONAL CALLBACKS

@app.callback( #callback for list of problem status
    [
        Output('problem_status_newCnewP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('problem_status_newCnewP', 'value'),
    ]
)
def problemstatuslist(pathname, searchterm):
    if pathname == "/home_newCnewP"  and not searchterm:
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


@app.callback( #callback for list of existing clients for returning patient
    [
        Output('re_clientlist_newCnewP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('re_clientlist_newCnewP', 'value'),
    ]
)
def re_clientlist_newCnewP(pathname, searchterm):
    if pathname == "/home_newCnewP"  and not searchterm:
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

#newCnewP
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
    if pathname == "/home_newCnewP"  and not searchterm:
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
        Output('patientlist_newCnewP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('re_clientlist_newCnewP', 'value'),
        Input('patientlist_newCnewP', 'value'),
    ]
)
def patientlist_newCnewP(pathname, selected_client_id, searchterm):
    if pathname == "/home_newCnewP" and not searchterm:
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

@app.callback( #list of problems
    [
        Output('problem_list_newCnewP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('patientlist_newCnewP', 'value'),
        Input('problem_list_newCnewP', 'value'),
    ]
)

def problem_list_newCnewP(pathname, selected_patient_id,searchterm):
    if pathname == "/home_newCnewP"  and not searchterm:
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
     
@app.callback(#list of veterinarians for fixed card
    [
        Output("vetlist_newCnewP", 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input("vetlist_newCnewP", 'value'),
    ]
)
def vetlist_newCnewP(pathname, searchterm):
    if pathname == "/home_newCnewP" and not searchterm:
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

@app.callback(#list of veterinarians for variable card
    [
        Output({"type": "veterinarian_list_newCnewP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "veterinarian_list_newCnewP", "index": MATCH}, 'value'),
    ]
)
def vetlist_newCnewP(pathname, searchterm):
    if pathname == "/home_newCnewP" and not searchterm:
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
        Output("vaccine_name_newCnewP", "options"),
    ],
    [
        Input('url', 'pathname'),
        Input("vaccine_name_newCnewP", "value"),
    ]
)
def vaccinelistfixed(pathname, searchterm):
    if pathname == "/home_newCnewP" and not searchterm:
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
        Output("deworm_name_newCnewP", 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input("deworm_name_newCnewP", 'value'),
    ]
)
def dewormlistfixed(pathname, searchterm):
    if pathname == "/home_newCnewP" and not searchterm:
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
        Output({"type": "vaccine_name_newCnewP", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "vaccine_name_newCnewP", "index": MATCH}, "value"),
    ]
)
def vaccinelistvariable(pathname, searchterm):
    if pathname == "/home_newCnewP" and not searchterm:
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
        Output({"type": "deworm_name_newCnewP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "deworm_name_newCnewP", "index": MATCH}, 'value'),
    ]
)
def dewormlistvariable(pathname, searchterm):
    if pathname == "/home_newCnewP" and not searchterm:
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
        Output('clinical_exam_list_newCnewP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('clinical_exam_list_newCnewP', 'value'),
    ]
)
def clinicalexamlistfixed(pathname, searchterm):
    if pathname == "/home_newCnewP"  and not searchterm:
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
        Output({"type": "clinical_exam_list_newCnewP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "clinical_exam_list_newCnewP", "index": MATCH}, 'value'),
    ]
)
def clinicalexamlistvariable(pathname, searchterm):
    if pathname == "/home_newCnewP"  and not searchterm:
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
        Output('clinician_list_newCnewP', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('clinician_list_newCnewP', 'value'),
    ]
)
def clinicianlistfixed(pathname, searchterm):
    if pathname == "/home_newCnewP"  and not searchterm:
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
        Output({"type": "clinician_list_newCnewP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "clinician_list_newCnewP", "index": MATCH}, 'value'),
    ]
)
def clinicianlistfixed(pathname, searchterm):
    if pathname == "/home_newCnewP"  and not searchterm:
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
        Output({"type": "lab_exam_list_newCnewP", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "lab_exam_list_newCnewP", "index": MATCH}, 'value'),
    ]
)
def labexamlistvariable(pathname, searchterm):
    if pathname == "/home_newCnewP"  and not searchterm:
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


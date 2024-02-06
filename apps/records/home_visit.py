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
        dbc.Alert(id = 'visitrecord_alert', is_open = False),
        dbc.Card( # Main Visits Info
            [
                dbc.CardHeader(
                    html.Div([
                            html.H2("Record Visits", className = "flex-grow-1"),
#                            html.Div([
#                                dbc.Button("Returning Patient", href= '/home_visit',className = "me-2",n_clicks = 0),
#                                dbc.Button("New Patient", href= '/home_reCnewP',n_clicks = 0),
#                            ], className = "ml-2 d-flex")
                        ], #className = "d-flex align-items-center justify-content-between"
                    )
                ),

                dbc.CardBody([
                    dbc.Row([ #Select Client
                        
                        dbc.Col(html.H4("Select Client"), width = 3),

                        dbc.Col(
                            dcc.Dropdown(
                                id = "re_clientlist",
                                placeholder = "Search Client",
                                searchable = True,
                                options = [],
                                value = None,
                            ), width = 4),
                        
                        dbc.Col(html.H6("Client not listed?", style={"text-align": "right"}), width = 2),

                        dbc.Col(
                            dbc.Button(
                                "Create Client Profile",
                                id = "create_client_profile",
                                style={"width":"100%"},
                            ), width = 3), 

                    ], style={"margin-left": "2%", "margin-right": "1%", "align-items": "center"}),
                    
                    html.Br(),

                    dbc.Row([ #Select Patient
                        
                        dbc.Col(html.H4("Select Patient"), width = 3),
                        
                        dbc.Col(
                            dcc.Dropdown(
                                id = "patientlist",
                                placeholder="Search Patient",
                                searchable=True,
                                options=[],
                                value=None,
                            ), width = 4),
                        
                        dbc.Col(html.H6("Patient not listed?", style={"text-align": "right"}), width = 2),

                        dbc.Col(
                            dbc.Button(
                                "Create Patient Profile",
                                id = "create_patient_profile",
                                style={"width":"100%"},
                            ), width = 3), 

                    ], style={"margin-left": "2%", "margin-right": "1%", "align-items": "center"}),
                    
                    html.Br(),

                    dbc.Row([ #Select Veterinarian
                            
                        dbc.Col(html.H4("Assign Veterinarian"), width=3),

                        dbc.Col(
                            dcc.Dropdown(
                                id="vetlist",
                                placeholder="Select Veterinarian",
                                searchable=True,
                                options=[],
                                value=None,
                            ),width = 4),
                        
                        dbc.Col(html.H6("Vet not listed?", style={"text-align": "right"}), width = 2),

                        dbc.Col(
                            dbc.Button(
                                "Create Veterinarian Profile",
                                id = "create_vet_profile",
                                style={"width":"100%"},
                            ), width = 3), 

                    ], style={"margin-left": "2%", "margin-right": "1%", "align-items": "center"}),

                    html.Br(),
                    
                    dbc.Row([ #Visit purpose and Visit Date
                        dbc.Col(html.H4("Visit Purpose"), width=3),
                        dbc.Col(
                            dbc.Checklist(
                                options=[
                                    {"label": "New Problem", "style": {"flex-grow": 1}, "value": "new_problem"},
                                    {"label": "Follow up to a Problem", "style": {"flex-grow": 1}, "value": "follow_up"},
                                ],
                                id="visitpurpose_problem",
                                inline=True,
                                style={
                                    "display": "flex",
                                    "flex-direction": "column",
                                    "justify-content": "flex-start",
                                    "fontSize": "1rem",
                                    "align-items": "flex-start",
                                },
                            ),
                            width=3, style={"margin-right": "-15px"}
                        ),
                        dbc.Col(
                            dbc.Checklist(
                                options=[
                                    {"label": "Vaccination", "style": {"flex-grow": 1}, "value": "vaccination"},
                                    {"label": "Deworming", "style": {"flex-grow": 1}, "value": "deworming"},
                                ],
                                id="visitpurpose",
                                inline=True,
                                style={
                                    "display": "flex",
                                    "flex-direction": "column",
                                    "justify-content": "flex-start",
                                    "fontSize": "1rem",
                                    "align-items": "flex-start",
                                },
                            ),
                            width=1, style={"margin-left": "-15px", "margin-right": "30px"}
                        ),
                        dbc.Col(html.H4("Visit Date", style={"text-align": "right"}), width = 2),
                        dbc.Col(
                            dmc.DatePicker(
                            id='visitdate',
                            placeholder="Select Visit Date",
                            value=datetime.now().date(),
                            inputFormat='MMM DD, YYYY',
                            dropdownType='modal',
                            ), width=3
                        ),
                    ], style={"margin-left": "2%", "margin-right": "1%", "align-items": "center"}),

                    html.Div([ #Previous Problem Extension
                        html.Br(),
                        dbc.Row([
                            dbc.Col(html.H4("Previous problem:"), width=3),
                            dbc.Col(
                                dcc.Dropdown(
                                    id="problem_list",
                                    placeholder="Search patient's past problems",
                                    searchable=True,
                                    options=[],
                                    value=None,
                                ),
                            ),                    
                        ], style={"margin-left": "2%", "margin-right": "1%", "align-items": "center"}),
                    ],id = 'follow_up_field', style = {'display': 'none'}),

                ]),
                
            ]),
            

        html.Br(),
        dbc.Button( #Submit button
                    'Submit',
                    id = 'visitrecord_submit',
                    n_clicks = 0, #initialization 
                    className='custom-submitbutton',
                ),
        #modal for successful saving of visit
        dbc.Modal(children = [ 
            dbc.ModalHeader(html.H4('Visit Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                dbc.Button("Proceed to Visit Details", href = "/home_visit/purpose", className = "ms-auto"),
            ]),
        ],centered = True, id = 'visitrecord_successmodal', backdrop = 'static', is_open = False, keyboard = False),
        
        # modal for creating client profile
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Create Client Profile", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "client_profile_alert", is_open = False),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("First Name", style={"width": "17%"}),
                        dbc.Input(id='new_client_fn', type='text', placeholder="e.g. Juan"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Last Name", style={"width": "17%"}),
                        dbc.Input(id='new_client_ln', type='text', placeholder="e.g. Dela Cruz"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Middle Initial", style={"width": "17%"}),
                        dbc.Input(id='new_client_mi', type='text', placeholder="e.g. M."),
                        dbc.InputGroupText("Suffix", style={"width": "12%"}),
                        dbc.Input(id='new_client_suffix', type='text', placeholder="e.g. Jr."),
                    ],
                    className="mb-4",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Contact No.", style={"width": "17%"}),
                        dbc.Input(id='new_client_contact_no', type='text', placeholder="e.g. 09123456789"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Email", style={"width": "17%"}),
                        dbc.Input(id='new_client_email', type='text', placeholder="e.g. Juan.DelaCruz@example.com"),
                    ],
                    className="mb-4",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("House No.", style={"width": "17%"}),
                        dbc.Input(id='new_client_house_no', type='text', placeholder="e.g. No. 1A (or any landmark)"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Street", style={"width": "17%"}),
                        dbc.Input(id='new_client_street', type='text', placeholder="e.g. P. Vargas St."),
                        dbc.InputGroupText("Barangay", style={"width": "12%"}),
                        dbc.Input(id='new_client_barangay', type='text', placeholder="e.g. Krus na Ligas"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("City", style={"width": "17%"}),
                        dbc.Input(id='new_client_city', type='text', placeholder="e.g. Pasay City"),
                        dbc.InputGroupText("Region", style={"width": "12%"}),
                        dbc.Input(id='new_client_region', type='text', placeholder="e.g. Metro Manila"),
                    ],
                    #className="mb-3",
                ),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Client Details", href = "/home_visit", id = "client_profile_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "client_profile_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of client profile
            dbc.ModalHeader(html.H4('Client Profile Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                html.A(html.Button("Close", id = 'close_client_successmodal', className = "btn btn-primary ms-auto"),href = '/home_visit'),
                #dbc.Button("Close", href = "/", id = "close_client_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'client_profile_successmodal', backdrop = 'static', is_open = False, keyboard = False),

        # modal for creating patient profile
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Create Patient Profile", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "patient_profile_alert", is_open = False),
                
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Client", style={"width": "17%"}),                            
                        dbc.InputGroupText(dcc.Dropdown(
                                id = "new_clientlist",
                                placeholder = "Search Patient's Owner",
                                searchable = True,
                                options = [],
                                value = None,
                                style = {"width": "100%"}
                            ), style = {"width": "83%"}
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Name", style={"width": "17%"}),
                        dbc.Input(id='new_patient_m', type='text', placeholder="e.g. Bantay (leave blank if none)"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Species", style={"width": "17%"}),
                        dbc.Input(id='new_patient_species', type='text', placeholder="e.g. Dog"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Breed", style={"width": "17%"}),
                        dbc.Input(id='new_patient_breed', type='text', placeholder="e.g. Bulldog"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Color Marks", style={"width": "17%"}),
                        dbc.Input(id='new_patient_color', type='text', placeholder="e.g. White or With black spots"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Sex", style={"width": "17%"}),                            
                        dbc.InputGroupText(dcc.Dropdown(
                            id='new_patient_sex',
                            options=[
                                {'label':'Male', 'value':'Male'},
                                {'label':'Female', 'value':'Female'},
                            ],
                            placeholder='Select Sex',
                            style = {"width": "100%"}
                            ), style = {"width": "43%"}
                        ),
                        dbc.InputGroupText("Birth Date", style={"width": "19%"}),
                        dbc.InputGroupText(dcc.DatePickerSingle(
                            id='new_patient_bd',
                            date=None,
                            display_format='MMM DD, YYYY',
                            placeholder = "Choose Date"
                            ),
                        ),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Idiosyncrasies", style={"width": "17%"}),
                        dbc.Input(id='new_patient_idiosync', type='text', placeholder="e.g. Likes morning walks"),
                    ],
                    #className="mb-3",
                ),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Patient Details", id = "patient_profile_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "patient_profile_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of patient profile
            dbc.ModalHeader(html.H4('Patient Profile Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                html.A(html.Button("Close", id = 'close_patient_successmodal', className = "btn btn-primary ms-auto"),href = '/home_visit'),
                #dbc.Button("Close", id = "close_patient_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'patient_profile_successmodal', backdrop = 'static', is_open = False, keyboard = False),

        # modal for creating vet user profile
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Create Veterinarian User Profile", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "vet_profile_alert", is_open = False),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("First Name", style={"width": "20%"}),
                        dbc.Input(id='new_vet_fn', type='text', placeholder="e.g. Peter"),
                    ],
                    className="mb-2",
                ),
                
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Last Name", style={"width": "20%"}),
                        dbc.Input(id='new_vet_ln', type='text', placeholder="e.g. Dimagiba"),
                    ],
                    className="mb-2",
                ),


                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Middle Initial", style={"width": "20%"}),
                        dbc.Input(id='new_vet_mi', type='text', placeholder="e.g. K"),
                        dbc.InputGroupText("Suffix", style={"width": "9%"}),
                        dbc.Input(id='new_vet_suffix', type='text', placeholder="e.g. III"),
                    ],
                    className="mb-4",
                ),
                
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Contact Number", style={"width": "20%"}),
                        dbc.Input(id='new_vet_cn', type='text', placeholder="e.g. 09123456789"),
                    ],
                    className="mb-2",
                ),


                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Email (Username)", style={"width": "20%"}),
                        dbc.Input(type="text", id="new_vet_email", placeholder="e.g.PKDimagiba@example.com"),
                    ],
                    className="mb-4",
                ),
                
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Password", style={"width": "20%"}),
                        dbc.Input(type="password", id="new_vet_password", placeholder="Enter a password"),
                    ],
                    className="mb-2",
                ),
                
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Confirm Password", style={"width": "20%"}),
                        dbc.Input(type="password", id="new_vet_passwordconf", placeholder="Re-type the password"),
                    ],
                    className="mb-2",
                ),


            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Vet User Details", id = "vet_profile_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "vet_profile_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of vet profile
            dbc.ModalHeader(html.H4('Vet User Profile Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                html.A(html.Button("Close", id = 'close_vet_successmodal', className = "btn btn-primary ms-auto"),href = '/home_visit'),
                #dbc.Button("Close", id = "close_vet_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'vet_profile_successmodal', backdrop = 'static', is_open = False, keyboard = False),

        # modal for creating new problem profile
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Enter New Problem Details", style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalBody([
                dbc.Alert(id = "new_problem_alert", is_open = False),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Problem", style={"width": "23%"}),
                        dbc.Input(id='newproblem', type='text', placeholder="Describe the overall problem"),
                    ],
                    className="mb-4",
                ),
                html.H4("Health & Nutrients Intake", className="mb-2"),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Medical History", style={"width": "23%"}),
                        dbc.InputGroupText(dbc.Textarea(id='newproblem_medhistory', placeholder='Enter any relevant medical history', style={"height":30, 'width':'100%'}), style={"width": "77%"})
                    ],
                    className="mb-2",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Diet", style={"width": "23%"}),
                        dbc.Input(id='newproblem_diet', type='text', placeholder="Enter patient's general diet"),
                    ],
                    className="mb-2",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Water Source", style={"width": "23%"}),
                        dbc.Input(id='newproblem_watersource', type='text', placeholder="Enter patient's general source of hydration"),
                    ],
                    className="mb-4",
                ),
                html.H4("Health Assessment", className="mb-2"),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Temperature", style={"width": "23%"}),
                        dbc.Input(id='newproblem_temp', type='text', placeholder="Enter most recent temperature in °C"),
                    ],
                    className="mb-2",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Pulse Rate", style={"width": "23%"}),
                        dbc.Input(id='newproblem_pr', type='text', placeholder="Enter pulse rate per min"),
                    ],
                    className="mb-2",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Weight", style={"width": "23%"}),
                        dbc.Input(id='newproblem_weight', type='text', placeholder="Enter weight in kilogram"),
                    ],
                    className="mb-2",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Respiration Rate", style={"width": "23%"}),
                        dbc.Input(id='newproblem_rr', type='text', placeholder="Enter respiration rate per min"),
                    ],
                    className="mb-2",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Body Condition Score", style={"width": "23%"}),
                        dbc.Input(id='newproblem_bodyscore', type='text', placeholder="Enter patient's condition score (1-9)"),
                    ],
                    #className="mb-2",
                ),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Problem Details", id = "problem_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "new_problem_modal", is_open = False, backdrop = "static", size = 'lg', keyboard = False),
    ])


# MODAL CALLBACKS

@app.callback( #opens and close form and success modal for creating client profile
        [
            Output("client_profile_modal", "is_open"),
            Output('client_profile_successmodal', 'is_open'),
        ],
        [
            Input("create_client_profile", "n_clicks"),
            Input('client_profile_submit','n_clicks'),
            Input('close_client_successmodal','n_clicks'),
        ],
        [
            State("client_profile_modal", "is_open"),
            State('client_profile_successmodal', 'is_open'),
            State('new_client_fn', 'value'),
            State('new_client_ln', 'value'),
            State('new_client_contact_no', 'value'),
            State('new_client_email', 'value'),
            State('new_client_street', 'value'),
            State('new_client_barangay', 'value'),
            State('new_client_city', 'value'),
            State('new_client_region', 'value'),
        ]
)
def toggle_client_profile_modal(create, submit, close, form, success, fn, ln, cn, email, street, brgy, city, region):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "create_client_profile" and create:
            return [not form, success]
        
        if eventid == 'client_profile_submit' and submit and all([fn, ln, cn, email, street, brgy, city, region]):
            return [not form, not success]
        
        if eventid == 'close_client_successmodal' and close:
            return [form, not success]
        
    return [form, success]

@app.callback( #opens and close form and success modal for creating patient profile
        [
            Output("patient_profile_modal", "is_open"),
            Output('patient_profile_successmodal', 'is_open'),
        ],
        [
            Input("create_patient_profile", "n_clicks"),
            Input('patient_profile_submit','n_clicks'),
            Input('close_patient_successmodal','n_clicks'),
        ],
        [
            State("patient_profile_modal", "is_open"),
            State('patient_profile_successmodal', 'is_open'),
            State('new_patient_species', 'value'),
            State('new_patient_breed', 'value'),
            State('new_patient_color', 'value'),
            State('new_patient_sex', 'value'),
            State('new_patient_bd', 'date'),
            State('new_patient_idiosync', 'value'),
            State('new_clientlist', 'value'),
        ]
)
def toggle_patient_profile_modal(create, submit, close, form, success, species, breed, color, sex, bd, idiosync, client):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "create_patient_profile" and create:
            return [not form, success]
        
        if eventid == "patient_profile_submit" and submit and all([species, color, breed, sex, bd, idiosync, client]):
            return [not form, not success]
        
        if eventid == "close_patient_successmodal" and close:
            return [form, not success]
           
    return [form, success]

@app.callback( #opens and close form and success modal for creating vet user profile
        [
            Output("vet_profile_modal", "is_open"),
            Output('vet_profile_successmodal', 'is_open'),
        ],
        [
            Input("create_vet_profile", "n_clicks"),
            Input('vet_profile_submit','n_clicks'),
            Input('close_vet_successmodal','n_clicks'),
        ],
        [
            State("vet_profile_modal", "is_open"),
            State('vet_profile_successmodal', 'is_open'),
            State('new_vet_fn', 'value'),
            State('new_vet_ln', 'value'),
            State('new_vet_cn', 'value'),
            State('new_vet_email', 'value'),
            State('new_vet_password', 'value'),
            State('new_vet_passwordconf', 'value'),
        ]
)
def toggle_vet_profile_modal(create, submit, close, form, success, fn, ln, cn, email, pw, pwconf):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "create_vet_profile" and create:
            return [not form, success]
        
        if eventid == "vet_profile_submit" and submit and all([ln, fn, email, cn, pw, pwconf]) and pw ==pwconf:
            return [not form, not success]
        
        if eventid == "close_vet_successmodal" and close:
            return [form, not success]
        
    return [form, success] 

@app.callback( #opens and close form modal for creating new problem a d visit success modal
    [
        Output('visitrecord_successmodal','is_open'),
        Output("new_problem_modal", "is_open"),
    ],
    [
        Input('visitrecord_submit','n_clicks'),
        Input('problem_submit','n_clicks'),
    ],
    [
        State('visitrecord_successmodal','is_open'),
        State("new_problem_modal", "is_open"),
        State('re_clientlist', 'value'),
        State('patientlist','value'),
        State('vetlist','value'),
        State('visitdate', 'value'),
        State('problem_list', 'value'),
        State('visitpurpose', 'value'),
        State('visitpurpose_problem', 'value'),
        State('newproblem', 'value'),
        State('newproblem_medhistory', 'value'),
        State('newproblem_diet', 'value'),
        State('newproblem_watersource', 'value'),
        State('newproblem_temp', 'value'),
        State('newproblem_pr', 'value'),
        State('newproblem_weight', 'value'),
        State('newproblem_rr', 'value'),
        State('newproblem_bodyscore', 'value'),
    ]
)
def toggle_new_problem_modal(visit_btn, problem_btn, visit_success, problem_modal, client, patient, vet, date, prev_prob, vacc_deworm, prob, problem, hist, diet, water, temp, pr, weight, rr, bodyscore):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if vacc_deworm is None:
            vacc_deworm_purpose = []
        else:
            vacc_deworm_purpose = vacc_deworm

        if prob is None:
            prob_purpose = []
        else:
            prob_purpose = prob

        visit_for_vacc = 'vaccination' in vacc_deworm_purpose
        visit_for_deworm = 'deworming' in vacc_deworm_purpose
        new_problem = 'new_problem' in prob_purpose
        follow_up = 'follow_up' in prob_purpose
        follow_and_problem = follow_up == any([prev_prob])
        visit_for_problem = len(prob_purpose) == 1

        if eventid == "visitrecord_submit" and visit_btn and all([client, patient, vet, date, follow_and_problem, any([visit_for_problem, visit_for_deworm, visit_for_vacc])]):
            if new_problem:
                return [visit_success, not problem_modal]
            else:
                return [not visit_success, problem_modal]
            
        if eventid == "problem_submit" and problem_btn and all([problem, hist, diet, water, temp, pr, rr, weight, bodyscore]):
            return [not visit_success, not problem_modal]

    return [visit_success, problem_modal]



#SAVE AND SUBMIT CALLBACKS

@app.callback( # Submit Button for visit
    [
        Output('visitrecord_alert','color'),
        Output('visitrecord_alert','children'),
        Output('visitrecord_alert','is_open'),
        Output('re_clientlist', 'value'),
        Output('patientlist','value'),
        Output('vetlist','value'),
        Output('visitdate', 'value'),
        Output('problem_list', 'value'),
    ],
    [
        Input('visitrecord_submit','n_clicks'),
        Input('re_clientlist', 'value'),
        Input('patientlist','value'),
        Input('vetlist','value'),
        Input('visitdate', 'value'),
    ],
    [
        State('problem_list', 'value'),
        State('visitpurpose', 'value'),
        State('visitpurpose_problem', 'value')
    ]
)
def visitrecord_save(submitbtn, client, patient, vet, date, prev_prob, vacc_deworm, prob):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        alert_open = False
        alert_color = ''
        alert_text = ''

        if vacc_deworm is None:
            vacc_deworm_purpose = []
        else:
            vacc_deworm_purpose = vacc_deworm

        if prob is None:
            prob_purpose = []
        else:
            prob_purpose = prob
        
        if eventid == 'visitrecord_submit' and submitbtn:

            visit_for_vacc = 'vaccination' in vacc_deworm_purpose
            visit_for_deworm = 'deworming' in vacc_deworm_purpose
            follow_up = 'follow_up' in prob_purpose
            follow_and_problem = follow_up == any([prev_prob])
            visit_for_problem = len(prob_purpose) == 1
   
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
            elif not any([visit_for_problem, visit_for_deworm, visit_for_vacc]):
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please choose the purpose of visit (can be more than one)'
            elif not date:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please select the date of visit'
            elif not follow_and_problem:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please select the previous problem for this follow-up visit'
            else:
                sql = '''
                INSERT INTO visit(
                                patient_id,
                                vet_id,
                                visit_for_vacc,
                                visit_for_deworm,
                                visit_for_problem,
                                problem_id,
                                visit_delete_ind
                            )
                            VALUES(%s, %s, %s, %s, %s, %s, %s)
                    '''
                values = [patient, vet, visit_for_vacc, visit_for_deworm, visit_for_problem, prev_prob, False]

                db.modifydatabase(sql, values)
            
            if not all([client, patient, vet, date, follow_and_problem, any([visit_for_problem, visit_for_deworm, visit_for_vacc])]):
                return [alert_color, alert_text, alert_open, client, patient, vet, date, prev_prob]

            return [alert_color, alert_text, alert_open, None, None, None, datetime.now().date(), None]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback( # Submit Button for client profile
        [
            Output('client_profile_alert', 'color'),
            Output('client_profile_alert', 'children'),
            Output('client_profile_alert', 'is_open'),
            Output('new_client_fn', 'value'),
            Output('new_client_ln', 'value'),
            Output('new_client_mi', 'value'),
            Output('new_client_suffix', 'value'),
            Output('new_client_contact_no', 'value'),
            Output('new_client_email', 'value'),
            Output('new_client_house_no', 'value'),
            Output('new_client_street', 'value'),
            Output('new_client_barangay', 'value'),
            Output('new_client_city', 'value'),
            Output('new_client_region', 'value'),
        ],
        [
            Input('client_profile_submit', 'n_clicks'),
            Input('new_client_fn', 'value'),
            Input('new_client_ln', 'value'),
            Input('new_client_mi', 'value'),
            Input('new_client_suffix', 'value'),
            Input('new_client_contact_no', 'value'),
            Input('new_client_email', 'value'),
            Input('new_client_house_no', 'value'),
            Input('new_client_street', 'value'),
            Input('new_client_barangay', 'value'),
            Input('new_client_city', 'value'),
            Input('new_client_region', 'value'),
        ],
)
def client_profile_save(submitbtn, fn, ln, mi, sf, cn, email, house_no, street, brgy, city, region):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        alert_open = False
        alert_color = ''
        alert_text = ''

        if eventid == 'client_profile_submit' and submitbtn:

            if not fn:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter client's first name"
            elif not ln:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter client's last name"
            elif not cn:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter client's contact number"
            elif not email:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter client's email address"
            elif not street:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter client's street address"
            elif not brgy:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter client's barangay"
            elif not city:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter the city of client's address"
            elif not region:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter the region of client's address"
            else:
                sql = '''
                INSERT INTO client(
                                client_ln,
                                client_fn,
                                client_mi,
                                client_suffix,
                                client_email,
                                client_cn,
                                client_house_no,
                                client_street,
                                client_barangay,
                                client_city,
                                client_region,
                                client_delete_ind
                            )
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                values = [ln, fn, mi, sf, email, cn, house_no, street, brgy, city, region, False]

                db.modifydatabase(sql, values)

            if not all([fn, ln, cn, email, street, brgy, city, region]):
                return [alert_color, alert_text, alert_open, fn, ln, mi, sf, cn, email, house_no, street, brgy, city, region]

            return [alert_color, alert_text, alert_open, None, None, None, None, None, None, None, None, None, None, None]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback( # Submit Button for patient profile
        [
            Output('patient_profile_alert', 'color'),
            Output('patient_profile_alert', 'children'),
            Output('patient_profile_alert', 'is_open'),
            Output('new_clientlist', 'value'),
            Output('new_patient_m', 'value'),
            Output('new_patient_species', 'value'),
            Output('new_patient_breed', 'value'),
            Output('new_patient_color', 'value'),
            Output('new_patient_sex', 'value'),
            Output('new_patient_bd', 'date'),
            Output('new_patient_idiosync', 'value'),
        ],
        [
            Input('patient_profile_submit', 'n_clicks'),
            Input('new_clientlist', 'value'),
            Input('new_patient_m', 'value'),
            Input('new_patient_species', 'value'),
            Input('new_patient_breed', 'value'),
            Input('new_patient_color', 'value'),
            Input('new_patient_sex', 'value'),
            Input('new_patient_bd', 'date'),
            Input('new_patient_idiosync', 'value'),
        ]
)
def patient_profile_save(submitbtn, client, name, species, breed, color, sex, bd, idiosync):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        alert_open = False
        alert_color = ''
        alert_text = ''

        if eventid == 'patient_profile_submit' and submitbtn:

            if not client:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please search the owner of the patient'
            elif not species:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please indicate the species of the patient'
            elif not breed:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please indicate the breed of the patient'
            elif not color:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please describe the color or any color marks on the patient'
            elif not sex:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please indicate the sex of the patient'
            elif not bd:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please enter the birth date of the patient'
            elif not idiosync:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please describe any behavior or characteristic of the patient'
            else:
                sql = '''
                INSERT INTO patient(
                                patient_m,
                                patient_species,
                                patient_color,
                                patient_breed,
                                patient_sex,
                                patient_bd,
                                patient_idiosync,
                                patient_delete_ind,
                                client_id
                            )
                            VALUES(COALESCE(%s, 'N/A'), %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                values = [name, species, color, breed, sex, bd, idiosync, False, client]

                db.modifydatabase(sql, values)

            if not all([species, color, breed, sex, bd, idiosync, client]):
                return [alert_color, alert_text, alert_open, client, name, species, breed, color, sex, bd, idiosync]
            
            return [alert_color, alert_text, alert_open, None, None, None, None, None, None, None, None]
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback( # Submit Button for vet profile
        [
            Output('vet_profile_alert', 'color'),
            Output('vet_profile_alert', 'children'),
            Output('vet_profile_alert', 'is_open'),
            Output('new_vet_fn', 'value'),
            Output('new_vet_ln', 'value'),
            Output('new_vet_mi', 'value'),
            Output('new_vet_suffix', 'value'),
            Output('new_vet_cn', 'value'),
            Output('new_vet_email', 'value'),
            Output('new_vet_password', 'value'),
            Output('new_vet_passwordconf', 'value'),
        ],
        [
            Input('vet_profile_submit', 'n_clicks'),
            Input('new_vet_fn', 'value'),
            Input('new_vet_ln', 'value'),
            Input('new_vet_mi', 'value'),
            Input('new_vet_suffix', 'value'),
            Input('new_vet_cn', 'value'),
            Input('new_vet_email', 'value'),
            Input('new_vet_password', 'value'),
            Input('new_vet_passwordconf', 'value'),
        ]
)
def vet_profile_save(submitbtn, fn, ln, mi, suffix, cn, email, pw, pwconf):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        alert_open = False
        alert_color = ''
        alert_text = ''

        if eventid == 'vet_profile_submit' and submitbtn:

            if not fn:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter vet's first name"
            elif not ln:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter vet's last name"
            elif not cn:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter vet's contact number"
            elif not email:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter vet's email address"
            elif not pw:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter a password for user's login"
            elif not pwconf:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please confirm password"
            elif pw != pwconf:
                pwconf = None
                alert_open = True
                alert_color = 'danger'
                alert_text = "Password doesn't match"
            else:
                sql = '''
                INSERT INTO vet(
                                vet_ln,
                                vet_fn,
                                vet_mi,
                                vet_suffix,
                                vet_email,
                                vet_cn,
                                vet_user_pw,
                                vet_delete_ind
                            )
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                values = [ln, fn, mi, suffix, email, cn, pwconf, False]

                db.modifydatabase(sql, values)

            if not all([ln, fn, email, cn, pw, pwconf]):
                return [alert_color, alert_text, alert_open, fn, ln, mi, suffix, cn, email, pw, pwconf]
            
            return [alert_color, alert_text, alert_open, None, None, None, None, None, None, None, None]
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback( # Submit Button for new problem
    [
        Output('new_problem_alert', 'color'),
        Output('new_problem_alert', 'children'),
        Output('new_problem_alert', 'is_open'),
        Output('newproblem', 'value'),
        Output('newproblem_medhistory', 'value'),
        Output('newproblem_diet', 'value'),
        Output('newproblem_watersource', 'value'),
        Output('newproblem_temp', 'value'),
        Output('newproblem_pr', 'value'),
        Output('newproblem_weight', 'value'),
        Output('newproblem_rr', 'value'),
        Output('newproblem_bodyscore', 'value'),
    ],
    [
        Input('problem_submit', 'n_clicks'),
        Input('newproblem', 'value'),
        Input('newproblem_medhistory', 'value'),
        Input('newproblem_diet', 'value'),
        Input('newproblem_watersource', 'value'),
        Input('newproblem_temp', 'value'),
        Input('newproblem_pr', 'value'),
        Input('newproblem_weight', 'value'),
        Input('newproblem_rr', 'value'),
        Input('newproblem_bodyscore', 'value'),
    ]
)
def new_problem_save(submitbtn, problem, hist, diet, water, temp, pr, weight, rr, bodyscore):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        sql = """
            select max(visit_id)
            from visit
            """
        values = []
        df = db.querydatafromdatabase(sql,values)
        visit_id = int(df.loc[0,0])

        sql = """
            select patient_id
            from visit
            where visit_id = %s
            """
        values = [visit_id]
        df = db.querydatafromdatabase(sql, values)
        patient_id = int(df.loc[0][0])

        sql = """
            select count(distinct(problem_id)) + 1
            from visit
            where patient_id = %s
            """
        values = [patient_id]
        df = db.querydatafromdatabase(sql, values)
        prob_no = int(df.loc[0][0])

        sql = """
            select
                floor(extract(year from age(current_date, patient_bd)))
            from patient
            where patient_id = %s
            """
        values = [patient_id]
        df = db.querydatafromdatabase(sql, values)
        prob_age = int(df.loc[0][0])
    
        alert_open = False
        alert_color = ''
        alert_text = ''

        if eventid == 'problem_submit' and submitbtn:

            if not problem:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please describe the problem in general"
            elif not hist:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter any relevant medical history, medication, or injuries. If none, type None"
            elif not diet:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter the patient's general diet"
            elif not water:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter the patient's general source of hydration"
            elif not temp:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter the patient's most recent temperature"
            elif not pr:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter the patient's pulse rate per minute"
            elif not weight:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter the patient's weight in kilogram"
            elif not rr:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter the patient's respiration rate per minute"
            elif not bodyscore:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please enter the patient's body condition score"
            else:
                sql = '''
                INSERT INTO problem(
                                problem_no,
                                problem_animalage,
                                problem_chief_complaint,
                                problem_medical_history,
                                problem_diet_source,
                                problem_water_source,
                                problem_temp,
                                problem_pr,
                                problem_rr,
                                problem_weight,
                                problem_bodycondition_score,
                                problem_delete_ind
                            )
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                values = [prob_no, prob_age, problem, hist, diet, water, temp, pr, rr, weight, bodyscore, False]

                db.modifydatabase(sql, values)

            if not all([problem, hist, diet, water, temp, pr, rr, weight, bodyscore]):
                return [alert_color, alert_text, alert_open, problem, hist, diet, water, temp, pr, weight, rr, bodyscore]
            
            return [alert_color, alert_text, alert_open, None, None, None, None, None, None, None, None, None]
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate



#FUNCTIONAL CALLBACKS

@app.callback( #callback for list of existing clients for returning patient
    [
        Output('re_clientlist', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('re_clientlist', 'value'),
    ]
)
def re_clientlist(pathname, searchterm):
    if pathname == "/home_visit"  and not searchterm:
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
            
        if searchterm:
            sql += """ AND (
                client_ln ILIKE %s 
                OR client_fn ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]

        sql += " ORDER BY client_name;"

        cols = ['client_id', 'client_name']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['client_name'], 'value': row['client_id']} for _, row in result.iterrows()]

        return options, 
    else:
        raise PreventUpdate  

@app.callback( #callback for list of existing patients in the database
    [
        Output('patientlist', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('re_clientlist', 'value'),
        Input('patientlist', 'value'),
    ]
)
def patientlist(pathname, selected_client_id, searchterm):
    if pathname == "/home_visit" and not searchterm:
        sql = """ 
            SELECT 
                patient_id,
                COALESCE(patient_m, '') ||' - ' || COALESCE(patient_species,'') || ' (' || COALESCE(patient_breed, '')|| ')' AS patient_name
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
                OR patient_species ILIKE %s 
                OR patient_breed ILIKE %s
                );
            """
            values.extend([f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"])

        sql += " ORDER BY patient_name;"

        cols = ['patient_id', 'patient_name']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['patient_name'], 'value': row['patient_id']} for _, row in result.iterrows()]
        return options, 
    else:
        raise PreventUpdate  
     
@app.callback(#list of veterinarian assigned for visit
    [
        Output("vetlist", 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input("vetlist", 'value'),
    ]
)
def vetlist(pathname, searchterm):
    if pathname == "/home_visit" and not searchterm:
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

        if searchterm:
            sql += """ AND vet_name ILIKE %s
            """
            values = [f"%{searchterm}%"]

        sql += " ORDER BY vet_name;"

        cols = ['vet_id', 'vet_name']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['vet_name'], 'value': row['vet_id']} for _, row in result.iterrows()]
        return options,    
    else:
        raise PreventUpdate  

@app.callback( #callback for list of existing clients for new patientInp
    [
        Output('new_clientlist', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('new_clientlist', 'value'),
    ]
)
def new_clientlist(pathname, searchterm):
    if pathname == "/home_visit"  and not searchterm:
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
            
        if searchterm:
            sql += """ AND (
                client_ln ILIKE %s 
                OR client_fn ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]

        sql += " ORDER BY client_name;"
        
        cols = ['client_id', 'client_name']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['client_name'], 'value': row['client_id']} for _, row in result.iterrows()]
        return options, 
    else:
        raise PreventUpdate  

@app.callback( #list of problems for follow up 
    [
        Output('problem_list', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('patientlist', 'value'),
        Input('problem_list', 'value'),
    ]
)
def problem_list_reCreP(pathname, selected_patient_id,searchterm):
    if pathname == "/home_visit"  and not searchterm:
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

@app.callback( # to extend the card to include the problem dropdown
    Output('follow_up_field', 'style'),
    Input('visitpurpose_problem', 'value'),
)
def toggle_problem_list(selected_option):
    if selected_option is None:
        selected_option = []
    
    if 'follow_up' in selected_option:
        return {"display": "block"}
    else:
        return {"display": "none"}
    
@app.callback( # to reset the visit purpose and make the problem mutually exclusive
    [
        Output('visitpurpose', 'value'),
        Output('visitpurpose_problem', 'value'),
    ],
    [
        Input('visitrecord_submit', 'n_clicks'),
        Input('visitpurpose_problem', 'value'),
    ],
    [
        State('visitpurpose_problem', 'value'),
        State('visitpurpose', 'value'),
        State('re_clientlist', 'value'),
        State('patientlist','value'),
        State('vetlist','value'),
        State('visitdate', 'value'),
        State('problem_list', 'value'),
    ],
)
def resetvisitfield(submitbtn, selected_option, prob, vacc_deworm, client, patient, vet, date, prev_prob):
    if selected_option is None:
        prob = []

    if vacc_deworm is None:
        vacc_deworm = []
    
    if len(prob) == 2:
        prob = prob[1:]    

    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        visit_for_vacc = 'vaccination' in vacc_deworm
        visit_for_deworm = 'deworming' in vacc_deworm
        follow_up = 'follow_up' in prob
        follow_and_problem = follow_up == any([prev_prob])
        visit_for_problem = len(prob) == 1

        if eventid == 'visitrecord_submit' and submitbtn and all([client, patient, vet, date, follow_and_problem, any([visit_for_problem, visit_for_deworm, visit_for_vacc])]):
            prob = []
            vacc_deworm = []
    
    return [vacc_deworm, prob]




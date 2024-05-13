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
import time


layout = html.Div([
        html.Div(id = 'client_patient_content'),
        
        html.Div([ # vaccination card
            html.Br(),
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.H2("Vaccination", className = 'flex-grow-1'),
                        html.Div(dbc.Button("Add Administered Vaccine Medication", id = "add_vaccine_form_btn", href=""), className = "ml-2 d-flex"),
                    ], className = "d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody([
                    html.Div(id = "visit_vaccine_list")
                ]),
            ]),
        ], id = 'vaccine_field', style = {'display': 'none'}),

        html.Div([ # deworming card
            html.Br(),
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.H2("Deworming", className = 'flex-grow-1'),
                        html.Div(dbc.Button("Add Administered Deworm Medication", id = "add_deworm_form_btn", href=""), className = "ml-2 d-flex"),
                    ], className = "d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody([
                    html.Div(id = "visit_deworm_list")
                ]),
            ]),
        ], id = 'deworm_field', style = {'display': 'none'}),
        html.Div([ # problem card
            html.Br(),
            dbc.Card(
                [
                    dbc.CardHeader(
                    html.Div([
                        html.H2("Problem", className = 'flex-grow-1'),
                    ], className = "d-flex align-items-center justify-content-between")
                    ),
                    dbc.CardBody(
                        [
                            html.Div([
                                html.Div(id='homevisit_problem-table'),
                            ])
                        ]
                    )
                ]
            ),
        ], id = 'new_problem_card', style = {'display': 'none'}),
        
        # html.Div([ #Problem Card
        #     html.Br(),
            # dbc.Card([ 
            #     dbc.CardHeader(
            #                 html.Div([                                
            #                     html.H2("Problem Details", id='homevisit_problemtable', className = 'flex-grow-1'),

            #                     dbc.Col([
            #                         html.Div("Problem Status", className = 'me-2', style = {'white-space': 'nowrap','flex': '0 0 auto'}),
            #                         dcc.Dropdown(
            #                             id = "newproblem_status",
            #                             placeholder = "Select Status",
            #                             searchable = True,
            #                             options = [],
            #                             value = None,
            #                             style = {'flex': '1'},
            #                         ),
            #                     ], className = "d-flex align-items-center", width = 3),
            #                 ], className = "d-flex align-items-center justify-content-between")
            #             ),
            #     dbc.CardBody([

            #                 dbc.Row( #Problem
            #                     [
            #                         dbc.Col(html.H3("Problem"), width=2),
            #                         dbc.Col(dbc.Input(id="newproblem", type='text', placeholder='Enter Problem',), width = 6),
            #                         dbc.Col(html.H6("Problem No:", style={"text-align": "right"}), width = 2),
            #                         dbc.Col(dbc.Input(id='newproblem_no', type='text', placeholder='Problem no'), width = 2),
            #                     ], style={"align-items": "center"}, className="mb-4"
            #                 ),

            #                 dbc.Row([ #Health, Intake, and assessment (2 columns)
            #                     dbc.Col([ #Health & Nutrients Intake column
            #                         dbc.Row(html.H3("Health & Nutrients Intake")),

            #                         dbc.Row(
            #                             [
            #                                 dbc.Label("Relevant Medical History"),
            #                                 dbc.Textarea(id='newproblem_medhistory', placeholder='Enter Any Relevant Medical History', style={"height":85, 'width': '95%'})
            #                             ], style={"margin-left": "1%"}, className="mb-1"
            #                         ),
            #                         dbc.Row(
            #                             [
            #                                 dbc.Col(html.H6("Diet"), width = 3),
            #                                 dbc.Col(dbc.Input(id='newproblem_diet', type = 'text', placeholder="Enter Patient's Diet"))
            #                             ], style={"margin-left": "1%", "margin-right": "1%", "align-items": "center"}, className="mb-1"
            #                         ),
            #                         dbc.Row(
            #                             [
            #                                 dbc.Col(html.H6("Water Source"), width = 3),
            #                                 dbc.Col(dbc.Input(id='newproblem_water', type = 'text', placeholder="Enter Patient's Water Source"))
            #                             ], style={"margin-left": "1%", "margin-right": "1%", "align-items": "center"}, className="mb-1"
            #                         ),
            #                     ]),

            #                     dbc.Col([
            #                         dbc.Row(html.H3("Health Assessment")),
            #                         dbc.Row(
            #                             [
            #                                 dbc.Col(html.H6("Temperature"), width = 4),
            #                                 dbc.Col(dbc.Input(id='newproblem_temp', type='text', placeholder='Enter Temperature'), width = 7)
            #                             ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
            #                         ),
            #                         dbc.Row(
            #                             [
            #                                 dbc.Col(html.H6("Pulse Rate"), width = 4),
            #                                 dbc.Col(dbc.Input(id='newproblem_pr', type='text', placeholder="Enter Pulse Rate"), width = 7)
            #                             ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
            #                         ),
            #                         dbc.Row(
            #                             [
            #                                 dbc.Col(html.H6("Weight"), width = 4),
            #                                 dbc.Col(dbc.Input(id='newproblem_weight', type='text', placeholder='Enter Weight'), width = 7)
            #                             ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
            #                         ),
            #                         dbc.Row(
            #                             [
            #                                 dbc.Col(html.H6("Respiration Rate"), width = 4),
            #                                 dbc.Col(dbc.Input(id='newproblem_rr', type='text', placeholder="Enter Respiration Rate"), width = 7)
            #                             ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
            #                         ),
            #                         dbc.Row(
            #                             [
            #                                 dbc.Col(html.H6("Body Condition Score"), width = 4),
            #                                 dbc.Col(dbc.Input(id='newproblem_bodyscore', type='text', placeholder="Enter Body Condition Score"), width = 7)
            #                             ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
            #                         ),
            #                     ]),
            #                 ], className="mb-4"),

            #                 html.Div([ #Clinical Exam List
            #                     dbc.Card([
            #                         dbc.CardHeader(
            #                             html.Div([
            #                                 html.H2("List of Clinical Exams Done", className = 'flex-grow-1'),
            #                                 html.Div(dbc.Button("Add Exam", id = "add_clinical_form_btn"), className = "ml-2 d-flex"),
            #                             ], className = "d-flex align-items-center justify-content-between")
            #                         ),
            #                         dbc.CardBody([
            #                             html.Div(id = "clinical_exam_list")
            #                         ]),
            #                     ], className="mb-4"),
            #                 ], id = 'clincal_exam_field', style = {'display': 'none'}), 

            #                 html.Div([ #add clinical and progress button row 
            #                     dbc.Row([
            #                         dbc.Col(html.Hr(), className='text-center'),
            #                         dbc.Col(dbc.Button("Add Clinical Exams", id = 'clinical_exam_btn'), width='auto', className='text-center', id = 'show_clinical_exam', style = {'display': 'block'}),
            #                         dbc.Col(dbc.Button("Add Progress Notes", id = 'progress_notes_btn'), width='auto', className='text-center', id = 'show_progress_notes', style = {'display': 'block'}), 
            #                         dbc.Col(html.Hr(), className='text-center'),
            #                     ], className="mb-4"),
            #                 ], id = 'button_row', style = {'display': 'block'}),

            #                 html.Div([ #Progress Notes Card
            #                     dbc.Card([
            #                         dbc.CardHeader(
            #                             html.Div([
            #                                 html.H2("Problem Progress Notes", className = 'flex-grow-1'),
            #                                 html.Div(dbc.Button("Add Note", id = "add_clinical_form_btn"), className = "ml-2 d-flex"),
            #                             ], className = "d-flex align-items-center justify-content-between")
            #                         ),
            #                         dbc.CardBody([
            #                             html.Div(id = "progress_notes_list")
            #                         ]),
            #                     ], className="mb-4"),
            #                 ], id = 'progress_notes_field', style = {'display': 'none'}), 

            #                 dbc.Row(dbc.Col(html.H3("Diagnosis and Treatment"))),
            #                 dbc.Row([ # Under Diagnosis
            #                     dbc.Col(
            #                         [
            #                             dbc.Label("Diagnosis"),
            #                             dbc.Textarea(id='newproblem_reCreP_diagnosis', placeholder='Enter Diagnosis', style={"height":50})
            #                         ],
            #                         width=4
            #                     ),
            #                     dbc.Col(
            #                         [
            #                             dbc.Label("Prescription"),
            #                             dbc.Textarea(id='newproblem_reCreP_prescription', placeholder="Enter Prescription", style={"height":50})
            #                         ],
            #                         width=4
            #                     ),
            #                     dbc.Col(
            #                         [
            #                             dbc.Label("Patient instructions"),
            #                             dbc.Textarea(id='newproblem_reCreP_clienteduc', placeholder="Enter instructions", style={"height":50})
            #                         ],
            #                         width=4
            #                     ),
            #                 ]),
            #             ]),
            # ])
        # ], id = 'new_problem_card', style = {'display': 'none'}),

        dbc.Modal([ #For adding vaccination
            dbc.ModalHeader(html.H4("Administered Vaccine Details", style={'text-align': 'center', 'width': '100%'}), close_button = True),
            dbc.ModalBody([
                dbc.Alert(id = 'vaccinevisitrecord_alert', is_open = False),
                dbc.InputGroup([
                    dbc.InputGroupText("Vaccine Medication", style = {'width': '35%'}),
                    dbc.InputGroupText(
                        dcc.Dropdown(
                            id="vaccine_name",
                            placeholder='Select Vaccine',
                            searchable=True,
                            options=[],
                            value=None,
                            style = {"width": "100%"}
                        ), 
                    style = {'width': '65%'})
                ], className="mb-2",),
                dbc.InputGroup([
                    dbc.InputGroupText("Vaccine Dose", style = {'width': '35%'}),
                    dbc.InputGroupText(
                        dcc.Dropdown(
                            id="vaccine_dose",
                            options=[
                                {'label':'1st', 'value':'1st'},
                                {'label':'2nd', 'value':'2nd'},
                                {'label':'3rd', 'value':'3rd'},
                                {'label':'4th', 'value':'4th'},
                                {'label':'Booster', 'value':'Booster'},
                            ],
                            placeholder='Select Vaccine Dose',
                            style = {"width": "100%"}
                        ), 
                    style = {'width': '65%'}),
                ], className="mb-2",),
                dbc.InputGroup([
                    dbc.InputGroupText("From VetMed?", style = {'width': '35%'}),
                    dbc.InputGroupText(
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
                                'width': '100%',
                            },
                        ), 
                    style = {'width': '65%'}),
                ], className="mb-2",),
                dbc.InputGroup([
                    dbc.InputGroupText("Date Administered (to track all medicine)", style = {'width': '66%'}),
                    dbc.InputGroupText(
                        dcc.DatePickerSingle(
                            id="vaccine_admin",
                            date = None,
                            placeholder="Select Date",
                            display_format='MMM DD, YYYY',
                        )                      
                    ),
                ], className="mb-2",),
                dbc.InputGroup([
                    dbc.InputGroupText("Vaccine Expiration (to plan all medicine)", style = {'width': '66%'}),
                    dbc.InputGroupText(
                        dcc.DatePickerSingle(
                            id="vaccine_exp",
                            date = None,
                            placeholder="Select Date",
                            display_format='MMM DD, YYYY',
                        )                      
                    ),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Details", id="vaccine_submit_btn", className="ms-auto", n_clicks=0),
            ]),
        ], centered = True, id="vaccine_modal", is_open=False, backdrop = "static"), #size = "lg"),
        
        dbc.Modal([ #For adding deworming
            dbc.ModalHeader(html.H4("Administered Deworm Details", style={'text-align': 'center', 'width': '100%'}), close_button = True),
            dbc.ModalBody([
                dbc.Alert(id = 'dewormvisitrecord_alert', is_open = False),
                dbc.InputGroup([
                    dbc.InputGroupText("Deworm Medication", style = {'width': '35%'}),
                    dbc.InputGroupText(
                        dcc.Dropdown(
                            id="deworm_name",
                            placeholder='Select Deworm',
                            searchable=True,
                            options=[],
                            value=None,
                            style = {"width": "100%"}
                        ), 
                    style = {'width': '65%'})
                ], className="mb-2",),
                dbc.InputGroup([
                    dbc.InputGroupText("Deworm Dose", style = {'width': '35%'}),
                    dbc.InputGroupText(
                        dcc.Dropdown(
                            id="deworm_dose",
                            options=[
                                {'label':'1st', 'value':'1st'},
                                {'label':'2nd', 'value':'2nd'},
                                {'label':'3rd', 'value':'3rd'},
                                {'label':'4th', 'value':'4th'},
                                {'label':'Booster', 'value':'Booster'},
                            ],
                            placeholder='Select Deworm Dose',
                            style = {"width": "100%"}
                        ), 
                    style = {'width': '65%'}),
                ], className="mb-2",),
                dbc.InputGroup([
                    dbc.InputGroupText("From VetMed?", style = {'width': '35%'}),
                    dbc.InputGroupText(
                        dbc.RadioItems(
                            options=[
                                {"label": "Yes", "value": "true"},
                                {"label": " No", "value": "false"},
                            ],
                            id="deworm_from_vetmed",
                            inline=False,
                            style={
                                "display": "flex",
                                "justify-content": "between",
                                "gap": "15px",
                                'width': '100%',
                            },
                        ), 
                    style = {'width': '65%'}),
                ], className="mb-2",),
                dbc.InputGroup([
                    dbc.InputGroupText("Date Administered (to track all medicine)", style = {'width': '66%'}),
                    dbc.InputGroupText(
                        dcc.DatePickerSingle(
                            id="deworm_admin",
                            date = None,
                            placeholder="Select Date",
                            display_format='MMM DD, YYYY',
                        )                      
                    ),
                ], className="mb-2",),
                dbc.InputGroup([
                    dbc.InputGroupText("Deworm Expiration (to plan all medicine)", style = {'width': '66%'}),
                    dbc.InputGroupText(
                        dcc.DatePickerSingle(
                            id="deworm_exp",
                            date = None,
                            placeholder="Select Date",
                            display_format='MMM DD, YYYY',
                        )                      
                    ),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Details", id="deworm_submit_btn", className="ms-auto", n_clicks=0),
            ]),
        ], centered = True, id="deworm_modal", is_open=False, backdrop = "static"), #size = "lg"),
        
        # modal for editing client profile
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Edit Client Profile", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "homevisit_clientprofile_alert", is_open = False),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("First Name", style={"width": "17%"}),
                        dbc.Input(id='homevisit_client_fn', type='text', placeholder="e.g. Juan"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Last Name", style={"width": "17%"}),
                        dbc.Input(id='homevisit_client_ln', type='text', placeholder="e.g. Dela Cruz"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Middle Initial", style={"width": "17%"}),
                        dbc.Input(id='homevisit_client_mi', type='text', placeholder="e.g. M."),
                        dbc.InputGroupText("Suffix", style={"width": "12%"}),
                        dbc.Input(id='homevisit_client_suffix', type='text', placeholder="e.g. Jr."),
                    ],
                    className="mb-4",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Contact No.", style={"width": "17%"}),
                        dbc.Input(id='homevisit_client_contact_no', type='text', placeholder="e.g. 09123456789"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Email", style={"width": "17%"}),
                        dbc.Input(id='homevisit_client_email', type='text', placeholder="e.g. Juan.DelaCruz@example.com"),
                    ],
                    className="mb-4",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("House No.", style={"width": "17%"}),
                        dbc.Input(id='homevisit_client_house_no', type='text', placeholder="e.g. No. 1A (or any landmark)"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Street", style={"width": "17%"}),
                        dbc.Input(id='homevisit_client_street', type='text', placeholder="e.g. P. Vargas St."),
                        dbc.InputGroupText("Barangay", style={"width": "12%"}),
                        dbc.Input(id='homevisit_client_barangay', type='text', placeholder="e.g. Krus na Ligas"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("City", style={"width": "17%"}),
                        dbc.Input(id='homevisit_client_city', type='text', placeholder="e.g. Pasay City"),
                        dbc.InputGroupText("Region", style={"width": "12%"}),
                        dbc.Input(id='homevisit_client_region', type='text', placeholder="e.g. Metro Manila"),
                    ],
                    #className="mb-3",
                ),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Client Details", id = "homevisit_client_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "homevisit_client_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of client profile
            dbc.ModalHeader(html.H4('Client Profile Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                dbc.Button("Close", id = 'homevisit_client_close_successmodal', className = "btn btn-primary ms-auto", href=""),
                #dbc.Button("Close", href = "/", id = "close_client_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'homevisit_client_successmodal', backdrop = 'static', is_open = False, keyboard = False),

        # modal for editing patient profile
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Edit Patient Profile", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "homevisit_patientprofile_alert", is_open = False),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Name", style={"width": "17%"}),
                        dbc.Input(id='homevisit_patient_m', type='text', placeholder="e.g. Bantay (leave blank if none)"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Species", style={"width": "17%"}),
                        dbc.Input(id='homevisit_patient_species', type='text', placeholder="e.g. Dog"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Breed", style={"width": "17%"}),
                        dbc.Input(id='homevisit_patient_breed', type='text', placeholder="e.g. Bulldog"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Color Marks", style={"width": "17%"}),
                        dbc.Input(id='homevisit_patient_color', type='text', placeholder="e.g. White or With black spots"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Sex", style={"width": "19%"}),                            
                        dbc.InputGroupText(dcc.Dropdown(
                            id='homevisit_patient_sex',
                            options=[
                                {'label':'Male', 'value':'Male'},
                                {'label':'Female', 'value':'Female'},
                            ],
                            placeholder='Select Sex',
                            style = {"width": "100%"}
                            ), style = {"width": "32%"}
                        ),
                        dbc.InputGroupText("Birth Date", style={"width": "17%"}),
                        dbc.InputGroupText(dmc.DatePicker(
                            id='homevisit_patient_bd',
                            dropdownType='modal',
                            inputFormat='MMM DD, YYYY',
                            placeholder = "Choose Date"
                            ), style = {"width":"32%"}
                        ),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Idiosyncrasies", style={"width": "17%"}),
                        dbc.Input(id='homevisit_patient_idiosync', type='text', placeholder="e.g. Likes morning walks"),
                    ],
                    #className="mb-3",
                ),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Patient Details", id = "homevisit_patient_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "homevisit_patient_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of patient profile
            dbc.ModalHeader(html.H4('Patient Profile Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                dbc.Button("Close", id = 'homevisit_patient_close_successmodal', className = "btn btn-primary ms-auto", href=""),
                #dbc.Button("Close", id = "close_patient_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'homevisit_patient_successmodal', backdrop = 'static', is_open = False, keyboard = False),
        
        
        #modal for editing visit details
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Edit Visit Details", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "homevisit_visitdetails_alert", is_open = False),
                dbc.Row([
                    dbc.Col(html.H4("Veterinarian Assigned"), width=6),
                    dbc.Col(
                        dcc.Dropdown(
                            id='homevisit_visitdetails_vetassigned',
                            options=[],
                            placeholder = "Select Veterinarian"
                        ),
                        width=6,
                    )
                ]),
                html.Div(style={'margin-bottom':'1rem'}),
                dbc.Row([
                    dbc.Col(html.H4("Visit Date"), width=6),
                    dbc.Col(
                        dmc.DatePicker(
                            id='homevisit_visitdetails_date',
                            dropdownType='modal',
                            inputFormat='MMM DD, YYYY',
                            placeholder = "Choose Date"
                        ),
                        width=6,
                    )
                ]),
                html.Div(style={'margin-bottom':'1rem'}),
                html.H3("Visit Purpose"),
                html.Hr(),
                dbc.Row([
                    dbc.Col(html.H4("For Vaccine?"), width=6),
                    dbc.Col(
                        dcc.Dropdown(
                            id='homevisit_visitdetails_forvaccine',
                            options=[
                                {"label": "Yes", "value": True},
                                {"label": "No", "value": False},
                            ],
                            placeholder='Visit Purpose: Vaccine?',
                        ), 
                        width=6,
                    )
                ]),
                html.Div(style={'margin-bottom':'1rem'}),
                dbc.Row([
                    dbc.Col(html.H4("For Deworm?"), width=6),
                    dbc.Col(
                        dcc.Dropdown(
                            id='homevisit_visitdetails_fordeworm',
                            options=[
                                {"label": "Yes", "value": True},
                                {"label": "No", "value": False},
                            ],
                            placeholder='Visit Purpose: Deworming?',
                        ), 
                        width=6,
                    )
                ]),
                html.Div(style={'margin-bottom':'1rem'}),
                dbc.Row([
                    dbc.Col(html.H4("For Problem?"), width=6),
                    dbc.Col(
                        dcc.Dropdown(
                            id='homevisit_visitdetails_forproblem',
                            options=[
                                {"label": "Yes", "value": True},
                                {"label": "No", "value": False},
                            ],
                            placeholder='Visit Purpose: Problem?',
                        ), 
                        width=6,
                    )
                ]),
                html.Div(style={'margin-bottom':'1rem'}),
                dbc.Row([
                    dbc.Col(html.H4("Problem Chief Complaint"), width=6),
                    dbc.Col(
                        dcc.Dropdown(
                            id='homevisit_visitdetails_problemname',
                            options=[],
                            placeholder='Select Problem',
                        ), 
                        width=6,
                    )
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Visit Details", id = "homevisit_visitdetails_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "homevisit_visitdetails_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of visit details
            dbc.ModalHeader(html.H4('Visit Details Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                dbc.Button("Close", id = 'homevisit_visitdetails_close_successmodal', className = "btn btn-primary ms-auto", href=""),
                #dbc.Button("Close", id = "close_patient_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'homevisit_visitdetails_successmodal', backdrop = 'static', is_open = False, keyboard = False),

        html.Div(id = 'temp'),

       ])



# CONTENT CALLBACKS
@app.callback(
    [
        Output('client_patient_content', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('url', 'search'),
    ],
)
def client_patient(pathname, url_search):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)

    sql = """
        SELECT MAX(visit_id)
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])

    sql = """
        select
            vet_fn || ' ' || COALESCE(vet_mi, '') || ' ' || vet_ln || ' ' || COALESCE(vet_suffix, ''),
            TO_CHAR(visit_date, 'Mon DD, YYYY'),
            visit_for_vacc,
            visit_for_deworm,
            visit_for_problem
        from visit v
        join vet on v.vet_id = vet.vet_id
        where
            NOT visit_delete_ind and visit_id = %s
        """
    values = [visit_id]
    cols = ['visit_vet', 'visit_date', 'for_vacc', 'for_deworm', 'for_problem']
    df = db.querydatafromdatabase(sql,values,cols)

    visit_vet = df['visit_vet'][0]
    visit_date = df['visit_date'][0]
    for_problem = df['for_problem'][0]
    for_vacc = df['for_vacc'][0]
    for_deworm = df['for_deworm'][0]

    purpose = []
    if for_problem:
        purpose.append('Medical Problem')
    if for_vacc:
        purpose.append('Vaccination')
    if for_deworm:
        purpose.append('Deworming')
    visit_purpose = '; '.join(purpose)
    
    patient_id = query_id.get('patient_id', [None])[0]

    sql = """
        select
            client.client_id
        from patient
        inner join client on patient.client_id = client.client_id
        where patient_id = %s
        """
    values = [patient_id]
    cols = ['client_id']
    df = db.querydatafromdatabase(sql,values, cols)

    client_id = int(df['client_id'][0])

    sql = """
        SELECT
            patient_m,
            patient_species,
            patient_breed,
            patient_color,
            patient_sex,
            patient_bd,
            floor(extract(year from age(current_date, patient_bd))),
            patient_idiosync
        FROM
            patient
        WHERE
            NOT patient_delete_ind and patient_id = %s
    """
    values = [patient_id]
    cols = ['patient_name', 'species', 'breed', 'color', 'sex', 'bd', 'age', 'idiosync']
    df = db.querydatafromdatabase(sql,values, cols)

    patient_name = df['patient_name'][0]
    patient_species = df['species'][0]
    patient_breed = df['breed'][0]
    patient_color = df['color'][0]
    patient_sex = df['sex'][0]
    patient_bd = df['bd'][0]
    patient_age = int(df['age'][0])
    patient_idiosync = df['idiosync'][0]

    sql = """ 
        SELECT 
            client_fn || ' ' || COALESCE(client_mi, '') || ' ' || client_ln || ' ' || COALESCE(client_suffix, ''),
            client_email,
            client_cn,
            COALESCE(client_house_no || ' ', '') || client_street || ' ' || client_barangay,
            client_city || ', ' || client_region
        FROM 
            client
        WHERE 
            NOT client_delete_ind and client_id = %s
        """
    values = [client_id]
    cols = ['client_name', 'email', 'cn', 'add1', 'add2']
    df = db.querydatafromdatabase(sql,values, cols)

    client_name = df['client_name'][0]
    client_email = df['email'][0]
    client_cn = df['cn'][0]
    client_add1 = df['add1'][0]
    client_add2 = df['add2'][0]

    input = []
    if pathname == "/home_visit/purpose":
        input.extend([
            html.Div([
                dbc.Row([ #Client and Patient Information
                    dbc.Col( #Patient Information (1st Column)
                    dbc.Card([ #Patient Information Card
                        dbc.CardHeader(
                            html.Div([
                                    html.H3("Patient Information", className = "flex-grow-1"),
                                    dbc.Button("Edit Info", id = 'homevisit_patientdetails', n_clicks = 0),
                                ], className = "d-flex align-items-center justify-content-between"),
                        ),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(html.H6('Name:'), width = 3),
                                dbc.Col(html.H3(f'{patient_name}')),
                            ], style={"align-items": "center", "border-bottom": "1px solid #ccc"}, className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.H6('Species:'), width = 3),
                                dbc.Col(html.H6(f'{patient_species}'), width = 4),
                                dbc.Col(html.H6('Breed:'), width = 2),
                                dbc.Col(html.H6(f'{patient_breed}'), width = 3),
                            ], style={"align-items": "center"}, className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.H6('Color Marks:'), width = 3),
                                dbc.Col(html.H6(f'{patient_color}'), width = 4),
                                dbc.Col(html.H6('Sex:'), width = 2),
                                dbc.Col(html.H6(f'{patient_sex}'), width = 3),
                            ], style={"align-items": "center"}, className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.H6('Birth date:'), width = 3),
                                dbc.Col(html.H6(f'{patient_bd}'), width = 4),
                                dbc.Col(html.H6('Age:'), width = 2),
                                dbc.Col(html.H6(f'{patient_age} years old'), width = 3),
                            ], style={"align-items": "center"}, className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.H6('Idiosyncracies:'), width = 3),
                                dbc.Col(html.H6(f'{patient_idiosync}')),
                            ], style={"align-items": "center"}),
                        ]),
                    ]), width = 7,
                ),
                    dbc.Col( #Client Information (2nd column)
                    dbc.Card([ #Client Information Card
                        dbc.CardHeader(
                            html.Div([
                                    html.H3("Client Information", className = "flex-grow-1"),
                                    dbc.Button("Edit Info", id = 'homevisit_clientdetails', n_clicks = 0),
                                ], className = "d-flex align-items-center justify-content-between"),
                        ),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(html.H6('Name:'), width = 3),
                                dbc.Col(html.H3(f'{client_name}')),
                            ], style={"align-items": "center", "border-bottom": "1px solid #ccc"}, className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.H6('Email:'), width = 3),
                                dbc.Col(html.H6(f'{client_email}')),
                            ], style={"align-items": "center"}, className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.H6('Contact No:'), width = 3),
                                dbc.Col(html.H6(f'{client_cn}')),
                            ], style={"align-items": "center"}, className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.H6('Address:'), width = 3),
                                dbc.Col(html.H6(f'{client_add1}')),
                            ], style={"align-items": "center"}, className="mb-2"),
                            dbc.Row([
                                dbc.Col(width = 3),
                                dbc.Col(html.H6(f'{client_add2}')),
                            ], style={"align-items": "center"}),
                        ]),
                    ]), width = 5,
                ),
                ]),
                html.Br(),
                dbc.Card([ # Visit Details
                    dbc.CardHeader(
                html.Div([
                        html.H3("Visit Details", className = "flex-grow-1"),
                        dbc.Button("Edit Details", id = 'homevisit_visitdetails', n_clicks = 0),
                    ], className = "d-flex align-items-center justify-content-between"),
            ),
                    dbc.CardBody([
                        dbc.Row([ # Vet assigned
                            dbc.Col(html.H5('Veterinarian Assigned:'), width = 3),
                            dbc.Col(html.H4(f'{visit_vet}'), width = 3),
                        ], style={"margin-left": "4%", "margin-right": "1%", "align-items": "center"}, className="mb-2"),
                        dbc.Row([ # Visit Date
                            dbc.Col(html.H5('Visit Date:'), width = 3),
                            dbc.Col(html.H4(f'{visit_date}'), width = 3),
                        ], style={"margin-left": "4%", "margin-right": "1%", "align-items": "center"}, className="mb-2"),
                        dbc.Row([ # Visit Purpose
                            dbc.Col(html.H5("Visit Purpose:"), width=3),
                            dbc.Col(html.H4(f'{visit_purpose}'), width = 9),
                        ], style={"margin-left": "4%", "margin-right": "1%", "align-items": "center"}),
                    ]),
                ]),
            ])
        ])
    else:
        input = [None]
    return input



# LAYOUT CALLBACKS

@app.callback( #Add the card depending on the visit purpose
    [
        Output('new_problem_card', 'style'),
        Output('vaccine_field', 'style'),
        Output('deworm_field', 'style'),
    ],
    Input('url', 'pathname'),
)
def toggle_purpose_cards(pathname):
    problem = {'display': "none"}
    vaccine = {'display': "none"}
    deworm = {'display': "none"}

    sql = """
        SELECT MAX(visit_id)
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])

    sql = """
        select
            visit_for_vacc,
            visit_for_deworm,
            visit_for_problem
        from visit
        where
            NOT visit_delete_ind and visit_id = %s
        """
    values = [visit_id]
    cols = ['for_vacc', 'for_deworm', 'for_problem']
    df = db.querydatafromdatabase(sql,values,cols)

    for_problem = df['for_problem'][0]
    for_vacc = df['for_vacc'][0]
    for_deworm = df['for_deworm'][0]

    if pathname == "/home_visit/purpose":
        if for_problem:
            problem = {"display": "block"}

        if for_vacc:
            vaccine = {"display": "block"}

        if for_deworm:
            deworm = {"display": "block"}

    return [problem, vaccine, deworm]
    
@app.callback( #Add vaccine table in the layout
    Output("visit_vaccine_list", "children"),
    Input("url", "pathname")
)
def visit_vaccine_list(pathname):

    sql = """
        SELECT MAX(visit_id)
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])

    try:  
        if pathname == "/home_visit/purpose":
            sql = """
                    SELECT patient.patient_id
                    FROM visit
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                    WHERE
                        visit_id = %s
                """
            values = [visit_id]
            df = db.querydatafromdatabase(sql, values)
            patient_id = int(df.loc[0,0])


            sql = """
                SELECT
                    vacc_no,
                    vacc_m,
                    vacc_dose,
                    vacc_date_administered,
                    vacc_exp,
                    vacc_from_vetmed,
                    v.vacc_id
                FROM vacc v 
                    INNER JOIN vacc_m m on v.vacc_m_id = m.vacc_m_id
                    INNER JOIN visit ON v.visit_id = visit.visit_id
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                WHERE NOT vacc_delete_ind
                    AND patient.patient_id = %s
            """
            values = [patient_id]
            cols = ["No.", "Vaccine Name", "Vaccine Dose", "Date Administered", "Expiration Date", "Vaccine from VetMed?", "ID"]

            df = db.querydatafromdatabase(sql, values, cols)

            if not df.empty:

                buttons = []
                for vacc_id in df["ID"]:
                    buttons += [
                        html.Div(
                            dbc.Button("Edit", href=f'/editvaccine?mode=add&vacc_id={vacc_id}&patient_id={patient_id}', id="vacc_edit_btn", size = 'sm', color = 'success'),
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

@app.callback( #Add deworm table in the layout
    Output("visit_deworm_list", "children"),
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

    try:  
        if pathname == "/home_visit/purpose":
            sql = """
                    SELECT patient.patient_id
                    FROM visit
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                    WHERE
                        visit_id = %s
                """
            values = [visit_id]
            df = db.querydatafromdatabase(sql, values)
            patient_id = int(df.loc[0,0])
            
            sql = """
                SELECT
                    deworm_no,
                    deworm_m,
                    deworm_dose,
                    deworm_administered,
                    deworm_exp,
                    deworm_from_vetmed,
                    d.deworm_id
                FROM deworm d
                    INNER JOIN deworm_m m on d.deworm_m_id = m.deworm_m_id
                    INNER JOIN visit ON d.visit_id = visit.visit_id
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                WHERE NOT deworm_delete_ind
                    AND patient.patient_id = %s
            """
            values = [patient_id]
            cols = ["No.", "Deworm Name", "Deworm Dose", "Date Administered", "Expiration Date", "Deworm from VetMed?", "ID"]

            df = db.querydatafromdatabase(sql, values, cols)

            if not df.empty:

                buttons = []
                for deworm_id in df["ID"]:
                    buttons += [
                        html.Div(
                            dbc.Button("Edit", href=f'/editdeworm?mode=add&deworm_id={deworm_id}&patient_id={patient_id}', size = 'sm', color = 'success'),
                            style = {'text-align': 'center'}
                        )
                    ]
                df['Action'] = buttons
                df = df[["No.", "Deworm Name", "Deworm Dose", "Date Administered", "Expiration Date", "Deworm from VetMed?", "Action"]]
                df["Deworm from VetMed?"] = df["Deworm from VetMed?"].apply(lambda x: 'Yes' if x else 'No')


                table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align': 'center'})
                return [table]
            else:
                empty_df = pd.DataFrame(columns=["No.", "Deworm Name", "Deworm Dose", "Date Administered", "Expiration Date", "Deworm from VetMed?", "Action"])
                table = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'}, header=True, index=False)
                return [table]
        else:
            return [html.Div()]
    except Exception as e:
        print(f"An error occurred: {e}")
        return [html.Div()]

# @app.callback( #Add the client table in the layout
#     Output("clinical_exam_list", "children"),
#     Input("url", "pathname")        
# )
# def clinical_exam_list(pathname):

#     sql = """
#         SELECT MAX(visit_id)
#         FROM visit
#         """
#     values = []
#     df = db.querydatafromdatabase(sql,values)
#     visit_id = int(df.loc[0,0])

#     sql = """
#         select problem_id
#         from visit
#         where visit_id = %s
#         """
#     values = [visit_id]
#     df = db.querydatafromdatabase(sql, values)
#     problem_id = df.loc[0][0]
#     if problem_id == None:
#         problem_id = 0
#     else:
#         problem_id = int(problem_id)
#     problem_id = 6

#     try:  
#         if pathname == "/home_visit/purpose":

#             sql = """
#                 select
#                     clinical_exam_no,
#                     clinical_exam_type_m,
#                     clinical_exam_ab_findings,
#                     STRING_AGG((COALESCE(clinician_fn, '') || ' ' || COALESCE(clinician_mi, '') || ' ' || COALESCE(clinician_ln, '') || ' ' || COALESCE(clinician_suffix, '')),'; ') AS clinician_assigned,
#                     clinical_exam_modified_date,
#                     clinical_exam_no
#                 from clinical_exam e
#                 join clinical_exam_type m on e.clinical_exam_type_id = m.clinical_exam_type_id
#                 join clinician_assignment a on e.clinical_exam_id = a.clinical_exam_id
#                 join clinician c on a.clinician_id = c.clinician_id
#                 where problem_id = %s
#                 group by clinical_exam_no, clinical_exam_type_m, clinical_exam_ab_findings, clinical_exam_modified_date
#                 order by clinical_exam_modified_date
#             """
#             values = [problem_id]
#             cols = ["No.", "Exam", "Clinical Findings", "Clinicians Assigned", "Date", "ID"]

#             df = db.querydatafromdatabase(sql, values, cols)

#             if not df.empty:

#                 buttons = []
#                 for clinical_exam_no in df["ID"]:
#                     buttons += [
#                         html.Div(
#                             dbc.Button("Edit", size = 'sm', color = 'success'),
#                             style = {'text-align': 'center'}
#                         )
#                     ]
#                 df['Action'] = buttons
#                 df = df[["No.", "Exam", "Clinical Findings", "Clinicians Assigned", "Date", "Action"]]


#                 table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align': 'center'})
#                 return [table]
#             else:
#                 empty_df = pd.DataFrame(columns=["No.", "Exam", "Clinical Findings", "Clinicians Assigned", "Date", "Action"])
#                 table = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'}, header=True, index=False)
#                 return [table]
#         else:
#             return [html.Div()]
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return [html.Div()]    

# @app.callback( #Add the progress notes table in the layout
#     Output("progress_notes_list", "children"),
#     Input("url", "pathname")        
# )
# def progress_notes_list(pathname):

#     sql = """
#         SELECT MAX(visit_id)
#         FROM visit
#         """
#     values = []
#     df = db.querydatafromdatabase(sql,values)
#     visit_id = int(df.loc[0,0])

#     sql = """
#         select problem_id
#         from visit
#         where visit_id = %s
#         """
#     values = [visit_id]
#     df = db.querydatafromdatabase(sql, values)
#     problem_id = df.loc[0][0]
#     if problem_id == None:
#         problem_id = 0
#     else:
#         problem_id = int(problem_id)
#     problem_id = 2

#     try:  
#         if pathname == "/home_visit/purpose":

#             sql = """
#                 select
#                     note_no,
#                     note_have_been_tested,
#                     note_differential_diagnosis,
#                     note_treatment,
#                     note_for_testing,
#                     note_or_no,
#                     note_bill,
#                     note_no
#                 from note
#                 where problem_id = %s
#             """
#             values = [problem_id]
#             cols = ["No.", "result_id",  "Differential Diagnosis", "Treatment", "Follow-up test", "OR No.", "Bill", "ID"]

#             df = db.querydatafromdatabase(sql, values, cols)

#             if not df.empty:

#                 action_buttons = []
#                 for action in df["ID"]:
#                     action_buttons += [
#                         html.Div(
#                             dbc.Button("Edit", size = 'sm', color = 'success'),
#                             style = {'text-align': 'center'}
#                         )
#                     ]
#                 df['Action'] = action_buttons

#                 test_buttons = []
#                 for action in df["result_id"]:
#                     if action:
#                         test_buttons += [
#                             html.Div(
#                                 dbc.Button("See Results", size = 'sm', color = 'success'),
#                                 style = {'text-align': 'center'}
#                             )
#                         ]
#                     else:
#                         test_buttons += ['None']
#                 df['Previous Lab Exam'] = test_buttons

#                 df = df[["No.", "Previous Lab Exam", "Differential Diagnosis", "Treatment", "Follow-up test", "OR No.", "Bill", "Action"]]


#                 table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align': 'center'})
#                 return [table]
#             else:
#                 empty_df = pd.DataFrame(columns=["No.", "Previous Lab Exam", "Differential Diagnosis", "Treatment", "Follow-up test", "OR No.", "Bill", "Action"])
#                 table = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'}, header=True, index=False)
#                 return [table]
#         else:
#             return [html.Div()]
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return [html.Div()]    

# @app.callback( # button row
#     [
#         Output('show_clinical_exam', 'style'),
#         Output('show_progress_notes', 'style'),
#         Output('button_row', 'style'),
#         Output('clincal_exam_field', 'style'),
#         Output('progress_notes_field', 'style'),
#     ],
#     [
#         Input('clinical_exam_btn', 'n_clicks'),
#         Input('progress_notes_btn', 'n_clicks'),
#     ],
#     [
#         State('show_clinical_exam', 'style'),
#         State('show_progress_notes', 'style'),
#     ]
# )
# def toggle_clinical_btn(clinical_btn, progress_btn, clinical_show, progress_show):
#     ctx = dash.callback_context
    
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]

#         if eventid == 'clinical_exam_btn' and clinical_btn and progress_show == {'display': 'block'}:
#             return [{'display': 'none'},{'display': 'block'},{'display': 'block'},{'display': 'block'},{'display': 'none'}]
#         if eventid == 'clinical_exam_btn' and clinical_btn and progress_show == {'display': 'none'}:
#             return [{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'block'},{'display': 'block'}]
        
#         if eventid == 'progress_notes_btn' and progress_btn and clinical_show == {'display': 'block'}:
#             return [{'display': 'block'},{'display': 'none'},{'display': 'block'},{'display': 'none'},{'display': 'block'}]
#         if eventid == 'progress_notes_btn' and progress_btn and clinical_show == {'display': 'none'}:
#             return [{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'block'},{'display': 'block'}]
    
#     return [{'display': 'block'}, {'display': 'block'}, {'display': 'block'},{'display': 'none'},{'display': 'none'}]



# MODAL CALLBACKS
    
# @app.callback( # opens vaccine medication modal
#     [
#         Output('vaccine_modal', 'is_open'),
#     ],
#     [
#         Input('add_vaccine_form_btn', 'n_clicks'),
#     ],
#     [
#         State('vaccine_modal', 'is_open'),
#     ]
# )
# def toggle_vaccine_modal(vacc_add_btn, vacc_modal):
#     ctx = dash.callback_context

#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]

#         if eventid == 'add_vaccine_form_btn' and vacc_add_btn:
#             return [not vacc_modal]
        
#     return [vacc_modal]
    
# @app.callback( # opens deworm medication modal
#     [
#         Output('deworm_modal', 'is_open'),
#     ],
#     [
#         Input('add_deworm_form_btn', 'n_clicks'),
#     ],
#     [
#         State('deworm_modal', 'is_open'),
#     ]
# )
# def toggle_deworm_modal(deworm_add_btn, deworm_modal):
#     ctx = dash.callback_context

#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        
#         if eventid == 'add_deworm_form_btn' and deworm_add_btn:
#             return [ not deworm_modal]
        
#     return [deworm_modal]

# @app.callback( # opens vaccine medication modal
#     [
#         Output('temp', 'children'),
#     ],
#     [
#         #Input('vacc_edit_btn', 'n_clicks'),
#         Input({"type": "vacc_edit_btn", "index": ALL}, 'n_clicks'),
#     ],
# )
# def toggle_vaccine_modal(edit_btn):
#     ctx = dash.callback_context

#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         vacc_id = ctx.triggered[0]['prop_id'].split('.')[1]

#         if eventid == 'vacc_edit_btn' and edit_btn:
#             print(vacc_id)
        
#         return [html.Div()]
#     else:
#         return [html.Div()]
    

@app.callback( #opens and close form and success modal for editing client profile
        [
            Output('homevisit_client_modal', 'is_open'),
            Output('homevisit_client_successmodal', 'is_open'),
        ],
        [
            Input('homevisit_clientdetails', 'n_clicks'),
            Input('homevisit_client_submit','n_clicks'),
            Input('homevisit_client_close_successmodal','n_clicks'),
        ],
        [
            State('homevisit_client_modal', 'is_open'),
            State('homevisit_client_successmodal', 'is_open'),
            State('homevisit_client_fn', 'value'),
            State('homevisit_client_ln', 'value'),
            State('homevisit_client_contact_no', 'value'),
            State('homevisit_client_email', 'value'),
            State('homevisit_client_street', 'value'),
            State('homevisit_client_barangay', 'value'),
            State('homevisit_client_city', 'value'),
            State('homevisit_client_region', 'value'),
        ]
)
def homevisit_client_modal(create, submit, close, form, success, fn, ln, cn, email, street, brgy, city, region):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "homevisit_clientdetails" and create:
            return [not form, success]
            
        if eventid == 'homevisit_client_submit' and submit and all([fn, ln, cn, email, street, brgy, city, region]):
            return [not form, not success]
            
        if eventid == 'homevisit_client_close_successmodal' and close:
            return [form, not success]
            
    return [form, success]



@app.callback( #modal initial values
    [
        Output('homevisit_client_fn', 'value'),
        Output('homevisit_client_ln', 'value'),
        Output('homevisit_client_mi', 'value'),
        Output('homevisit_client_suffix', 'value'),
        Output('homevisit_client_contact_no', 'value'),
        Output('homevisit_client_email', 'value'),
        Output('homevisit_client_house_no', 'value'),
        Output('homevisit_client_street', 'value'),
        Output('homevisit_client_barangay', 'value'),
        Output('homevisit_client_city', 'value'),
        Output('homevisit_client_region', 'value'),
    ],
    [
        Input('homevisit_clientdetails', 'n_clicks'),
        Input('url', 'search'),
    ],
)
def homevisit_clientmodal_initial_values(click, url_search):
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)
    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'homevisit_clientdetails' and click:
                sql = """
                    SELECT 
                        client_fn,
                        client_ln,
                        client_mi,
                        client_suffix, 
                        client_cn, 
                        client_email,
                        client_house_no,
                        client_street,
                        client_barangay,
                        client_city,
                        client_region
                    FROM 
                        patient
                    INNER JOIN client ON patient.client_id = client.client_id
                    WHERE patient_id = %s
                """
                values = [patient_id]
                col = ['client_fn', 'client_ln', 'client_mi', 'client_suffix', 'client_cn', 'client_email', 'client_house_no', 'client_street', 'client_barangay', 'client_city', 'client_region']
                        
                df = db.querydatafromdatabase(sql, values, col)
                        
                client_fn = df['client_fn'][0]
                client_ln = df['client_ln'][0]
                client_mi = df['client_mi'][0]
                client_suffix = df['client_suffix'][0]
                client_cn = df['client_cn'][0]
                client_email = df['client_email'][0]
                client_house_no = df['client_house_no'][0]
                client_street = df['client_street'][0]
                client_barangay = df['client_barangay'][0]
                client_city = df['client_city'][0]
                client_region = df['client_region'][0]

                return [client_fn, client_ln, client_mi, client_suffix, client_cn, client_email, client_house_no, client_street, client_barangay, client_city, client_region]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate



@app.callback( # Submit Button for client profile
        [
            Output('homevisit_clientprofile_alert', 'color'),
            Output('homevisit_clientprofile_alert', 'children'),
            Output('homevisit_clientprofile_alert', 'is_open'),
            Output('homevisit_client_close_successmodal', 'href')
        ],
        [
            Input('homevisit_client_submit', 'n_clicks'),
            Input('url', 'search'),
            Input('homevisit_client_fn', 'value'),
            Input('homevisit_client_ln', 'value'),
            Input('homevisit_client_mi', 'value'),
            Input('homevisit_client_suffix', 'value'),
            Input('homevisit_client_contact_no', 'value'),
            Input('homevisit_client_email', 'value'),
            Input('homevisit_client_house_no', 'value'),
            Input('homevisit_client_street', 'value'),
            Input('homevisit_client_barangay', 'value'),
            Input('homevisit_client_city', 'value'),
            Input('homevisit_client_region', 'value'),
        ],
)
def homevisit_client_save(submitbtn, url_search, fn, ln, mi, sf, cn, email, house_no, street, brgy, city, region):
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)
    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'homevisit_client_submit' and submitbtn: 
                alert_open = False
                alert_color = ''
                alert_text = ''

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
                        SELECT client.client_id
                        FROM patient
                        INNER JOIN client ON patient.client_id = client.client_id
                        WHERE patient_id = %s
                    '''
                    values = [patient_id]
                    col = ['client_id']
                    df = db.querydatafromdatabase(sql, values, col)
                    client_id = int(df['client_id'][0])

                    modified_date = datetime.now().strftime("%Y-%m-%d")
                    sql = '''
                        UPDATE client 
                        SET
                            client_ln = %s,
                            client_fn = %s,
                            client_mi = %s,
                            client_suffix = %s,
                            client_email = %s,
                            client_cn = %s,
                            client_house_no = %s,
                            client_street = %s,
                            client_barangay = %s,
                            client_city = %s,
                            client_region = %s,
                            client_modified_date = %s
                        WHERE client_id = %s
                    '''
                    values = [ln, fn, mi, sf, email, cn, house_no, street, brgy, city, region, modified_date, client_id]

                    db.modifydatabase(sql, values)

                href = f'/home_visit/purpose?mode=add&patient_id={patient_id}&refresh={time.time()}'
                return [alert_color, alert_text, alert_open, href]
            
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    



@app.callback( #opens and close form and success modal for creating patient profile
        [
            Output('homevisit_patient_modal', 'is_open'),
            Output('homevisit_patient_successmodal', 'is_open'),
        ],
        [
            Input('homevisit_patientdetails', 'n_clicks'),
            Input('homevisit_patient_submit','n_clicks'),
            Input('homevisit_patient_close_successmodal','n_clicks'),
        ],
        [
            State('homevisit_patient_modal', 'is_open'),
            State('homevisit_patient_successmodal', 'is_open'),
            State('homevisit_patient_species', 'value'),
            State('homevisit_patient_breed', 'value'),
            State('homevisit_patient_color', 'value'),
            State('homevisit_patient_sex', 'value'),
            State('homevisit_patient_bd', 'value'),
            State('homevisit_patient_idiosync', 'value'),
        ]
)
def homevisit_patient_modal(create, submit, close, form, success, species, breed, color, sex, bd, idiosync):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "homevisit_patientdetails" and create:
            return [not form, success]
        
        if eventid == "homevisit_patient_submit" and submit and all([species, color, breed, sex, bd, idiosync]):
            return [not form, not success]
        
        if eventid == "homevisit_patient_close_successmodal" and close:
            return [form, not success]
           
    return [form, success]



@app.callback( #modal initial values
    [
        Output('homevisit_patient_m', 'value'),
        Output('homevisit_patient_species', 'value'),
        Output('homevisit_patient_breed', 'value'),
        Output('homevisit_patient_color', 'value'),
        Output('homevisit_patient_sex', 'value'),
        Output('homevisit_patient_bd', 'value'),
        Output('homevisit_patient_idiosync', 'value'),
    ],
    [
        Input('url', 'search'),
        Input('homevisit_patientdetails', 'n_clicks'),
    ],
)
def homevisit_patientmodal_initial_values(url_search, click):
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'homevisit_patientdetails' and click:
                sql = """
                    SELECT 
                        patient_m,
                        patient_species,
                        patient_breed,
                        patient_color,
                        patient_sex,
                        patient_bd,
                        patient_idiosync
                    FROM 
                        patient
                    WHERE patient_id = %s
                """
                values = [patient_id]
                col = ['patient_m', 'patient_species', 'patient_breed', 'patient_color', 'patient_sex', 'patient_bd', 'patient_idiosync']
                    
                df = db.querydatafromdatabase(sql, values, col)
                    
                patient_m = df['patient_m'][0]
                patient_species = df['patient_species'][0]
                patient_breed = df['patient_breed'][0]
                patient_color = df['patient_color'][0]
                patient_sex = df['patient_sex'][0]
                patient_bd = df['patient_bd'][0]
                patient_idiosync = df['patient_idiosync'][0]

                return [patient_m, patient_species, patient_breed, patient_color, patient_sex, patient_bd, patient_idiosync]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    



@app.callback( # Submit Button for patient profile
        [
            Output('homevisit_patientprofile_alert', 'color'),
            Output('homevisit_patientprofile_alert', 'children'),
            Output('homevisit_patientprofile_alert', 'is_open'),
            Output('homevisit_patient_close_successmodal', 'href')
        ],
        [
            Input('homevisit_patient_submit', 'n_clicks'),
            Input('url', 'search'),
            Input('homevisit_patient_m', 'value'),
            Input('homevisit_patient_species', 'value'),
            Input('homevisit_patient_breed', 'value'),
            Input('homevisit_patient_color', 'value'),
            Input('homevisit_patient_sex', 'value'),
            Input('homevisit_patient_bd', 'value'),
            Input('homevisit_patient_idiosync', 'value'),
        ],
)
def editprofile_patient_save(submitbtn, url_search, name, species, breed, color, sex, bd, idiosync):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'homevisit_patient_submit' and submitbtn: 
            parsed = urlparse(url_search)
            query_patient_id = parse_qs(parsed.query)
            if 'patient_id' in query_patient_id:
                patient_id = query_patient_id['patient_id'][0]
        
                alert_open = False
                alert_color = ''
                alert_text = ''

                if not species:
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
                    modified_date = datetime.now().strftime("%Y-%m-%d")
                    sql = '''
                        UPDATE patient 
                        SET
                            patient_m = %s,
                            patient_species = %s,
                            patient_breed = %s,
                            patient_color = %s,
                            patient_sex = %s,
                            patient_bd = %s,
                            patient_idiosync = %s,
                            patient_modified_date = %s
                        WHERE patient_id = %s
                    '''
                    values = [name, species, breed, color, sex, bd, idiosync, modified_date, patient_id]

                    db.modifydatabase(sql, values)

                href = f'/home_visit/purpose?mode=add&patient_id={patient_id}&refresh={time.time()}'

                return [alert_color, alert_text, alert_open, href]
            
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    


@app.callback( #opens and close form and success modal for editing visit details
        [
            Output('homevisit_visitdetails_modal', 'is_open'),
            Output('homevisit_visitdetails_successmodal', 'is_open'),
        ],
        [
            Input('homevisit_visitdetails', 'n_clicks'),
            Input('homevisit_visitdetails_submit','n_clicks'),
            Input('homevisit_visitdetails_close_successmodal','n_clicks'),
        ],
        [
            State('homevisit_visitdetails_modal', 'is_open'),
            State('homevisit_visitdetails_successmodal', 'is_open'),
            State('homevisit_visitdetails_date', 'value'),
            State('homevisit_visitdetails_forvaccine', 'value'),
            State('homevisit_visitdetails_fordeworm', 'value'),
            State('homevisit_visitdetails_forproblem', 'value'),
        ]
)
def homevisit_visitdetails_modal(create, submit, close, form, success, date, forvaccine, fordeworm, forproblem):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "homevisit_visitdetails" and create:
            return [not form, success]
        
        if eventid == "homevisit_visitdetails_submit" and submit and all([date, forvaccine, fordeworm, forproblem]):
            return [not form, not success]
        
        if eventid == "homevisit_visitdetails_close_successmodal" and close:
            return [form, not success]
           
    return [form, success]



@app.callback( #modal initial values
    [
        Output('homevisit_visitdetails_vetassigned', 'options'),
        Output('homevisit_visitdetails_vetassigned', 'value'),
        Output('homevisit_visitdetails_date', 'value'),
        Output('homevisit_visitdetails_forvaccine', 'value'),
        Output('homevisit_visitdetails_fordeworm', 'value'),
        Output('homevisit_visitdetails_forproblem', 'value'),
        Output('homevisit_visitdetails_problemname', 'options'),
        Output('homevisit_visitdetails_problemname', 'value'),
    ],
    [
        Input('url', 'search'),
        Input('homevisit_visitdetails', 'n_clicks'),
    ],
)
def homevisit_visitdetailsmodal_initial_values(url_search, click):
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'homevisit_visitdetails' and click:
                sql = """
                    SELECT 
                        vet_id,
                        COALESCE(vet_ln, '') || ', ' || COALESCE (vet_fn, '') || ' ' || COALESCE (vet_mi, '') AS vet_name
                    FROM 
                        vet
                    WHERE 
                        NOT vet_delete_ind
                """
                values = []
                cols = ['vet_id', 'vet_name']
                result = db.querydatafromdatabase(sql, values, cols)
                options1 = [{'label': row['vet_name'], 'value': row['vet_id']} for _, row in result.iterrows()]
                
                sql = """
                    SELECT DISTINCT
                        problem.problem_id,
                        problem_chief_complaint
                    FROM 
                        problem
                    INNER JOIN visit ON problem.problem_id = visit.problem_id
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                    WHERE 
                        NOT problem_delete_ind AND patient.patient_id = %s
                """
                values = [patient_id]
                cols = ['problem_id', 'problem_complaint']
                result = db.querydatafromdatabase(sql, values, cols)
                options2 = [{'label': row['problem_complaint'], 'value': row['problem_id']} for _, row in result.iterrows()]
                
                sql = """
                    SELECT MAX(visit_id)
                    FROM visit
                    """
                values = []
                df = db.querydatafromdatabase(sql,values)
                visit_id = int(df.loc[0,0])

                sql = """
                    SELECT 
                        vet_id,
                        visit_date,
                        visit_for_vacc,
                        visit_for_deworm,
                        visit_for_problem,
                        problem_id
                    FROM 
                        visit
                    WHERE
                        visit_id = %s
                """
                values = [visit_id]
                col = ['vet_id', 'visit_date', 'visit_for_vacc', 'visit_for_deworm', 'visit_for_problem', 'problem_id']
                    
                df = db.querydatafromdatabase(sql, values, col)
                    
                vet_id = df['vet_id'][0]
                visit_date = df['visit_date'][0]
                visit_for_vacc = df['visit_for_vacc'][0]
                visit_for_deworm = df['visit_for_deworm'][0]
                visit_for_problem = df['visit_for_problem'][0]
                problem_id = df['problem_id'][0]

                return [options1, vet_id, visit_date, visit_for_vacc, visit_for_deworm, visit_for_problem, options2, problem_id]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    



@app.callback( # Submit Button for patient profile
        [
            Output('homevisit_visitdetails_alert', 'color'),
            Output('homevisit_visitdetails_alert', 'children'),
            Output('homevisit_visitdetails_alert', 'is_open'),
            Output('homevisit_visitdetails_close_successmodal', 'href')
        ],
        [
            Input('homevisit_visitdetails_submit', 'n_clicks'),
            Input('url', 'search'),
            Input('homevisit_visitdetails_vetassigned', 'value'),
            Input('homevisit_visitdetails_date', 'value'),
            Input('homevisit_visitdetails_forvaccine', 'value'),
            Input('homevisit_visitdetails_fordeworm', 'value'),
            Input('homevisit_visitdetails_forproblem', 'value'),
            Input('homevisit_visitdetails_problemname', 'value'),
        ],
)
def editprofile_visitdetails_save(submitbtn, url_search, vet, date, forvaccine, fordeworm, forproblem, problemname):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'homevisit_visitdetails_submit' and submitbtn: 
            parsed = urlparse(url_search)
            query_patient_id = parse_qs(parsed.query)
            
            if 'patient_id' in query_patient_id:
                patient_id = query_patient_id['patient_id'][0]

                sql = """
                    SELECT MAX(visit_id)
                    FROM visit
                    """
                values = []
                df = db.querydatafromdatabase(sql,values)
                visit_id = int(df.loc[0,0])
        
                alert_open = False
                alert_color = ''
                alert_text = ''

                if not vet:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the veterinarian assigned'
                elif not date:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the visit date'
                elif not forvaccine:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the purpose of visit'
                elif not fordeworm:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the purpose of visit'
                elif not forproblem:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the purpose of visit'
                else:
                    sql = '''
                        UPDATE visit
                        SET
                            vet_id = %s,
                            visit_date = %s,
                            visit_for_vacc = %s,
                            visit_for_deworm = %s,
                            visit_for_problem = %s,
                            problem_id = %s
                        WHERE visit_id = %s
                    '''
                    values = [vet, date, forvaccine, fordeworm, forproblem, problemname, visit_id]

                    db.modifydatabase(sql, values)

                href = f'/home_visit/purpose?mode=add&patient_id={patient_id}&refresh={time.time()}'

                return [alert_color, alert_text, alert_open, href]
            
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate








@app.callback(
    Output('homevisit_problem-table', 'children'),
    Input('url', 'search'),
)

def homevisit_problem_table(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]
        sql = """
        SELECT DISTINCT
            problem_chief_complaint, problem_diagnosis, problem_prescription, problem_client_educ, problem_status_m, problem_date_created, problem_date_resolved, problem.problem_id, patient.patient_id
        FROM 
            problem
        INNER JOIN problem_status ON problem.problem_status_id = problem_status.problem_status_id
        INNER JOIN visit ON problem.problem_id = visit.problem_id
        INNER JOIN patient ON visit.patient_id = patient.patient_id
        WHERE patient.patient_id = %s AND problem_delete_ind = false
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
                        dbc.Button('Edit', href=f'/editproblem?mode=add&problem_id={problem_id}&patient_id={patient_id_query}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Chief Complaint', 'Diagnosis', 'Prescription', 'Patient Instructions', 'Problem Status', 'Start Date', 'Resolved Date', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate


@app.callback(  
    Output('add_vaccine_form_btn', 'href'),
    Output('add_deworm_form_btn', 'href'),
    Input('url', 'search'),
)
def vaccinedewormbuttonlink(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)
    
    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]

        vaccinelink = f'/addvaccine?mode=add&patient_id={patient_id}'
        dewormlink = f'/adddeworm?mode=add&patient_id={patient_id}'
        return vaccinelink, dewormlink

    else:
        raise PreventUpdate
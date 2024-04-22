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
        html.Div(id = 'client_patient_content'),

        dbc.Card([ # Visit Details
            dbc.CardHeader(
                html.Div([
                        html.H3("Visit Details", className = "flex-grow-1"),
                        #dbc.Button("Edit Details", id = 'edit_visit_detail_btn', n_clicks = 0),
                    ], className = "d-flex align-items-center justify-content-between"),
            ),
            dbc.CardBody(html.Div(id = 'purpose_visit_content')),
        ]),

        html.Br(),

        dbc.Row([ #Client and Patient Information
            dbc.Col( #Patient Information (1st Column)
                dbc.Card([ #Patient Information Card
                    dbc.CardHeader(
                        html.Div([
                                html.H3("Patient Information", className = "flex-grow-1"),
                                #dbc.Button("Edit Info", id = 'edit_patient_detail_btn', n_clicks = 0),
                            ], className = "d-flex align-items-center justify-content-between"),
                    ),
                    dbc.CardBody(html.Div(id = 'purpose_patient_content')),
                ]), width = 7,
            ),
            dbc.Col( #Client Information (2nd column)
                dbc.Card([ #Client Information Card
                    dbc.CardHeader(
                        html.Div([
                                html.H3("Client Information", className = "flex-grow-1"),
                                #dbc.Button("Edit Info", id = 'edit_client_detail_btn', n_clicks = 0),
                            ], className = "d-flex align-items-center justify-content-between"),
                    ),
                    dbc.CardBody(html.Div(id = 'purpose_client_content')),
                ]), width = 5,
            ),
        ]),
        
        html.Div([ # vaccination card
            html.Br(),
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.H2("Vaccination", className = 'flex-grow-1'),
                        html.Div(dbc.Button("Add Administered Vaccine Medication", id = {"type": "add_vaccine_form_btn", "index": 0}), className = "ml-2 d-flex"),
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
                        html.Div(dbc.Button("Add Administered Deworm Medication", id = "add_deworm_form_btn"), className = "ml-2 d-flex"),
                    ], className = "d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody([
                    html.Div(id = "visit_deworm_list")
                ]),
            ]),
        ], id = 'deworm_field', style = {'display': 'none'}),

        html.Div([ #Problem Card
            html.Br(),
            dbc.Card([ 
                dbc.CardHeader(
                            html.Div([                                
                                html.H2("Problem Details", className = 'flex-grow-1'),

                                dbc.Col([
                                    html.Div("Problem Status", className = 'me-2', style = {'white-space': 'nowrap','flex': '0 0 auto'}),
                                    dcc.Dropdown(
                                        id = "newproblem_status",
                                        placeholder = "Select Status",
                                        searchable = True,
                                        options = [],
                                        value = None,
                                        style = {'flex': '1'},
                                    ),
                                ], className = "d-flex align-items-center", width = 3),
                            ], className = "d-flex align-items-center justify-content-between")
                        ),
                dbc.CardBody([

                            dbc.Row( #Problem
                                [
                                    dbc.Col(html.H3("Problem"), width=2),
                                    dbc.Col(dbc.Input(id="newproblem", type='text', placeholder='Enter Problem',), width = 6),
                                    dbc.Col(html.H6("Problem No:", style={"text-align": "right"}), width = 2),
                                    dbc.Col(dbc.Input(id='newproblem_no', type='text', placeholder='Problem no'), width = 2),
                                ], style={"align-items": "center"}, className="mb-4"
                            ),

                            dbc.Row([ #Health, Intake, and assessment (2 columns)
                                dbc.Col([ #Health & Nutrients Intake column
                                    dbc.Row(html.H3("Health & Nutrients Intake")),

                                    dbc.Row(
                                        [
                                            dbc.Label("Relevant Medical History"),
                                            dbc.Textarea(id='newproblem_medhistory', placeholder='Enter Any Relevant Medical History', style={"height":85, 'width': '95%'})
                                        ], style={"margin-left": "1%"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Diet"), width = 3),
                                            dbc.Col(dbc.Input(id='newproblem_diet', type = 'text', placeholder="Enter Patient's Diet"))
                                        ], style={"margin-left": "1%", "margin-right": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Water Source"), width = 3),
                                            dbc.Col(dbc.Input(id='newproblem_water', type = 'text', placeholder="Enter Patient's Water Source"))
                                        ], style={"margin-left": "1%", "margin-right": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                ]),

                                dbc.Col([
                                    dbc.Row(html.H3("Health Assessment")),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Temperature"), width = 4),
                                            dbc.Col(dbc.Input(id='newproblem_temp', type='text', placeholder='Enter Temperature'), width = 7)
                                        ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Pulse Rate"), width = 4),
                                            dbc.Col(dbc.Input(id='newproblem_pr', type='text', placeholder="Enter Pulse Rate"), width = 7)
                                        ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Weight"), width = 4),
                                            dbc.Col(dbc.Input(id='newproblem_weight', type='text', placeholder='Enter Weight'), width = 7)
                                        ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Respiration Rate"), width = 4),
                                            dbc.Col(dbc.Input(id='newproblem_rr', type='text', placeholder="Enter Respiration Rate"), width = 7)
                                        ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Body Condition Score"), width = 4),
                                            dbc.Col(dbc.Input(id='newproblem_bodyscore', type='text', placeholder="Enter Body Condition Score"), width = 7)
                                        ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                ]),
                            ], className="mb-4"),

                            html.Div([ #Clinical Exam List
                                dbc.Card([
                                    dbc.CardHeader(
                                        html.Div([
                                            html.H2("List of Clinical Exams Done", className = 'flex-grow-1'),
                                            html.Div(dbc.Button("Add Exam", id = "add_clinical_form_btn"), className = "ml-2 d-flex"),
                                        ], className = "d-flex align-items-center justify-content-between")
                                    ),
                                    dbc.CardBody([
                                        html.Div(id = "clinical_exam_list")
                                    ]),
                                ], className="mb-4"),
                            ], id = 'clincal_exam_field', style = {'display': 'none'}), 

                            html.Div([ #add clinical and progress button row 
                                dbc.Row([
                                    dbc.Col(html.Hr(), className='text-center'),
                                    dbc.Col(dbc.Button("Add Clinical Exams", id = 'clinical_exam_btn'), width='auto', className='text-center', id = 'show_clinical_exam', style = {'display': 'block'}),
                                    dbc.Col(dbc.Button("Add Progress Notes", id = 'progress_notes_btn'), width='auto', className='text-center', id = 'show_progress_notes', style = {'display': 'block'}), 
                                    dbc.Col(html.Hr(), className='text-center'),
                                ], className="mb-4"),
                            ], id = 'button_row', style = {'display': 'block'}),

                            html.Div([ #Progress Notes Card
                                dbc.Card([
                                    dbc.CardHeader(
                                        html.Div([
                                            html.H2("Problem Progress Notes", className = 'flex-grow-1'),
                                            html.Div(dbc.Button("Add Note", id = "add_clinical_form_btn"), className = "ml-2 d-flex"),
                                        ], className = "d-flex align-items-center justify-content-between")
                                    ),
                                    dbc.CardBody([
                                        html.Div(id = "progress_notes_list")
                                    ]),
                                ], className="mb-4"),
                            ], id = 'progress_notes_field', style = {'display': 'none'}), 

                            dbc.Row(dbc.Col(html.H3("Diagnosis and Treatment"))),
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
        ], id = 'new_problem_card', style = {'display': 'none'}),

        dbc.Modal([ #For adding vaccination
            dbc.ModalHeader(html.H4("Administered Vaccine Details", style={'text-align': 'center', 'width': '100%'}), close_button = True),
            dbc.ModalBody([
                dbc.Alert(id = 'add_vaccinevisitrecord_alert', is_open = False),
                dbc.InputGroup([
                    dbc.InputGroupText("Vaccine Medication", style = {'width': '35%'}),
                    dbc.InputGroupText(
                        dcc.Dropdown(
                            id="add_vaccine_name",
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
                            id="add_vaccine_dose",
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
                            id="add_vacc_from_vetmed",
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
                            id="add_vaccine_admin",
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
                            id="add_vaccine_exp",
                            date = None,
                            placeholder="Select Date",
                            display_format='MMM DD, YYYY',
                        )                      
                    ),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Details", id={"type": "add_vaccine_submit_btn", "index": 0}, className="ms-auto", n_clicks=0),
            ]),
        ], centered = True, id="vacc_add_modal", is_open=False, backdrop = "static"), #size = "lg"),

        dbc.Modal([ #For editing vaccination
            dbc.ModalHeader(html.H4("Administered Vaccine Details", style={'text-align': 'center', 'width': '100%'}), close_button = True),
            dbc.ModalBody([
                dbc.Alert(id = 'edit_vaccinevisitrecord_alert', is_open = False),
                dbc.InputGroup([
                    dbc.InputGroupText("Vaccine Medication", style = {'width': '35%'}),
                    dbc.InputGroupText(
                        dcc.Dropdown(
                            id="edit_vaccine_name",
                            placeholder='Select Vaccine',
                            searchable=True,
                            style = {"width": "100%"}
                        ), 
                    style = {'width': '65%'})
                ], className="mb-2",),
                dbc.InputGroup([
                    dbc.InputGroupText("Vaccine Dose", style = {'width': '35%'}),
                    dbc.InputGroupText(
                        dcc.Dropdown(
                            id="edit_vaccine_dose",
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
                            id="edit_vacc_from_vetmed",
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
                            id="edit_vaccine_admin",
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
                            id="edit_vaccine_exp",
                            date = None,
                            placeholder="Select Date",
                            display_format='MMM DD, YYYY',
                        )                      
                    ),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Details", id={"type": "edit_vaccine_submit_btn", "index": 0}, className="ms-auto", n_clicks=0),
            ]),
        ], centered = True, id="vacc_edit_modal", is_open=False, backdrop = "static"), #size = "lg"),

        dbc.Modal([ #For adding deworming
            dbc.ModalHeader(html.H4("Administered Deworm Details", style={'text-align': 'center', 'width': '100%'}), close_button = True),
            dbc.ModalBody([
                dbc.Alert(id = 'dewormvisitrecord_alert', is_open = False),
                dbc.InputGroup([
                    dbc.InputGroupText("Deworm Medication", style = {'width': '35%'}),
                    dbc.InputGroupText(
                        dcc.Dropdown(
                            id="add_deworm_name",
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
                            id="add_deworm_dose",
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
                            id="add_deworm_from_vetmed",
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
                            id="add_deworm_admin",
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
                            id="add_deworm_exp",
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
        ], centered = True, id="deworm_add_modal", is_open=False, backdrop = "static"), #size = "lg"),

        dbc.Modal([ #For editing deworming
            dbc.ModalHeader(html.H4("Administered Deworm Details", style={'text-align': 'center', 'width': '100%'}), close_button = True),
            dbc.ModalBody([
                dbc.Alert(id = 'dewormvisitrecord_alert', is_open = False),
                dbc.InputGroup([
                    dbc.InputGroupText("Deworm Medication", style = {'width': '35%'}),
                    dbc.InputGroupText(
                        dcc.Dropdown(
                            id="edit_deworm_name",
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
                            id="edit_deworm_dose",
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
                            id="edit_deworm_from_vetmed",
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
                            id="edit_deworm_admin",
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
                            id="edit_deworm_exp",
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
        ], centered = True, id="deworm_edit_modal", is_open=False, backdrop = "static"), #size = "lg"),

        html.Div(id = 'temp'),

       ])



# CONTENT CALLBACKS
@app.callback( # profile content callbacks
    [
        Output('purpose_patient_content', 'children'),
        Output('purpose_client_content', 'children'),
        Output('purpose_visit_content', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ],
)
def client_patient(pathname):

    # RETRIEVE INFO FOR VISIT_ID
    sql = """
        SELECT MAX(visit_id)
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])

    sql = """
        select
            v.patient_id,
            p.client_id
        from visit v
        join patient p on v.patient_id = p.patient_id
        join client c on p.client_id = c.client_id
        where visit_id = %s
        """
    values = [visit_id]
    cols = ['patient_id', 'client_id']
    df = db.querydatafromdatabase(sql,values, cols)

    patient_id = int(df['patient_id'][0])
    client_id = int(df['client_id'][0])


    # RETRIEVE INFO FOR CLIENT
    sql = """
        SELECT
            patient_m,
            patient_species,
            patient_breed,
            patient_color,
            patient_sex,
            TO_CHAR(patient_bd, 'Mon DD, YYYY'),
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

    patient_content = []    
    if pathname == "/home_visit/purpose":
        patient_content.extend([
            html.Div([
                dbc.Row([
                    dbc.Col(html.H6('Name:'), style={"margin-right": "-8px"}, width = 3),
                    dbc.Col(html.H3(f'{patient_name}'), style={"margin-right": "8px"}),
                ], style={"align-items": "center", "border-bottom": "1px solid #ccc"}, className="mb-2"),
                dbc.Row([
                    dbc.Col(html.H6('Species:'), width = 3),
                    dbc.Col(html.H6(f'{patient_species}'), style={"border-bottom": "1px solid #ccc"}, width = 4),
                    dbc.Col(html.H6('Breed:'), width = 2),
                    dbc.Col(html.H6(f'{patient_breed}'), style={"border-bottom": "1px solid #ccc"}, width = 3),
                ], style={"align-items": "center", "margin-right": "2%"}, className="mb-2"),
                dbc.Row([
                    dbc.Col(html.H6('Color Marks:'), width = 3),
                    dbc.Col(html.H6(f'{patient_color}'), style={"border-bottom": "1px solid #ccc"}, width = 4),
                    dbc.Col(html.H6('Sex:'), width = 2),
                    dbc.Col(html.H6(f'{patient_sex}'), style={"border-bottom": "1px solid #ccc"}, width = 3),
                ], style={"align-items": "center", "margin-right": "2%"}, className="mb-2"),
                dbc.Row([
                    dbc.Col(html.H6('Birth date:'), width = 3),
                    dbc.Col(html.H6(f'{patient_bd}'), style={"border-bottom": "1px solid #ccc"}, width = 4),
                    dbc.Col(html.H6('Age:'), width = 2),
                    dbc.Col(html.H6(f'{patient_age} years old'), style={"border-bottom": "1px solid #ccc"}, width = 3),
                ], style={"align-items": "center", "margin-right": "2%"}, className="mb-2"),
                dbc.Row([
                    dbc.Col(html.H6('Idiosyncracies:'), width = 3),
                    dbc.Col(html.H6(f'{patient_idiosync}'), style={"border-bottom": "1px solid #ccc"}),
                ], style={"align-items": "center", "margin-right": "2%"}),
            ])
        ])


    # RETRIEVE INFO FOR CLIENT DETAILS
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

    client_content = []    
    if pathname == "/home_visit/purpose":
        client_content.extend([
            html.Div([
                dbc.Row([
                    dbc.Col(html.H6('Name:'), style={"margin-right": "-5px"}, width = 3),
                    dbc.Col(html.H3(f'{client_name}'), style={"margin-right": "5px"}),
                ], style={"align-items": "center", "border-bottom": "1px solid #ccc"}, className="mb-2"),
                dbc.Row([
                    dbc.Col(html.H6('Email:'), width = 3),
                    dbc.Col(html.H6(f'{client_email}'), style={"border-bottom": "1px solid #ccc"},),
                ], style={"align-items": "center", "margin-right": "2%"}, className="mb-2"),
                dbc.Row([
                    dbc.Col(html.H6('Contact No:'), width = 3),
                    dbc.Col(html.H6(f'{client_cn}'), style={"border-bottom": "1px solid #ccc"},),
                ], style={"align-items": "center", "margin-right": "2%"}, className="mb-2"),
                dbc.Row([
                    dbc.Col(html.H6('Address:'), width = 3),
                    dbc.Col(html.H6(f'{client_add1}'), style={"border-bottom": "1px solid #ccc"},),
                ], style={"align-items": "center", "margin-right": "2%"}, className="mb-2"),
                dbc.Row([
                    dbc.Col(width = 3),
                    dbc.Col(html.H6(f'{client_add2}'), style={"border-bottom": "1px solid #ccc"},),
                ], style={"align-items": "center", "margin-right": "2%"}),
            ])
        ])


    # RETRIEVE INFO FOR VISIT DETAILS
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

    visit_content = []    
    if pathname == "/home_visit/purpose":
        visit_content.extend([
            html.Div([
                dbc.Row([ # Vet assigned
                    dbc.Col(html.H6('Vet:'), style={"margin-right": "-30px"}, width = 1),
                    dbc.Col(html.H5(f'{visit_vet}'), style={"text-align": "center", "border-bottom": "1px solid #ccc"}, width = 2),
                    dbc.Col(html.H6('Date:'), style={"margin-right": "-30px"}, width = 1),
                    dbc.Col(html.H5(f'{visit_date}'), style={"text-align": "center", "border-bottom": "1px solid #ccc"}, width = 2),
                    dbc.Col(html.H6("Purpose:"), style={"margin-left": "90px"}, width=1),
                    dbc.Col(html.H5(f'{visit_purpose}'), style={"text-align": "center", "border-bottom": "1px solid #ccc", "margin-right": "-30px"}, width = 5),
                ], style={"align-items": "center", "margin-right": "3%"}, className="mb-2"),
            ]),
        ])

    return [patient_content, client_content, visit_content]

@app.callback( #list of deworming for ADD
    [
        Output("add_deworm_name", 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input("add_deworm_name", 'value'),
    ]
)
def dewormlistfixed(pathname, searchterm):
    if pathname == "/home_visit/purpose" and not searchterm:
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

@app.callback( #list of deworming for EDIT
    [
        Output("edit_deworm_name", 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input("edit_deworm_name", 'value'),
    ]
)
def dewormlistfixed(pathname, searchterm):
    if pathname == "/home_visit/purpose" and not searchterm:
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
    visit_id = 28

    try:  
        if pathname == "/home_visit/purpose":

            sql = """
                SELECT
                    deworm_no,
                    deworm_m,
                    deworm_dose,
                    TO_CHAR(deworm_administered, 'Mon DD, YYYY'),
                    TO_CHAR(deworm_exp, 'Mon DD, YYYY'),
                    deworm_from_vetmed,
                    d.deworm_id
                FROM deworm d
                    INNER JOIN deworm_m m on d.deworm_m_id = m.deworm_m_id
                WHERE NOT deworm_delete_ind
                    AND visit_id = %s
            """
            values = [visit_id]
            cols = ["No.", "Deworm Name", "Deworm Dose", "Date Administered", "Expiration Date", "Deworm from VetMed?", "ID"]

            df = db.querydatafromdatabase(sql, values, cols)

            if not df.empty:

                buttons = []
                for deworm_id in df["ID"]:
                    buttons += [
                        html.Div(
                            dbc.Button("Edit", id={"type": "deworm_edit_btn", "index": deworm_id}, size = 'sm', color = 'success'),
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

@app.callback( #Add the client table in the layout
    Output("clinical_exam_list", "children"),
    Input("url", "pathname")        
)
def clinical_exam_list(pathname):

    sql = """
        SELECT MAX(visit_id)
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])

    sql = """
        select problem_id
        from visit
        where visit_id = %s
        """
    values = [visit_id]
    df = db.querydatafromdatabase(sql, values)
    problem_id = df.loc[0][0]
    if problem_id == None:
        problem_id = 0
    else:
        problem_id = int(problem_id)
    problem_id = 6

    try:  
        if pathname == "/home_visit/purpose":

            sql = """
                select
                    clinical_exam_no,
                    clinical_exam_type_m,
                    clinical_exam_ab_findings,
                    STRING_AGG((COALESCE(clinician_fn, '') || ' ' || COALESCE(clinician_mi, '') || ' ' || COALESCE(clinician_ln, '') || ' ' || COALESCE(clinician_suffix, '')),'; ') AS clinician_assigned,
                    clinical_exam_modified_date,
                    clinical_exam_no
                from clinical_exam e
                join clinical_exam_type m on e.clinical_exam_type_id = m.clinical_exam_type_id
                join clinician_assignment a on e.clinical_exam_id = a.clinical_exam_id
                join clinician c on a.clinician_id = c.clinician_id
                where problem_id = %s
                group by clinical_exam_no, clinical_exam_type_m, clinical_exam_ab_findings, clinical_exam_modified_date
                order by clinical_exam_modified_date
            """
            values = [problem_id]
            cols = ["No.", "Exam", "Clinical Findings", "Clinicians Assigned", "Date", "ID"]

            df = db.querydatafromdatabase(sql, values, cols)

            if not df.empty:

                buttons = []
                for clinical_exam_no in df["ID"]:
                    buttons += [
                        html.Div(
                            dbc.Button("Edit", size = 'sm', color = 'success'),
                            style = {'text-align': 'center'}
                        )
                    ]
                df['Action'] = buttons
                df = df[["No.", "Exam", "Clinical Findings", "Clinicians Assigned", "Date", "Action"]]


                table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align': 'center'})
                return [table]
            else:
                empty_df = pd.DataFrame(columns=["No.", "Exam", "Clinical Findings", "Clinicians Assigned", "Date", "Action"])
                table = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'}, header=True, index=False)
                return [table]
        else:
            return [html.Div()]
    except Exception as e:
        print(f"An error occurred: {e}")
        return [html.Div()]    

@app.callback( #Add the progress notes table in the layout
    Output("progress_notes_list", "children"),
    Input("url", "pathname")        
)
def progress_notes_list(pathname):

    sql = """
        SELECT MAX(visit_id)
        FROM visit
        """
    values = []
    df = db.querydatafromdatabase(sql,values)
    visit_id = int(df.loc[0,0])

    sql = """
        select problem_id
        from visit
        where visit_id = %s
        """
    values = [visit_id]
    df = db.querydatafromdatabase(sql, values)
    problem_id = df.loc[0][0]
    if problem_id == None:
        problem_id = 0
    else:
        problem_id = int(problem_id)
    problem_id = 2

    try:  
        if pathname == "/home_visit/purpose":

            sql = """
                select
                    note_no,
                    note_have_been_tested,
                    note_differential_diagnosis,
                    note_treatment,
                    note_for_testing,
                    note_or_no,
                    note_bill,
                    note_no
                from note
                where problem_id = %s
            """
            values = [problem_id]
            cols = ["No.", "result_id",  "Differential Diagnosis", "Treatment", "Follow-up test", "OR No.", "Bill", "ID"]

            df = db.querydatafromdatabase(sql, values, cols)

            if not df.empty:

                action_buttons = []
                for action in df["ID"]:
                    action_buttons += [
                        html.Div(
                            dbc.Button("Edit", size = 'sm', color = 'success'),
                            style = {'text-align': 'center'}
                        )
                    ]
                df['Action'] = action_buttons

                test_buttons = []
                for action in df["result_id"]:
                    if action:
                        test_buttons += [
                            html.Div(
                                dbc.Button("See Results", size = 'sm', color = 'success'),
                                style = {'text-align': 'center'}
                            )
                        ]
                    else:
                        test_buttons += ['None']
                df['Previous Lab Exam'] = test_buttons

                df = df[["No.", "Previous Lab Exam", "Differential Diagnosis", "Treatment", "Follow-up test", "OR No.", "Bill", "Action"]]


                table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm', style = {'text-align': 'center'})
                return [table]
            else:
                empty_df = pd.DataFrame(columns=["No.", "Previous Lab Exam", "Differential Diagnosis", "Treatment", "Follow-up test", "OR No.", "Bill", "Action"])
                table = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'}, header=True, index=False)
                return [table]
        else:
            return [html.Div()]
    except Exception as e:
        print(f"An error occurred: {e}")
        return [html.Div()]    

@app.callback( # button row
    [
        Output('show_clinical_exam', 'style'),
        Output('show_progress_notes', 'style'),
        Output('button_row', 'style'),
        Output('clincal_exam_field', 'style'),
        Output('progress_notes_field', 'style'),
    ],
    [
        Input('clinical_exam_btn', 'n_clicks'),
        Input('progress_notes_btn', 'n_clicks'),
    ],
    [
        State('show_clinical_exam', 'style'),
        State('show_progress_notes', 'style'),
    ]
)
def toggle_clinical_btn(clinical_btn, progress_btn, clinical_show, progress_show):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'clinical_exam_btn' and clinical_btn and progress_show == {'display': 'block'}:
            return [{'display': 'none'},{'display': 'block'},{'display': 'block'},{'display': 'block'},{'display': 'none'}]
        if eventid == 'clinical_exam_btn' and clinical_btn and progress_show == {'display': 'none'}:
            return [{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'block'},{'display': 'block'}]
        
        if eventid == 'progress_notes_btn' and progress_btn and clinical_show == {'display': 'block'}:
            return [{'display': 'block'},{'display': 'none'},{'display': 'block'},{'display': 'none'},{'display': 'block'}]
        if eventid == 'progress_notes_btn' and progress_btn and clinical_show == {'display': 'none'}:
            return [{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'block'},{'display': 'block'}]
    
    return [{'display': 'block'}, {'display': 'block'}, {'display': 'block'},{'display': 'none'},{'display': 'none'}]



# MODAL CALLBACKS

@app.callback( # opens deworm medication modal
    [
        Output('deworm_add_modal', 'is_open'),
    ],
    [
        Input('add_deworm_form_btn', 'n_clicks'),
    ],
    [
        State('deworm_add_modal', 'is_open'),
    ]
)
def toggle_deworm_modal(deworm_add_btn, deworm_modal):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if eventid == 'add_deworm_form_btn' and deworm_add_btn:
            return [ not deworm_modal]
        
    return [deworm_modal]
    
@app.callback( # opens edit deworm medication modal
    [
        Output('deworm_edit_modal', 'is_open'),
    ],
    [
        Input({"type": "deworm_edit_btn", "index": ALL}, "n_clicks"),
    ],
    [
        State('deworm_edit_modal', 'is_open'),
    ]
)
def toggle_deworm_modal(deworm_add_btn, deworm_modal):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        value = ctx.triggered[0]['value']
        id_dictionary = json.loads(eventid)
        btn_id = id_dictionary["type"]
        deworm_id = id_dictionary["index"]
        
        if btn_id == "deworm_edit_btn" and value:
            return [not deworm_modal]
        
    return [deworm_modal]




# VACCINE-RELATED CALLBACKS

@app.callback( #list of vaccine for ADD
    [
        Output("add_vaccine_name", "options"),
    ],
    [
        Input('url', 'pathname'),
        Input("add_vaccine_name", "value"),
    ]
)
def vaccinelistfixed(pathname, searchterm):
    if pathname == "/home_visit/purpose" and not searchterm:
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

@app.callback( #list of vaccine for EDIT
    [
        Output("edit_vaccine_name", "options"),
    ],
    [
        Input('url', 'pathname'),
        Input("edit_vaccine_name", "value"),
    ]
)
def vaccinelistvariable(pathname, searchterm):
    if pathname == "/home_visit/purpose" and not searchterm:
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
  
@app.callback( #update vaccine table in the layout
    [
        Output("visit_vaccine_list", "children"),
    ],
    [
        Input("url", "pathname"),
        Input({"type": "add_vaccine_submit_btn", "index": ALL}, "n_clicks"),
        Input({"type": "edit_vaccine_submit_btn", "index": ALL}, "n_clicks"),
    ],
    [
        State('add_vaccine_name', 'value'),
        State('add_vaccine_dose','value'),
        State('add_vacc_from_vetmed','value'),
        State('add_vaccine_admin', 'date'),
        State('add_vaccine_exp', 'date'),
        State('edit_vaccine_name', 'value'),
        State('edit_vaccine_dose','value'),
        State('edit_vacc_from_vetmed','value'),
        State('edit_vaccine_admin', 'date'),
        State('edit_vaccine_exp', 'date'),
    ],
)
def visit_vaccine_table(pathname, addsubmitbtn, editsubmitbtn, add_name, add_dose, add_from_vetmed, add_admin, add_exp, edit_name, edit_dose, edit_from_vetmed, edit_admin, edit_exp):

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

    try:
        if pathname == "/home_visit/purpose":

            ctx = dash.callback_context
            
            if ctx.triggered:
                eventid = ctx.triggered[0]['prop_id'].split('.')[0]
                value = ctx.triggered[0]['value']
                id_dictionary = json.loads(eventid)
                btn_id = id_dictionary["type"]
                vacc_id = id_dictionary["index"]

                if btn_id == 'add_vaccine_submit_btn' and value and all([add_name, add_dose, add_from_vetmed, add_admin, add_exp]):

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
                    values = [vacc_no, add_name, add_dose, add_admin, add_exp, add_from_vetmed, False, visit_id]

                    db.modifydatabase(sql, values)

                if btn_id == 'edit_vaccine_submit_btn' and value and all([edit_name, edit_dose, edit_from_vetmed, edit_admin, edit_exp]):

                    sql = '''
                    UPDATE vacc
                    SET vacc_m_id = %s,
                        vacc_dose = %s,
                        vacc_date_administered = %s,
                        vacc_exp = %s,
                        vacc_from_vetmed = %s
                    WHERE vacc_id = %s
                        '''
                    values = [edit_name, edit_dose, edit_admin, edit_exp, edit_from_vetmed, vacc_id]

                    db.modifydatabase(sql, values)

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
    
@app.callback( # opens add vaccine medication modal
    [
        Output('vacc_add_modal', 'is_open'),
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
        Input({"type": "add_vaccine_form_btn", "index": ALL}, "n_clicks"),
        Input({"type": "add_vaccine_submit_btn", "index": ALL}, "n_clicks"),
    ],
    [
        State('add_vaccine_name', 'value'),
        State('add_vaccine_dose','value'),
        State('add_vacc_from_vetmed','value'),
        State('add_vaccine_admin', 'date'),
        State('add_vaccine_exp', 'date'),
        State('vacc_add_modal', 'is_open'),
    ]
)
def toggle_add_vaccine_modal(vacc_add_btn, submitbtn, name, dose, from_vetmed, admin, exp, vacc_modal):
    ctx = dash.callback_context

    alert_open = False
    alert_color = ''
    alert_text = ''

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        value = ctx.triggered[0]['value']
        id_dictionary = json.loads(eventid)
        btn_id = id_dictionary["type"]

        if btn_id == 'add_vaccine_form_btn' and value:
            return [not vacc_modal, alert_color, alert_text, alert_open, name, dose, from_vetmed, admin, exp]
        
        if btn_id == 'add_vaccine_submit_btn' and value:

            if not name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please select the administered vaccine medication'
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
            
            if not all([name, dose, from_vetmed, admin, exp]):
                return [vacc_modal, alert_color, alert_text, alert_open, name, dose, from_vetmed, admin, exp]
            else:
                return [not vacc_modal, alert_color, alert_text, alert_open, None, None, None, None, None]

    return [vacc_modal, alert_color, alert_text, alert_open, name, dose, from_vetmed, admin, exp]

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

@app.callback( # opens edit vaccine medication modal
    [
        Output('vacc_edit_modal', 'is_open'),
        Output('edit_vaccinevisitrecord_alert','color'),
        Output('edit_vaccinevisitrecord_alert','children'),
        Output('edit_vaccinevisitrecord_alert','is_open'),
    ],
    [
        Input({"type": "vacc_edit_btn", "index": ALL}, "n_clicks"),
        Input({"type": "edit_vaccine_submit_btn", "index": ALL}, "n_clicks"),
    ],
    [
        State('edit_vaccine_name', 'value'),
        State('edit_vaccine_dose','value'),
        State('edit_vacc_from_vetmed','value'),
        State('edit_vaccine_admin', 'date'),
        State('edit_vaccine_exp', 'date'),
        State('vacc_edit_modal', 'is_open'),
    ]
)
def toggle_edit_vaccine_modal(vacc_add_btn, vacc_edit_btn, name, dose, from_vetmed, admin, exp, vacc_modal):
    ctx = dash.callback_context

    alert_open = False
    alert_color = ''
    alert_text = ''

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        value = ctx.triggered[0]['value']
        id_dictionary = json.loads(eventid)
        btn_id = id_dictionary["type"]

        if btn_id == "vacc_edit_btn" and value:
            return [not vacc_modal, alert_color, alert_text, alert_open]
        
        if btn_id == "edit_vaccine_submit_btn" and value:

            if not name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please select the administered vaccine medication'
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
            
            if not all([name, dose, from_vetmed, admin, exp]):
                return [vacc_modal, alert_color, alert_text, alert_open]
            else:
                return [not vacc_modal, alert_color, alert_text, alert_open]

    return [vacc_modal, alert_color, alert_text, alert_open]





      
"""html.Div([
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
"""      
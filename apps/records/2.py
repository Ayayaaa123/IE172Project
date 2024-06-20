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
        dbc.Card([ # VISIT DETAILS
            dbc.CardHeader(
                html.Div([
                        html.H3("VISIT DETAILS", className = "flex-grow-1"),
                        #dbc.Button("Edit Details", id = 'edit_visit_detail_btn', n_clicks = 0),
                    ], className = "d-flex align-items-center justify-content-between"),
            ),
            dbc.CardBody(html.Div(id = 'purpose_visit_content')),
        ]),

        html.Br(),

        dbc.Row([ #CLIENT AND PATIENT INFORMATION
            dbc.Col( #Patient Information (1st Column)
                dbc.Card([ #Patient Information Card
                    dbc.CardHeader(
                        html.Div([
                                html.H3("PATIENT INFORMATION", className = "flex-grow-1"),
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
                                html.H3("CLIENT INFORMATION", className = "flex-grow-1"),
                                #dbc.Button("Edit Info", id = 'edit_client_detail_btn', n_clicks = 0),
                            ], className = "d-flex align-items-center justify-content-between"),
                    ),
                    dbc.CardBody(html.Div(id = 'purpose_client_content')),
                ]), width = 5,
            ),
        ]),
  
        html.Div([ # Vaccination card
            html.Br(),
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.H2("VACCINATION", className = 'flex-grow-1'),
                        html.Div(dbc.Button("Add Administered Vaccine Medication", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "add_vaccine_form_btn", href=""), className = "ml-2 d-flex"),
                    ], className = "d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody([
                    html.Div(id = "visit_vaccine_list")
                ]),
            ]),
        ], id = 'vaccine_field', style = {'display': 'none'}),

        html.Div([ # Deworming card
            html.Br(),
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.H2("DEWORMING", className = 'flex-grow-1'),
                        html.Div(dbc.Button("Add Administered Deworm Medication", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "add_deworm_form_btn", href=""), className = "ml-2 d-flex"),
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
                        html.H2("PROBLEM SUMMARY", className = 'flex-grow-1'),
                        html.Div(dbc.Button("Review / Modify Problem Information", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "edit_problem_btn", href=""), className = "ml-2 d-flex"),
                    ], className = "d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody([

                            dbc.Row( #Problem
                                [
                                    dbc.Col(html.H3("Chief Complaint:"), width=2),
                                    dbc.Col(dbc.Input(id="complaint", type='text', disabled=True), width = 5),
                                    dbc.Col(html.H6("Problem No:", style={"text-align": "right"}), width = 1),
                                    dbc.Col(dbc.Input(id='no', type='text', disabled=True), width = 1),
                                    dbc.Col(html.H6("Status:", style={"text-align": "right"}), width = 1),
                                    dbc.Col(dbc.Input(id='stat', type='text', disabled=True), width = 2),
                                ], style={"align-items": "center"}, className="mb-4"
                            ),

                            html.Hr(),

                            dbc.Row([ #Health, Intake, and assessment (2 columns)
                                dbc.Col([ #Health & Nutrients Intake column
                                    dbc.Row(html.H3("Health & Nutrients Intake")),

                                    dbc.Row(
                                        [
                                            dbc.Label("Relevant Medical History:"),
                                            dbc.Textarea(id='medhistory', disabled=True , style={"height":85, 'width': '97%'})
                                        ], style={"margin-left": "1%"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Daily Average Diet:"), width = 3),
                                            dbc.Col(dbc.Input(id='diet', type = 'text', disabled=True))
                                        ], style={"margin-left": "1%", "margin-right": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Daily Water Source:"), width = 3),
                                            dbc.Col(dbc.Input(id='water', type = 'text', disabled=True))
                                        ], style={"margin-left": "1%", "margin-right": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                ], width=8),

                                dbc.Col([
                                    dbc.Row(html.H3("Health Assessment")),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Temperature:"), width = 5),
                                            dbc.Col(dbc.Input(id='temp', type='text', disabled=True), width = 7)
                                        ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Pulse Rate:"), width = 5),
                                            dbc.Col(dbc.Input(id='pr', type='text', disabled=True), width = 7)
                                        ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Weight:"), width = 5),
                                            dbc.Col(dbc.Input(id='weight', type='text', disabled=True), width = 7)
                                        ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Respiration Rate:"), width = 5),
                                            dbc.Col(dbc.Input(id='rr', type='text', disabled=True), width = 7)
                                        ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Body Condition Score:"), width = 5),
                                            dbc.Col(dbc.Input(id='bodyscore', type='text', disabled=True), width = 7)
                                        ], style={"margin-left": "1%", "align-items": "center"}, className="mb-1"
                                    ),
                                ], width=4),
                            ], className="mb-4"),

                            #dbc.Row(dbc.Col(html.H3("Clinical Exams"))),

                            #dbc.Row(html.Div(id = "clinical_exam_list"), className="mb-4"),

                            #dbc.Row(dbc.Col(html.H3("Progress Notes"))),

                            #dbc.Row(html.Div(id = "progress_notes_list"), className="mb-4"),

                            dbc.Row(dbc.Col(html.H3("Diagnosis and Treatment"))),
                            dbc.Row([ # Under Diagnosis
                                dbc.Col(
                                    [
                                        dbc.Label("Diagnosis"),
                                        dbc.Textarea(id='diagnosis', disabled=True, style={"height":75})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Prescription"),
                                        dbc.Textarea(id='prescription', disabled=True, style={"height":75})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Patient instructions"),
                                        dbc.Textarea(id='clienteduc', disabled=True, style={"height":75})
                                    ],
                                    width=4
                                ),
                            ]),
                        ]),

                #dbc.CardBody([
                #    html.Div(id = "visit_problem_content")
                #]),
            ]),
        ], id = 'problem_field', style = {'display': 'none'}),

        html.Br(),
        dbc.Button( #Submit button
                    'Submit',
                    id = 'visitdetails_submit',
                    n_clicks = 0, #initialization 
                    className='custom-submitbutton',
                ),

        dbc.Modal([ #MODAL FOR CREATING NEW PROBLEM
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
                dbc.Button("Submit Problem Details", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "problem_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "new_problem_modal", is_open = False, backdrop = "static", size = 'lg', keyboard = False),

        dbc.Modal(children = [ # SUCCESFUL SAVING OF NEW PROBLEM
            dbc.ModalHeader(html.H4('New Problem Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                #html.A(html.Button("Close", id = 'close_new_problem_success_modal', className = "btn btn-primary ms-auto"),href = ""),
                dbc.Button("Close", href = "", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "close_new_problem_success_modal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'new_problem_success_modal', backdrop = 'static', is_open = False, keyboard = False),
  
        dbc.Modal(children = [ # MODAL IF VACCINE AND DEWORM WASN'T EDITED
            dbc.ModalHeader(html.H4('VACCINATION AND DEWORMING DETAILS!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalBody([
                dbc.Row(dbc.Col(html.H4("No Vaccination or Deworming medication were added", className='text-center')), className="justify-content-center mb-2"),
                dbc.Row(dbc.Col(html.H5("Click 'Close' to add more details for this visit", className='text-center')), className="justify-content-center mb-2"),
                dbc.Row(dbc.Col(html.H5("Click 'Save Visit Details' to continue without adding medication", className='text-center')), className="justify-content-center"),
            ]),
            dbc.ModalFooter([
                html.A(html.Button("Close", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'close_vaccine_deworm_warning_btn', className = "btn btn-primary ms-auto")),
                html.A(html.Button("Save Visit Details", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'ignore_vaccine_deworm_warning_btn', className = "btn btn-primary ms-auto")),
            ]),
        ], centered = True, id = 'vaccine_deworm_warning_Modal', backdrop = 'static', is_open = False, keyboard = False, size = 'lg'),
  
        dbc.Modal(children = [ # MODAL IF VACCINE WASN'T EDITED
            dbc.ModalHeader(html.H4('VACCINATION DETAILS!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalBody([
                dbc.Row(dbc.Col(html.H4("No vaccine medication were added", className='text-center')), className="justify-content-center mb-2"),
                dbc.Row(dbc.Col(html.H5("Click 'Close' to add more details for this visit", className='text-center')), className="justify-content-center mb-2"),
                dbc.Row(dbc.Col(html.H5("Click 'Save Visit Details' to continue saving without adding vaccine", className='text-center')), className="justify-content-center"),
            ]),
            dbc.ModalFooter([
                html.A(html.Button("Close", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'close_vaccine_warning_btn', className = "btn btn-primary ms-auto")),
                html.A(html.Button("Save Visit Details", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'ignore_vaccine_warning_btn', className = "btn btn-primary ms-auto")),
            ]),
        ], centered = True, id = 'vaccine_warning_Modal', backdrop = 'static', is_open = False, keyboard = False, size = 'lg'),

        dbc.Modal(children = [ # MODAL IF DEWORM WASN'T EDITED
            dbc.ModalHeader(html.H4('DEWORMING DETAILS!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalBody([
                dbc.Row(dbc.Col(html.H4("No deworming medication were added", className='text-center')), className="justify-content-center mb-2"),
                dbc.Row(dbc.Col(html.H5("Click 'Close' to add more details for this visit", className='text-center')), className="justify-content-center mb-2"),
                dbc.Row(dbc.Col(html.H5("Click 'Save Visit Details' to continue saving without adding deworming", className='text-center')), className="justify-content-center"),
            ]),
            dbc.ModalFooter([
                html.A(html.Button("Close", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'close_deworm_warning_btn', className = "btn btn-primary ms-auto")),
                html.A(html.Button("Save Visit Details", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'ignore_deworm_warning_btn', className = "btn btn-primary ms-auto")),
            ]),
        ], centered = True, id = 'deworm_warning_Modal', backdrop = 'static', is_open = False, keyboard = False, size = 'lg'),

        dbc.Modal(children = [ # MODAL FOR SUCCESSFUL SAVING OF VISIT DETAILS
            dbc.ModalHeader(html.H4('Visit Details Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                dbc.Button("Return to Home", href = "/home_visit", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='home_visit_btn', className = "ms-auto"),
            ]),
        ],centered = True, id = 'visitdetails_successmodal', backdrop = 'static', is_open = False, keyboard = False),        

       ])





# VISIT-PATIENT-CLIENT RELATED
@app.callback( # ADD CONTENT IN VISIT, PATIENT, CLIENT
    [
        Output('purpose_visit_content', 'children'),
        Output('purpose_patient_content', 'children'),
        Output('purpose_client_content', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('url', 'search'),
    ],
)
def client_patient_visit_content(pathname, url_search):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    
    patient_id = query_id.get('patient_id', [None])[0]
    if patient_id:

        sql = """
            SELECT MAX(visit_id)
            FROM visit
            WHERE 
                NOT visit_delete_ind
                AND patient_id = %s
            """
        values = [patient_id]
        df = db.querydatafromdatabase(sql,values)
        visit_id = int(df.loc[0,0])

        sql = """
            SELECT client_id
            FROM patient
            WHERE
                NOT patient_delete_ind
                AND patient_id = %s
            """
        values = [patient_id]
        df = db.querydatafromdatabase(sql,values)
        client_id = int(df.loc[0,0])



        #RETRIEVE INFO FOR VISIT DETAILS

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



        # RETRIEVE INFO FOR PATIENT

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



        # RETRIEVE INFO FOR CLIENT

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

        return [visit_content, patient_content, client_content]
    else:
        return [[], [], []]





# PROBLEM RELATED
#@app.callback( # giving the close button the href
#    Output('close_new_problem_success_modal', 'href'),
#    Input('url', 'search'),
#)
#def insert_href_in_close_btn(url_search):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    
    patient_id = query_id.get('patient_id', [None])[0]
    if patient_id:
        if url_search != f"?mode=add&patient_id={patient_id}":
            link = f'/home_visit/purpose?mode=add&patient_id={patient_id}'
            return link





# PROBLEM RELATED
@app.callback( #form and success modal for new problem modal
    [
        Output("new_problem_modal", "is_open"),
        Output('new_problem_success_modal', 'is_open'),
    ],
    [
        Input('url', 'search'),
        Input('problem_submit', 'n_clicks'),
        Input("close_new_problem_success_modal", "n_clicks"),
    ],
    [
        State("new_problem_modal", "is_open"),
        State("new_problem_success_modal", "is_open"),
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
def new_problem_modal(url_search, submit, close, form, success, problem, hist, diet, water, temp, pr, weight, rr, bodyscore):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    
    patient_id = query_id.get('patient_id', [None])[0]
    if patient_id:

        sql = """
            SELECT MAX(visit_id)
            FROM visit
            WHERE 
                NOT visit_delete_ind
                AND patient_id = %s
            """
        values = [patient_id]
        df = db.querydatafromdatabase(sql,values)
        visit_id = int(df.loc[0,0])

        sql = """
            select
                visit_for_problem,
                problem_id
            from
                visit
            where
                NOT visit_delete_ind
                AND visit_id = %s
            """
        values = [visit_id]
        cols = ['problem_purpose', 'problem_id']
        df = db.querydatafromdatabase(sql,values, cols)

        problem_purpose = df['problem_purpose'][0]
        problem_id = df['problem_id'][0]

        if problem_purpose:
            if not problem_id and not form:
                return [not form, success]
            
        if not problem_purpose:
            if problem_id:
                sql = '''
                UPDATE visit
                SET
                    problem_id = Null
                WHERE
                    visit_id = %s;
                '''
                values = [visit_id]
                db.modifydatabase(sql, values)

        ctx = dash.callback_context
    
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == "problem_submit" and submit and all([problem, hist, diet, water, temp, pr, weight, rr, bodyscore]):
                return [not form, not success]

            if eventid == "close_new_problem_success_modal" and close:
                return [form, not success]
           
        return [form, success]
    else:
        return [form, success]

@app.callback( # Submit Button for new problem
    [
        Output('close_new_problem_success_modal', 'href'),
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
        Input('url', 'search'),
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
def new_problem_save(url_search, submitbtn, problem, hist, diet, water, temp, pr, weight, rr, bodyscore):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
        
    link = ""
    alert_open = False
    alert_color = ''
    alert_text = ''
    
    patient_id = query_id.get('patient_id', [None])[0]
    if patient_id:

        sql = """
            SELECT MAX(visit_id)
            FROM visit
            WHERE 
                NOT visit_delete_ind
                AND patient_id = %s
            """
        values = [patient_id]
        df = db.querydatafromdatabase(sql,values)
        visit_id = int(df.loc[0,0])

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

        ctx = dash.callback_context
        
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

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
                    link = f'/home_visit/purpose?mode=add&patient_id={patient_id}'
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

                    sql = """
                        SELECT MAX(problem_id)
                        FROM problem
                        WHERE 
                            NOT problem_delete_ind
                        """
                    values = []
                    df = db.querydatafromdatabase(sql,values)
                    problem_id = int(df.loc[0,0])

                    sql = '''
                        UPDATE visit
                        SET
                            problem_id = %s
                        WHERE
                            visit_id = %s
                        '''
                    values = [problem_id, visit_id]
                    db.modifydatabase(sql, values)

                if not all([problem, hist, diet, water, temp, pr, rr, weight, bodyscore]):
                    return [link, alert_color, alert_text, alert_open, problem, hist, diet, water, temp, pr, weight, rr, bodyscore]
                
                return [link, alert_color, alert_text, alert_open, None, None, None, None, None, None, None, None, None]
            
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        return [link, alert_color, alert_text, alert_open, problem, hist, diet, water, temp, pr, weight, rr, bodyscore]

#@app.callback( # ADD CONTENT IN PROBLEM CARD
#    [
#        Output('visit_problem_content', 'children'),
#    ],
#    [
#        Input('url', 'pathname'),
#        Input('url', 'search'),
#    ],
#)
#def problem_content(pathname, url_search):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    
    patient_id = query_id.get('patient_id', [None])[0]
    if patient_id:

        sql = """
            SELECT MAX(visit_id)
            FROM visit
            WHERE 
                NOT visit_delete_ind
                AND patient_id = %s
            """
        values = [patient_id]
        df = db.querydatafromdatabase(sql,values)
        visit_id = int(df.loc[0,0])

        sql = """
            SELECT client_id
            FROM patient
            WHERE
                NOT patient_delete_ind
                AND patient_id = %s
            """
        values = [patient_id]
        df = db.querydatafromdatabase(sql,values)
        client_id = int(df.loc[0,0])

@app.callback( # fill problem card
    [
        Output('edit_problem_btn', 'href'),
        Output('complaint', 'value'),
        Output('no', 'value'),
        Output('stat', 'value'),
        Output('medhistory', 'value'),
        Output('diet', 'value'),
        Output('water', 'value'),
        Output('temp', 'value'),
        Output('pr', 'value'),
        Output('weight', 'value'),
        Output('rr', 'value'),
        Output('bodyscore', 'value'),
        Output('diagnosis', 'value'),
        Output('prescription', 'value'),
        Output('clienteduc', 'value'),
    ],
    [
        Input('url', 'search'),
        Input("close_new_problem_success_modal", "n_clicks"),
    ],
)
def fill_problem_card(url_search, close):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    
    patient_id = query_id.get('patient_id', [None])[0]
    if patient_id:

        sql = """
            SELECT MAX(visit_id)
            FROM visit
            WHERE 
                NOT visit_delete_ind
                AND patient_id = %s
            """
        values = [patient_id]
        df = db.querydatafromdatabase(sql,values)
        visit_id = int(df.loc[0,0])

        sql = """
            select
                problem_id
            from
                visit
            where
                NOT visit_delete_ind
                AND visit_id = %s
            """
        values = [visit_id]
        cols = ['problem_id']
        df = db.querydatafromdatabase(sql,values, cols)

        problem_id = df['problem_id'][0]

        ctx = dash.callback_context
    
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == "close_new_problem_success_modal" and close:
                sql = """
                    select
                        problem_id
                    from
                        visit
                    where
                        NOT visit_delete_ind
                        AND visit_id = %s
                    """
                values = [visit_id]
                cols = ['problem_id']
                df = db.querydatafromdatabase(sql,values, cols)

                problem_id = df['problem_id'][0]

        if problem_id == None:
            link = ""
            return [link, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        else:
            problem_id = int(problem_id)
            link = f'/editproblem?mode=add&problem_id={problem_id}&patient_id={patient_id}'

            sql = """
                select
                    problem_chief_complaint,
                    problem_no,
                    problem_status_m,
                    problem_medical_history,
                    problem_diet_source,
                    problem_water_source,
                    problem_temp,
                    problem_pr,
                    problem_weight,
                    problem_rr,
                    problem_bodycondition_score,
                    problem_diagnosis,
                    problem_prescription,
                    problem_client_educ
                from
                    problem p join problem_status s
                on
                    p.problem_status_id = s.problem_status_id
                where
                    NOT problem_delete_ind
                    AND problem_id = %s
                """
            values = [problem_id]
            cols = ['complaint','no','stat','hist','diet','water','temp','pr','weight','rr','score','diagnosis','prescription','educ']
            df = db.querydatafromdatabase(sql,values,cols)

            complaint = df['complaint'][0]
            no = df['no'][0]
            stat = df['stat'][0]
            hist = df['hist'][0]
            diet = df['diet'][0]
            water = df['water'][0]
            temp = df['temp'][0]
            pr = df['rr'][0]
            weight = df['weight'][0]
            rr = df['rr'][0]
            score = df['score'][0]
            diagnosis = df['diagnosis'][0]
            prescription = df['prescription'][0]
            educ = df['educ'][0]

            return [link, complaint, no, stat, hist, diet, water, temp, pr, weight, rr, score, diagnosis, prescription, educ]
    else:
        
        link = ""
        return [link, None, None, None, None, None, None, None, None, None, None, None, None, None, None]





# LAYOUT CALLBACKS
@app.callback( #Add the card depending on the visit purpose
    [
        Output('problem_field', 'style'),
        Output('vaccine_field', 'style'),
        Output('deworm_field', 'style'),
    ],
    Input('url', 'search'),
)
def toggle_purpose_cards(url_search):
    problem = {'display': "none"}
    vaccine = {'display': "none"}
    deworm = {'display': "none"}

    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    
    patient_id = query_id.get('patient_id', [None])[0]
    if patient_id:

        sql = """
            SELECT MAX(visit_id)
            FROM visit
            WHERE 
                NOT visit_delete_ind
                AND patient_id = %s
            """
        values = [patient_id]
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
                            dbc.Button("Edit", href=f'/editvaccine?mode=add&vacc_id={vacc_id}&patient_id={patient_id}', style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white", 'text-align': 'center'}, id="vacc_edit_btn", size = 'sm'), #color = 'success'),
                            #style = {'text-align': 'center'}
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
                            dbc.Button("Edit", href=f'/editdeworm?mode=add&deworm_id={deworm_id}&patient_id={patient_id}', style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white", 'text-align': 'center'}, size = 'sm'), #color = 'success'),
                            #style = {'text-align': 'center'}
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

@app.callback(  # adding href to vaccine and deworm buttons
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
    
@app.callback( # vaccine and deworm warning + save visit details
    [
        Output('vaccine_deworm_warning_Modal', 'is_open'),
        Output("vaccine_warning_Modal", "is_open"),
        Output('deworm_warning_Modal', 'is_open'),
        Output('visitdetails_successmodal', 'is_open'),
    ],
    [
        Input('url', 'search'),
        Input("visitdetails_submit", "n_clicks"),
        Input('close_vaccine_deworm_warning_btn','n_clicks'),
        Input('ignore_vaccine_deworm_warning_btn','n_clicks'),
        Input('close_vaccine_warning_btn','n_clicks'),
        Input('ignore_vaccine_warning_btn','n_clicks'),
        Input('close_deworm_warning_btn','n_clicks'),
        Input('ignore_deworm_warning_btn','n_clicks'),
        Input("home_visit_btn", "n_clicks"),
    ],
    [
        State('vaccine_deworm_warning_Modal', 'is_open'),
        State("vaccine_warning_Modal", "is_open"),
        State('deworm_warning_Modal', 'is_open'),
        State('visitdetails_successmodal', 'is_open'),
    ]
)
def save_visit_details(url_search, submit, close_vacc_deworm, ignore_vacc_deworm, close_vacc, ignore_vacc, close_deworm, ignore_deworm, home, vacc_deworm_warning, vacc_warning, deworm_warning, success):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    
    patient_id = query_id.get('patient_id', [None])[0]
    if patient_id:

        sql = """
            SELECT MAX(visit_id)
            FROM visit
            WHERE 
                NOT visit_delete_ind
                AND patient_id = %s
            """
        values = [patient_id]
        df = db.querydatafromdatabase(sql,values)
        visit_id = int(df.loc[0,0])

        sql = """
            SELECT max(vacc_id)
            FROM vacc
            WHERE
                NOT vacc_delete_ind
                AND visit_id = %s
            """
        values = [visit_id]
        df = db.querydatafromdatabase(sql,values)
        vacc_id = df.loc[0,0]

        sql = """
            SELECT max(deworm_id)
            FROM deworm
            WHERE
                NOT deworm_delete_ind
                AND visit_id = %s
            """
        values = [visit_id]
        df = db.querydatafromdatabase(sql,values)
        deworm_id = df.loc[0,0]

        sql = """
            select
                visit_for_vacc,
                visit_for_deworm
            from visit
            where
                NOT visit_delete_ind and visit_id = %s
            """
        values = [visit_id]
        cols = ['for_vacc', 'for_deworm']
        df = db.querydatafromdatabase(sql,values,cols)

        for_vacc = df['for_vacc'][0]
        for_deworm = df['for_deworm'][0]

        vaccination = for_vacc == any([vacc_id])
        deworming = for_deworm == any([deworm_id])

        ctx = dash.callback_context
        
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'visitdetails_submit' and submit and vaccination and deworming:
                return [vacc_deworm_warning, vacc_warning,  deworm_warning, not success]
            


            if eventid == 'visitdetails_submit' and submit and not vaccination and not deworming:
                return [not vacc_deworm_warning, vacc_warning, deworm_warning, success]
            
            if eventid == 'close_vaccine_deworm_warning_btn' and close_vacc_deworm:
                return [not vacc_deworm_warning, vacc_warning, deworm_warning, success]
            
            if eventid == 'ignore_vaccine_deworm_warning_btn' and ignore_vacc_deworm:
                sql = '''
                UPDATE visit
                SET
                    visit_for_vacc = %s,
                    visit_for_deworm = %s
                WHERE
                    visit_id = %s;
                '''
                values = [not for_vacc, not for_deworm, visit_id]
                db.modifydatabase(sql, values)

                return [not vacc_deworm_warning, vacc_warning, deworm_warning, not success]
            


            if eventid == 'visitdetails_submit' and submit and not vaccination and deworming:
                return [vacc_deworm_warning, not vacc_warning, deworm_warning, success]
            
            if eventid == 'close_vaccine_warning_btn' and close_vacc:
                return [vacc_deworm_warning, not vacc_warning, deworm_warning, success]
            
            if eventid == 'ignore_vaccine_warning_btn' and ignore_vacc:
                sql = '''
                UPDATE visit
                SET
                    visit_for_vacc = %s
                WHERE
                    visit_id = %s;
                '''
                values = [not for_vacc, visit_id]
                db.modifydatabase(sql, values)

                return [vacc_deworm_warning, not vacc_warning, deworm_warning, not success]
            


            if eventid == 'visitdetails_submit' and submit and vaccination and not deworming:
                return [vacc_deworm_warning, vacc_warning, not deworm_warning, success]
            
            if eventid == 'close_deworm_warning_btn' and close_deworm:
                return [vacc_deworm_warning, vacc_warning, not deworm_warning, success]
            
            if eventid == 'ignore_deworm_warning_btn' and ignore_deworm:
                sql = '''
                UPDATE visit
                SET
                    visit_for_deworm = %s
                WHERE
                    visit_id = %s;
                '''
                values = [not for_deworm, visit_id]
                db.modifydatabase(sql, values)

                return [vacc_deworm_warning, vacc_warning, not deworm_warning, not success]
            
            if eventid == 'home_visit_btn' and home:
                return [vacc_deworm_warning, vacc_warning, deworm_warning, not success]
    else:
        return [vacc_deworm_warning, vacc_warning, deworm_warning, success]
    
    return [vacc_deworm_warning, vacc_warning, deworm_warning, success]
            




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
        html.Div(id = 'client_patient_content'),
        
        html.Div([ # vaccination card
            html.Br(),
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.H2("Vaccination", className = 'flex-grow-1'),
                        html.Div(dbc.Button("Add Administered Vaccine Medication", id = "add_vaccine_form_btn"), className = "ml-2 d-flex"),
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

        html.Div(id = 'temp'),

       ])



# CONTENT CALLBACKS
@app.callback(
    [
        Output('client_patient_content', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ],
)
def client_patient(pathname):

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
                                    dbc.Button("Edit Info", id = 'edit_patient_detail_btn', n_clicks = 0),
                                ], className = "d-flex align-items-center justify-content-between"),
                        ),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(html.H6('Name:'), width = 3),
                                dbc.Col(html.H3(f'{patient_name}')),
                            ], style={"align-items": "center", "border-bottom": "1px solid #ccc"}, className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.H6('Species:'), width = 3),
                                dbc.Col(html.H6(f'{patient_species}'), style={"border-bottom": "1px solid #ccc"}, width = 4),
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
                                    dbc.Button("Edit Info", id = 'edit_client_detail_btn', n_clicks = 0),
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
                        dbc.Button("Edit Details", id = 'edit_visit_detail_btn', n_clicks = 0),
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
    visit_id = 18

    try:  
        if pathname == "/home_visit/purpose":

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
                            dbc.Button("Edit", id="vacc_edit_btn", size = 'sm', color = 'success'),
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
    visit_id = 28

    try:  
        if pathname == "/home_visit/purpose":

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
                            dbc.Button("Edit", size = 'sm', color = 'success'),
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
    
@app.callback( # opens vaccine medication modal
    [
        Output('vaccine_modal', 'is_open'),
    ],
    [
        Input('add_vaccine_form_btn', 'n_clicks'),
    ],
    [
        State('vaccine_modal', 'is_open'),
    ]
)
def toggle_vaccine_modal(vacc_add_btn, vacc_modal):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'add_vaccine_form_btn' and vacc_add_btn:
            return [not vacc_modal]
        
    return [vacc_modal]
    
@app.callback( # opens deworm medication modal
    [
        Output('deworm_modal', 'is_open'),
    ],
    [
        Input('add_deworm_form_btn', 'n_clicks'),
    ],
    [
        State('deworm_modal', 'is_open'),
    ]
)
def toggle_deworm_modal(deworm_add_btn, deworm_modal):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if eventid == 'add_deworm_form_btn' and deworm_add_btn:
            return [ not deworm_modal]
        
    return [deworm_modal]

@app.callback( # opens vaccine medication modal
    [
        Output('temp', 'children'),
    ],
    [
        #Input('vacc_edit_btn', 'n_clicks'),
        Input({"type": "vacc_edit_btn", "index": ALL}, 'n_clicks'),
    ],
)
def toggle_vaccine_modal(edit_btn):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        vacc_id = ctx.triggered[0]['prop_id'].split('.')[1]

        if eventid == 'vacc_edit_btn' and edit_btn:
            print(vacc_id)
        
        return [html.Div()]
    else:
        return [html.Div()]




from dash import dcc #interpreter recommended to replace 'import dash_core_components as dcc' with 'from dash import dcc'
from dash import html #interpreter recommended to replace 'import dash_html_components as html' with 'from dash import html'
import dash_bootstrap_components as dbc
from dash import dash_table #interpreter recommended to replace 'import dash_table' with 'from dash import dash_table'
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_mantine_components as dmc
from app import app
from apps import dbconnect as db
import datetime
from dash import ALL, MATCH
from urllib.parse import urlparse, parse_qs, urlencode
import time


layout = html.Div(
    [
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="/viewrecord", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        dbc.Row([ #Client and Patient Information
            dbc.Col( #Patient Information (1st Column)
                dbc.Card([ #Patient Information Card
                    dbc.CardHeader(
                        html.Div([
                            html.H3("Patient Information", className = "flex-grow-1"),
                            dbc.Button("Edit Info", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'editrecords_patientdetails', n_clicks = 0),
                        ], className = "d-flex align-items-center justify-content-between"),
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.H6('Name:'), width = 3),
                            dbc.Col(html.H3(id='patient_m')),
                        ], style={"align-items": "center", "border-bottom": "1px solid #ccc"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Species:'), width = 3),
                            dbc.Col(html.H6(id='patient_species'), width = 4),
                            dbc.Col(html.H6('Breed:'), width = 2),
                            dbc.Col(html.H6(id='patient_breed'), width = 3),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Color Marks:'), width = 3),
                            dbc.Col(html.H6(id='patient_color'), width = 4),
                            dbc.Col(html.H6('Sex:'), width = 2),
                            dbc.Col(html.H6(id='patient_sex'), width = 3),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Birth date:'), width = 3),
                            dbc.Col(html.H6(id='patient_bd'), width = 4),
                            dbc.Col(html.H6('Age:'), width = 2),
                            dbc.Col(html.H6(id='patient_age'), width = 3),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Idiosyncracies:'), width = 3),
                            dbc.Col(html.H6(id='patient_idiosync')),
                        ], style={"align-items": "center"}),
                    ]),
                ]), width = 7,
            ),
            dbc.Col( #Client Information (2nd column)
                dbc.Card([ #Client Information Card
                    dbc.CardHeader(
                        html.Div([
                            html.H3("Client Information", className = "flex-grow-1"),
                            dbc.Button("Edit Info", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'editrecords_clientdetails', n_clicks = 0),
                        ], className = "d-flex align-items-center justify-content-between"),
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.H6('Name:'), width = 3),
                            dbc.Col(html.H3(id='client_name')),
                        ], style={"align-items": "center", "border-bottom": "1px solid #ccc"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Email:'), width = 3),
                            dbc.Col(html.H6(id='client_email')),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Contact No:'), width = 3),
                            dbc.Col(html.H6(id='client_cn')),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(html.H6('Address:'), width = 3),
                            dbc.Col(html.H6(id='client_address1')),
                        ], style={"align-items": "center"}, className="mb-2"),
                        dbc.Row([
                            dbc.Col(width = 3),
                            dbc.Col(html.H6(id='client_address2')),
                        ], style={"align-items": "center"}),
                    ]),
                ]), width = 5,
            ),
        ]),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H2('Vaccine History')
                                ]
                            ),
                            dbc.CardBody(
                                [
                                    html.Div(  # create section to show list of records
                                        [
                                            html.Div(id='vaccine-table'),   
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    width=6  
                ), #vaccine history

                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H2('Deworming History')
                                ]
                            ),
                            dbc.CardBody(
                                [
                                    html.Div(  # create section to show list of records
                                        [
                                            html.Div(id='deworming-table'),   
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    width=6  
                ),#deworming history
            ]
        ), 
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Problem History")
                    ]
                ),
                dbc.CardBody(
                    [
                        html.Div([
                            html.Div(id='problem-table'),
                        ])
                    ]
                )
            ]
        ),
        html.Br(),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete Record?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='recordprofile_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            style={'fontWeight': 'bold'},
                        ),
                        width=5,
                    ),
                ],
                className="mb-3",
            ),
        id='recordrofile_removerecord_div'),
        html.Br(),
        dbc.Button(
            'Save',
            id='editrecord_savebtn',
            n_clicks=0,
            className='custom-submitbutton',
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4('Save Success')),
                dbc.ModalBody('Record has been updated', id='editrecord_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button("Okay", href='/viewrecord', style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='editrecord_btn_modal')
                )
            ],
            centered=True,
            id='editrecord_successmodal',
            backdrop='static'
        ),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Edit Client Profile", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "editprofile_clientprofile_alert", is_open = False),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("First Name", style={"width": "17%"}),
                        dbc.Input(id='editprofile_client_fn', type='text', placeholder="e.g. Juan"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Last Name", style={"width": "17%"}),
                        dbc.Input(id='editprofile_client_ln', type='text', placeholder="e.g. Dela Cruz"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Middle Initial", style={"width": "17%"}),
                        dbc.Input(id='editprofile_client_mi', type='text', placeholder="e.g. M."),
                        dbc.InputGroupText("Suffix", style={"width": "12%"}),
                        dbc.Input(id='editprofile_client_suffix', type='text', placeholder="e.g. Jr."),
                    ],
                    className="mb-4",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Contact No.", style={"width": "17%"}),
                        dbc.Input(id='editprofile_client_contact_no', type='text', placeholder="e.g. 09123456789"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Email", style={"width": "17%"}),
                        dbc.Input(id='editprofile_client_email', type='text', placeholder="e.g. Juan.DelaCruz@example.com"),
                    ],
                    className="mb-4",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("House No.", style={"width": "17%"}),
                        dbc.Input(id='editprofile_client_house_no', type='text', placeholder="e.g. No. 1A (or any landmark)"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Street", style={"width": "17%"}),
                        dbc.Input(id='editprofile_client_street', type='text', placeholder="e.g. P. Vargas St."),
                        dbc.InputGroupText("Barangay", style={"width": "12%"}),
                        dbc.Input(id='editprofile_client_barangay', type='text', placeholder="e.g. Krus na Ligas"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("City", style={"width": "17%"}),
                        dbc.Input(id='editprofile_client_city', type='text', placeholder="e.g. Pasay City"),
                        dbc.InputGroupText("Region", style={"width": "12%"}),
                        dbc.Input(id='editprofile_client_region', type='text', placeholder="e.g. Metro Manila"),
                    ],
                    #className="mb-3",
                ),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Client Details", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "editprofile_client_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "editprofile_client_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of client profile
            dbc.ModalHeader(html.H4('Client Profile Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                dbc.Button("Close", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'editprofile_client_close_successmodal', className = "btn btn-primary ms-auto", href=""),
                #dbc.Button("Close", href = "/", id = "close_client_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'editprofile_client_successmodal', backdrop = 'static', is_open = False, keyboard = False),

        # modal for creating patient profile
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Edit Patient Profile", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "editprofile_patientprofile_alert", is_open = False),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Name", style={"width": "17%"}),
                        dbc.Input(id='editprofile_patient_m', type='text', placeholder="e.g. Bantay (leave blank if none)"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Species", style={"width": "17%"}),
                        dbc.Input(id='editprofile_patient_species', type='text', placeholder="e.g. Dog"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Breed", style={"width": "17%"}),
                        dbc.Input(id='editprofile_patient_breed', type='text', placeholder="e.g. Bulldog"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Color Marks", style={"width": "17%"}),
                        dbc.Input(id='editprofile_patient_color', type='text', placeholder="e.g. White or With black spots"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Sex", style={"width": "19%"}),                            
                        dbc.InputGroupText(dcc.Dropdown(
                            id='editprofile_patient_sex',
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
                            id='editprofile_patient_bd',
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
                        dbc.Input(id='editprofile_patient_idiosync', type='text', placeholder="e.g. Likes morning walks"),
                    ],
                    #className="mb-3",
                ),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Patient Details", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "editprofile_patient_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "editprofile_patient_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of patient profile
            dbc.ModalHeader(html.H4('Patient Profile Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                dbc.Button("Close", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'editprofile_patient_close_successmodal', className = "btn btn-primary ms-auto", href=""),
                #dbc.Button("Close", id = "close_patient_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'editprofile_patient_successmodal', backdrop = 'static', is_open = False, keyboard = False),
    ]
)


@app.callback(
    [
        Output('client_name', 'children'),
        Output('client_email', 'children'),
        Output('client_cn', 'children'),
        Output('client_address1', 'children'),
        Output('client_address2', 'children'),
        Output('patient_m', 'children'),
        Output('patient_sex', 'children'),
        Output('patient_species', 'children'),
        Output('patient_breed', 'children'),
        Output('patient_bd', 'children'),
        Output('patient_age', 'children'),
        Output('patient_idiosync', 'children'),
        Output('patient_color', 'children'),
    ],
    [
        Input('url', 'search'),
    ],
)
def initial_values(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]
        sql = """
            SELECT 
                client_fn || ' ' || COALESCE(client_mi, '') || ' ' || client_ln || ' ' || COALESCE(client_suffix, '') AS client_name,
                client_email, 
                client_cn, 
                COALESCE(client_house_no || ' ', '') || client_street || ' ' || client_barangay AS client_address1, 
                client_city || ', ' || client_region AS client_address2,
                patient_m, 
                patient_sex, 
                patient_species, 
                patient_breed, 
                patient_bd, 
                floor(extract(year from age(current_date, patient_bd))), 
                patient_idiosync, 
                patient_color
            FROM 
                patient
            INNER JOIN client ON patient.client_id = client.client_id
            WHERE patient_id = %s
        """
        values = [patient_id]
        col = ['client_name', 'client_email', 'client_cn', 'client_address1', 'client_address2',
            'patient_m', 'patient_sex', 'patient_species', 'patient_breed', 'patient_bd', 'patient_age', 'patient_idiosync', 'patient_color']
        
        df = db.querydatafromdatabase(sql, values, col)
        
        client_name = df['client_name'][0]
        client_email = df['client_email'][0]
        client_cn = df['client_cn'][0]
        client_address1 = df['client_address1'][0]
        client_address2 = df['client_address2'][0]
        patient_m = df['patient_m'][0]
        patient_sex = df['patient_sex'][0]
        patient_species = df['patient_species'][0]
        patient_breed = df['patient_breed'][0]
        patient_bd = df['patient_bd'][0]
        patient_age_number = df['patient_age'][0]
        patient_age = str(patient_age_number) + " years old"
        patient_idiosync = df['patient_idiosync'][0]
        patient_color = df['patient_color'][0]

        return [client_name, client_email, client_cn, client_address1, client_address2, 
            patient_m, patient_sex, patient_species, patient_breed, patient_bd, patient_age, patient_idiosync, patient_color]
    
    else:
        raise PreventUpdate
    

@app.callback(
    Output('vaccine-table', 'children'),
    Input('url', 'search'),
)
def vaccine_table(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]
        sql = """
        SELECT 
            vacc_m, vacc_dose, vacc_date_administered, vacc_exp, vacc_id, patient.patient_id
        FROM 
            vacc
        INNER JOIN visit ON vacc.visit_id = visit.visit_id
        INNER JOIN patient ON visit.patient_id = patient.patient_id
        INNER JOIN vacc_m ON vacc.vacc_m_id = vacc_m.vacc_m_id
        WHERE patient.patient_id = %s AND vacc_delete_ind = false
        """
        values = [patient_id]
        sql += "ORDER BY vacc_date_administered DESC"
        col = ['Vaccine Name', 'Dose', 'Date Administered', 'Expiration Date', 'Vacc_ID', 'Patient_ID']
        df = db.querydatafromdatabase(sql, values, col)

        if df.shape:
            buttons = []
            for vacc_id, patient_id_query in zip(df['Vacc_ID'], df['Patient_ID']):
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editvaccine?mode=edit&vacc_id={vacc_id}&patient_id={patient_id_query}', style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white", 'text-align':'center'}, size='sm'), #color='success'),
                        #style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Vaccine Name', 'Dose', 'Date Administered', 'Expiration Date', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate

@app.callback(
    Output('deworming-table', 'children'),
    Input('url', 'search'),
)

def deworm_table(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]
        sql = """
        SELECT 
            deworm_m, deworm_dose, deworm_administered, deworm_exp, deworm_id, patient.patient_id
        FROM 
            deworm
        INNER JOIN visit ON deworm.visit_id = visit.visit_id
        INNER JOIN patient ON visit.patient_id = patient.patient_id
        INNER JOIN deworm_m ON deworm.deworm_m_id = deworm_m.deworm_m_id
        WHERE patient.patient_id = %s AND deworm_delete_ind = false
        """
        values = [patient_id]
        sql += "ORDER BY deworm_administered DESC"
        col = ['Medicine Name', 'Dose', 'Date Administered', 'Expiration Date', 'Deworm_ID', 'Patient_ID']
        df = db.querydatafromdatabase(sql, values, col)

        if df.shape:
            buttons = []
            for deworm_id, patient_id_query in zip(df['Deworm_ID'], df['Patient_ID']):
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editdeworm?mode=edit&deworm_id={deworm_id}&patient_id={patient_id_query}', style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white", 'text-align':'center'}, size='sm'), #color='success'),
                        #style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Medicine Name', 'Dose', 'Date Administered', 'Expiration Date', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate
    

@app.callback(
    Output('problem-table', 'children'),
    Input('url', 'search'),
)

def problem_table(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]
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
                        dbc.Button('Edit', href=f'/editproblem?mode=edit&problem_id={problem_id}&patient_id={patient_id_query}', style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white", 'text-align':'center'}, size='sm'), #color='success'),
                        #style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Chief Complaint', 'Diagnosis', 'Prescription', 'Patient Instructions', 'Problem Status', 'Start Date', 'Resolved Date', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate
    

@app.callback( #opens and close form and success modal for creating client profile
        [
            Output('editprofile_client_modal', 'is_open'),
            Output('editprofile_client_successmodal', 'is_open'),
        ],
        [
            Input('editrecords_clientdetails', 'n_clicks'),
            Input('editprofile_client_submit','n_clicks'),
            Input('editprofile_client_close_successmodal','n_clicks'),
        ],
        [
            State('editprofile_client_modal', 'is_open'),
            State('editprofile_client_successmodal', 'is_open'),
            State('editprofile_client_fn', 'value'),
            State('editprofile_client_ln', 'value'),
            State('editprofile_client_contact_no', 'value'),
            State('editprofile_client_email', 'value'),
            State('editprofile_client_street', 'value'),
            State('editprofile_client_barangay', 'value'),
            State('editprofile_client_city', 'value'),
            State('editprofile_client_region', 'value'),
        ]
)
def editprofile_client_modal(create, submit, close, form, success, fn, ln, cn, email, street, brgy, city, region):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "editrecords_clientdetails" and create:
            return [not form, success]
            
        if eventid == 'editprofile_client_submit' and submit and all([fn, ln, cn, email, street, brgy, city, region]):
            return [not form, not success]
            
        if eventid == 'editprofile_client_close_successmodal' and close:
            return [form, not success]
            
    return [form, success]



@app.callback( #modal initial values
    [
        Output('editprofile_client_fn', 'value'),
        Output('editprofile_client_ln', 'value'),
        Output('editprofile_client_mi', 'value'),
        Output('editprofile_client_suffix', 'value'),
        Output('editprofile_client_contact_no', 'value'),
        Output('editprofile_client_email', 'value'),
        Output('editprofile_client_house_no', 'value'),
        Output('editprofile_client_street', 'value'),
        Output('editprofile_client_barangay', 'value'),
        Output('editprofile_client_city', 'value'),
        Output('editprofile_client_region', 'value'),
    ],
    [
        Input('url', 'search'),
        Input('editrecords_clientdetails', 'n_clicks'),
    ],
)
def clientmodal_initial_values(url_search, click):
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'editrecords_clientdetails' and click:
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
            Output('editprofile_clientprofile_alert', 'color'),
            Output('editprofile_clientprofile_alert', 'children'),
            Output('editprofile_clientprofile_alert', 'is_open'),
            Output('editprofile_client_close_successmodal', 'href')
        ],
        [
            Input('editprofile_client_submit', 'n_clicks'),
            Input('url', 'search'),
            Input('editprofile_client_fn', 'value'),
            Input('editprofile_client_ln', 'value'),
            Input('editprofile_client_mi', 'value'),
            Input('editprofile_client_suffix', 'value'),
            Input('editprofile_client_contact_no', 'value'),
            Input('editprofile_client_email', 'value'),
            Input('editprofile_client_house_no', 'value'),
            Input('editprofile_client_street', 'value'),
            Input('editprofile_client_barangay', 'value'),
            Input('editprofile_client_city', 'value'),
            Input('editprofile_client_region', 'value'),
        ],
)
def editprofile_client_save(submitbtn, url_search, fn, ln, mi, sf, cn, email, house_no, street, brgy, city, region):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'editprofile_client_submit' and submitbtn: 
            parsed = urlparse(url_search)
            query_patient_id = parse_qs(parsed.query)
            if 'id' in query_patient_id:
                patient_id = query_patient_id['id'][0]
                
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

                    modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
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

                href = f'/editrecord?mode=edit&id={patient_id}&refresh={time.time()}'

                return [alert_color, alert_text, alert_open, href]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    



@app.callback( #opens and close form and success modal for creating patient profile
        [
            Output('editprofile_patient_modal', 'is_open'),
            Output('editprofile_patient_successmodal', 'is_open'),
        ],
        [
            Input('editrecords_patientdetails', 'n_clicks'),
            Input('editprofile_patient_submit','n_clicks'),
            Input('editprofile_patient_close_successmodal','n_clicks'),
        ],
        [
            State('editprofile_patient_modal', 'is_open'),
            State('editprofile_patient_successmodal', 'is_open'),
            State('editprofile_patient_species', 'value'),
            State('editprofile_patient_breed', 'value'),
            State('editprofile_patient_color', 'value'),
            State('editprofile_patient_sex', 'value'),
            State('editprofile_patient_bd', 'value'),
            State('editprofile_patient_idiosync', 'value'),
        ]
)
def editprofile_patient_modal(create, submit, close, form, success, species, breed, color, sex, bd, idiosync):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "editrecords_patientdetails" and create:
            return [not form, success]
        
        if eventid == "editprofile_patient_submit" and submit and all([species, color, breed, sex, bd, idiosync]):
            return [not form, not success]
        
        if eventid == "editprofile_patient_close_successmodal" and close:
            return [form, not success]
           
    return [form, success]



@app.callback( #modal initial values
    [
        Output('editprofile_patient_m', 'value'),
        Output('editprofile_patient_species', 'value'),
        Output('editprofile_patient_breed', 'value'),
        Output('editprofile_patient_color', 'value'),
        Output('editprofile_patient_sex', 'value'),
        Output('editprofile_patient_bd', 'value'),
        Output('editprofile_patient_idiosync', 'value'),
    ],
    [
        Input('url', 'search'),
        Input('editrecords_patientdetails', 'n_clicks'),
    ],
)
def patientmodal_initial_values(url_search, click):
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'editrecords_patientdetails' and click:
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
            Output('editprofile_patientprofile_alert', 'color'),
            Output('editprofile_patientprofile_alert', 'children'),
            Output('editprofile_patientprofile_alert', 'is_open'),
            Output('editprofile_patient_close_successmodal', 'href')
        ],
        [
            Input('editprofile_patient_submit', 'n_clicks'),
            Input('url', 'search'),
            Input('editprofile_patient_m', 'value'),
            Input('editprofile_patient_species', 'value'),
            Input('editprofile_patient_breed', 'value'),
            Input('editprofile_patient_color', 'value'),
            Input('editprofile_patient_sex', 'value'),
            Input('editprofile_patient_bd', 'value'),
            Input('editprofile_patient_idiosync', 'value'),
        ],
)
def editprofile_patient_save(submitbtn, url_search, name, species, breed, color, sex, bd, idiosync):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'editprofile_patient_submit' and submitbtn: 
            parsed = urlparse(url_search)
            query_patient_id = parse_qs(parsed.query)
            if 'id' in query_patient_id:
                patient_id = query_patient_id['id'][0]
        
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
                    modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
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

                href = f'/editrecord?mode=edit&id={patient_id}&refresh={time.time()}'

                return [alert_color, alert_text, alert_open, href]
            
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    


@app.callback( #callback for save button
    [
        Output('editrecord_successmodal', 'is_open'),
        Output('editrecord_feedback_message', 'children'),
        Output('editrecord_btn_modal', 'href'),
    ],
   
    [
        Input('editrecord_savebtn', 'n_clicks'),
        Input('url', 'search'),
        Input('recordprofile_removerecord', 'value')
    ],
)
def save_record_profile(n_clicks_btn, url_search, removerecord):   
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'id' in query_patient_id:
        patient_id = query_patient_id['id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'editrecord_savebtn' and n_clicks_btn:

                modal_open = False
                modal_text = ''
                modal_href = '#'

                sql = """ 
                        UPDATE patient
                        SET
                            patient_delete_ind = %s
                        WHERE
                            patient_id = %s
                    """
                to_delete = bool(removerecord) 
                values= [to_delete, patient_id]
                
                db.modifydatabase(sql, values)
                
                modal_text = "Changes have been saved successfully."
                modal_href = '/viewrecord'
                modal_open = True
            
                return [modal_open, modal_text, modal_href]
            else:
                raise PreventUpdate
        else: 
            raise PreventUpdate
    else:
        raise PreventUpdate
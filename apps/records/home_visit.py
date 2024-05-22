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
                            ), width = 4),
                        
                        dbc.Col(html.H6("Client not listed?", style={"margin-left": "30px", "margin-right": "-30px"}), width = 2),

                        dbc.Col(
                            dbc.Button(
                                "Create Client Profile",
                                id = "create_client_profile",
                                style={"width":"100%", "backgroundColor": "#333", "borderColor": "#333" , "color": "white"},
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
                        
                        dbc.Col(html.H6("Patient not listed?", style={"margin-left": "30px", "margin-right": "-30px"}), width = 2),

                        dbc.Col(
                            dbc.Button(
                                "Create Patient Profile",
                                id = "create_patient_profile",
                                style={"width":"100%", "backgroundColor": "#333", "borderColor": "#333" , "color": "white"},
                            ), width = 3), 

                    ], style={"margin-left": "2%", "margin-right": "1%", "align-items": "center"}),
                    
                    html.Br(),

                    dbc.Row([ #Select Veterinarian
                            
                        dbc.Col(html.H4("Veterinarian in charge"), width=3),

                        dbc.Col(
                            dcc.Dropdown(
                                id="vetlist",
                                placeholder="Select Veterinarian",
                                searchable=True,
                                options=[],
                                value=None,
                            ),width = 4),
                        
                        dbc.Col(html.H4("Visit Date", style={"margin-left": "30px", "margin-right": "-30px"}), width = 2),
                        
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

                    #html.Br(),
                    html.Hr(),
                    
                    dbc.Row([ #Visit purpose
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
                                    "flex-direction": "row",
                                    "justify-content": "flex-start",
                                    "fontSize": "1rem",
                                    "align-items": "flex-start",
                                },
                            ),
                            width=4, #style={"margin-right": "-15px"}
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
                                    "flex-direction": "row",
                                    "justify-content": "flex-start",
                                    "fontSize": "1rem",
                                    "align-items": "flex-start",
                                },
                            ),
                            width=4, style={"margin-left": "30px", "margin-right": "30px"}
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
                                ), width= 4, 
                            ),
                            dbc.Col(html.H4("Problem status:", style={"margin-left": "30px", "margin-right": "-30px"}), width=2),
                            dbc.Col(html.Div(id = "problem_status"), width=3),

                        ], style={"margin-left": "2%", "margin-right": "1%", "align-items": "center"}),
                    ],id = 'follow_up_field', style = {'display': 'none'}),

                ]),
                
            ]),

        html.Div([ #Client and Patient Information
            
            html.Br(),
            dbc.Row([
                dbc.Col( #Client Information (1st column)
                    dbc.Card([ #Client Information Card
                        dbc.CardHeader(
                            html.Div([
                                    html.H3("Client Information", className = "flex-grow-1"),
                                    dbc.Button("Edit Info", id = 'edit_client_detail_btn', style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, n_clicks = 0),
                                ], className = "d-flex align-items-center justify-content-between"),
                        ),
                        dbc.CardBody(html.Div(id = 'client_content')),
                    ]), width = 5,
                ),
                dbc.Col( #Patient Information (2nd Column)
                    dbc.Card([ #Patient Information Card
                        dbc.CardHeader(
                            html.Div([
                                    html.H3("Patient Information", className = "flex-grow-1"),
                                    dbc.Button("Edit Info", id = 'edit_patient_detail_btn', style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, n_clicks = 0),
                                ], className = "d-flex align-items-center justify-content-between"),
                        ),
                        dbc.CardBody(html.Div(id = 'patient_content')),
                    ]), width = 7,
                ),
            ]),
        ], id = 'client_patient_row', style = {'display': 'none'}),     

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
                dbc.Button("Proceed to Visit Details", href = "", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='home_visit_returnlink', className = "ms-auto"),
            ]),
        ],centered = True, id = 'visitrecord_successmodal', backdrop = 'static', is_open = False, keyboard = False),        



        #CLIENT-RELEATED MODALS

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
                dbc.Button("Submit Client Details", href = "/home_visit", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "client_profile_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "client_profile_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of client profile
            dbc.ModalHeader(html.H4('Client Profile Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                html.A(html.Button("Close", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'close_client_successmodal', className = "btn btn-primary ms-auto"),href = '/home_visit'),
                #dbc.Button("Close", href = "/", id = "close_client_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'client_profile_successmodal', backdrop = 'static', is_open = False, keyboard = False),

        # modal for editing client profile
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Edit Client Profile", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "edit_client_profile_alert", is_open = False),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("First Name", style={"width": "17%"}),
                        dbc.Input(id='edit_client_fn', type='text', placeholder="e.g. Juan"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Last Name", style={"width": "17%"}),
                        dbc.Input(id='edit_client_ln', type='text', placeholder="e.g. Dela Cruz"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Middle Initial", style={"width": "17%"}),
                        dbc.Input(id='edit_client_mi', type='text', placeholder="e.g. M."),
                        dbc.InputGroupText("Suffix", style={"width": "12%"}),
                        dbc.Input(id='edit_client_suffix', type='text', placeholder="e.g. Jr."),
                    ],
                    className="mb-4",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Contact No.", style={"width": "17%"}),
                        dbc.Input(id='edit_client_contact_no', type='text', placeholder="e.g. 09123456789"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Email", style={"width": "17%"}),
                        dbc.Input(id='edit_client_email', type='text', placeholder="e.g. Juan.DelaCruz@example.com"),
                    ],
                    className="mb-4",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("House No.", style={"width": "17%"}),
                        dbc.Input(id='edit_client_house_no', type='text', placeholder="e.g. No. 1A (or any landmark)"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Street", style={"width": "17%"}),
                        dbc.Input(id='edit_client_street', type='text', placeholder="e.g. P. Vargas St."),
                        dbc.InputGroupText("Barangay", style={"width": "12%"}),
                        dbc.Input(id='edit_client_barangay', type='text', placeholder="e.g. Krus na Ligas"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("City", style={"width": "17%"}),
                        dbc.Input(id='edit_client_city', type='text', placeholder="e.g. Pasay City"),
                        dbc.InputGroupText("Region", style={"width": "12%"}),
                        dbc.Input(id='edit_client_region', type='text', placeholder="e.g. Metro Manila"),
                    ],
                    #className="mb-3",
                ),
            ]),
            dbc.ModalFooter([
                #dbc.Button("Submit Modified Client Details", href = "/home_visit", id = "edit_client_profile_submit", className = "ms-auto"),
                dbc.Button("Submit Modified Client Details", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "edit_client_profile_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "edit_client_profile_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful editing of client profile
            dbc.ModalHeader(html.H4('Client Profile Edited Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                #html.A(html.Button("Close", id = 'close_edit_client_successmodal', className = "btn btn-primary ms-auto")),
                html.A(html.Button("Close", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'close_edit_client_successmodal', className = "btn btn-primary ms-auto"),href = '/home_visit'),
                #dbc.Button("Close", href = "/", id = "close_client_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'edit_client_profile_successmodal', backdrop = 'static', is_open = False, keyboard = False),



        #PATIENT-RELATED MODALS

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
                dbc.Button("Submit Patient Details", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "patient_profile_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "patient_profile_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of patient profile
            dbc.ModalHeader(html.H4('Patient Profile Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                html.A(html.Button("Close", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'close_patient_successmodal', className = "btn btn-primary ms-auto"),href = '/home_visit'),
                #dbc.Button("Close", id = "close_patient_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'patient_profile_successmodal', backdrop = 'static', is_open = False, keyboard = False),
    
        # modal for editing patient profile
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Edit Patient Profile", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "edit_patient_profile_alert", is_open = False),
                
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Name", style={"width": "17%"}),
                        dbc.Input(id='edit_patient_m', type='text', placeholder="e.g. Bantay (leave blank if none)"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Species", style={"width": "17%"}),
                        dbc.Input(id='edit_patient_species', type='text', placeholder="e.g. Dog"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Breed", style={"width": "17%"}),
                        dbc.Input(id='edit_patient_breed', type='text', placeholder="e.g. Bulldog"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Color Marks", style={"width": "17%"}),
                        dbc.Input(id='edit_patient_color', type='text', placeholder="e.g. White or With black spots"),
                    ],
                    className="mb-2",
                ),

                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Sex", style={"width": "17%"}),                            
                        dbc.InputGroupText(dcc.Dropdown(
                            id='edit_patient_sex',
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
                            id='edit_patient_bd',
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
                        dbc.Input(id='edit_patient_idiosync', type='text', placeholder="e.g. Likes morning walks"),
                    ],
                    #className="mb-3",
                ),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Modified Patient Details", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = "edit_patient_profile_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "edit_patient_profile_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful editing of patient profile
            dbc.ModalHeader(html.H4('Patient Profile Edited Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                html.A(html.Button("Close", style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id = 'close_edit_patient_successmodal', className = "btn btn-primary ms-auto"),href = '/home_visit'),
                #dbc.Button("Close", id = "close_patient_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'edit_patient_profile_successmodal', backdrop = 'static', is_open = False, keyboard = False),

    ])





# CLIENT-RELATED

@app.callback( # for list of existing clients for returning patient
    [
        Output('re_clientlist', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('re_clientlist', 'value'),
        Input('patientlist', 'value'),
    ]
)
def re_clientlist(pathname, searchterm, patient):
    if patient:
        sql = """
            SELECT
                client_id
            FROM
                patient
            WHERE
                patient_id = %s
            """
        values = [patient]
        df = db.querydatafromdatabase(sql,values)     
        client_id = int(df.loc[0,0])

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

        if patient:
            sql += """
                AND client_id = %s
            """
            values.append(client_id)
            
        if searchterm:
            sql += """ AND (
                client_ln ILIKE %s 
                OR client_fn ILIKE %s
                );
            """
            values.extend([f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"])

        sql += " ORDER BY client_name;"

        cols = ['client_id', 'client_name']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['client_name'], 'value': row['client_id']} for _, row in result.iterrows()]

        return options, 
    else:
        raise PreventUpdate  

@app.callback( # Submit Button for new client profile
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

@app.callback( #form and success modal for create client profile
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

@app.callback( # fill edit client modal
    [
        Output('edit_client_ln', 'value'),
        Output('edit_client_fn', 'value'),
        Output('edit_client_mi', 'value'),
        Output('edit_client_suffix', 'value'),
        Output('edit_client_contact_no', 'value'),
        Output('edit_client_email', 'value'),
        Output('edit_client_house_no', 'value'),
        Output('edit_client_street', 'value'),
        Output('edit_client_barangay', 'value'),
        Output('edit_client_city', 'value'),
        Output('edit_client_region', 'value'),
    ],
    [
        Input('re_clientlist', 'value'),
    ],
)
def edit_client_profile(client): 
    if not client:
        return [None, None, None, None, None, None, None, None, None, None, None]
    else: 
        sql = """ 
            SELECT 
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
                client_region
            FROM 
                client
            WHERE 
                NOT client_delete_ind and client_id = %s
            """
        values = [client]
        cols = ['ln', 'fn', 'mi', 'sfx', 'email', 'cn', 'hn', 'street', 'brgy', 'city', 'region']
        df = db.querydatafromdatabase(sql,values, cols)

        ln = df['ln'][0]
        fn = df['fn'][0]
        mi = df['mi'][0]
        sfx = df['sfx'][0]
        email = df['email'][0]
        cn = df['cn'][0]
        hn = df['hn'][0]
        street = df['street'][0]
        brgy = df['brgy'][0]
        city = df['city'][0]
        region = df['region'][0]
        
        return [ln, fn, mi, sfx, cn, email, hn, street, brgy, city, region]

@app.callback( # Submit Button for edit client profile
    [
        Output('edit_client_profile_alert', 'color'),
        Output('edit_client_profile_alert', 'children'),
        Output('edit_client_profile_alert', 'is_open'),
    ],
    [
        Input('edit_client_profile_submit', 'n_clicks'),
        Input('edit_client_fn', 'value'),
        Input('edit_client_ln', 'value'),
        Input('edit_client_mi', 'value'),
        Input('edit_client_suffix', 'value'),
        Input('edit_client_contact_no', 'value'),
        Input('edit_client_email', 'value'),
        Input('edit_client_house_no', 'value'),
        Input('edit_client_street', 'value'),
        Input('edit_client_barangay', 'value'),
        Input('edit_client_city', 'value'),
        Input('edit_client_region', 'value'),
        Input('re_clientlist', 'value'),
    ],
)
def edit_client_profile_save(submitbtn, fn, ln, mi, sf, cn, email, house_no, street, brgy, city, region, client_id):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        alert_open = False
        alert_color = ''
        alert_text = ''

        if eventid == 'edit_client_profile_submit' and submitbtn:

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
                    client_region = %s
                WHERE
                    client_id = %s;
                '''
                values = [ln, fn, mi, sf, email, cn, house_no, street, brgy, city, region, client_id]

                db.modifydatabase(sql, values)

            if not all([fn, ln, cn, email, street, brgy, city, region]):
                return [alert_color, alert_text, alert_open]

            return [alert_color, alert_text, alert_open]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback( #form and success modal for edit client profile
        [
            Output("edit_client_profile_modal", "is_open"),
            Output('edit_client_profile_successmodal', 'is_open'),
        ],
        [
            Input("edit_client_detail_btn", "n_clicks"),
            Input('edit_client_profile_submit','n_clicks'),
            Input('close_edit_client_successmodal','n_clicks'),
        ],
        [
            State("edit_client_profile_modal", "is_open"),
            State('edit_client_profile_successmodal', 'is_open'),
            State('edit_client_fn', 'value'),
            State('edit_client_ln', 'value'),
            State('edit_client_contact_no', 'value'),
            State('edit_client_email', 'value'),
            State('edit_client_street', 'value'),
            State('edit_client_barangay', 'value'),
            State('edit_client_city', 'value'),
            State('edit_client_region', 'value'),
        ]
)
def toggle_edit_client_profile_modal(edit, submit, close, form, success, fn, ln, cn, email, street, brgy, city, region):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "edit_client_detail_btn" and edit:
            return [not form, success]
        
        if eventid == 'edit_client_profile_submit' and submit and all([fn, ln, cn, email, street, brgy, city, region]):
            return [not form, not success]
        
        if eventid == 'close_edit_client_successmodal' and close:
            return [form, not success]
        
    return [form, success]





# PATIENT-RELATED

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
            client_id = int(selected_client_id)
            sql += """ 
                AND client_id = %s
            """
            values.append(client_id)

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

@app.callback( #callback for list of existing clients for new patient
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

@app.callback( #form and success modal for create patient profile
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

@app.callback( # fill edit patient modal
    [
        Output('edit_patient_m', 'value'),
        Output('edit_patient_species', 'value'),
        Output('edit_patient_breed', 'value'),
        Output('edit_patient_color', 'value'),
        Output('edit_patient_sex', 'value'),
        Output('edit_patient_bd', 'date'),
        Output('edit_patient_idiosync', 'value'),
    ],
    [
        Input('patientlist', 'value'),
    ],
)
def edit_patient_profile(patient): 
    if not patient:
        return [None, None, None, None, None, None, None]
    else: 
        sql = """
            SELECT
                patient_m,
                patient_species,
                patient_breed,
                patient_color,
                patient_sex,
                TO_CHAR(patient_bd, 'Mon DD, YYYY'),
                patient_idiosync
            FROM
                patient
            WHERE
                NOT patient_delete_ind and patient_id = %s
        """
        values = [patient]
        cols = ['patient_name', 'species', 'breed', 'color', 'sex', 'bd', 'idiosync']
        df = db.querydatafromdatabase(sql,values, cols)

        name = df['patient_name'][0]
        species = df['species'][0]
        breed = df['breed'][0]
        color = df['color'][0]
        sex = df['sex'][0]
        bd = df['bd'][0]
        idiosync = df['idiosync'][0]
        
        return [name, species, breed, color, sex, bd, idiosync]

@app.callback( # Submit Button for patient edit profile
    [
        Output('edit_patient_profile_alert', 'color'),
        Output('edit_patient_profile_alert', 'children'),
        Output('edit_patient_profile_alert', 'is_open'),
    ],
    [
        Input('edit_patient_profile_submit', 'n_clicks'),
        Input('edit_patient_m', 'value'),
        Input('edit_patient_species', 'value'),
        Input('edit_patient_breed', 'value'),
        Input('edit_patient_color', 'value'),
        Input('edit_patient_sex', 'value'),
        Input('edit_patient_bd', 'date'),
        Input('edit_patient_idiosync', 'value'),
        Input('patientlist', 'value'),
    ]
)
def edit_patient_profile_save(submitbtn, name, species, breed, color, sex, bd, idiosync, patient):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        alert_open = False
        alert_color = ''
        alert_text = ''

        if eventid == 'edit_patient_profile_submit' and submitbtn:

            if not name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please indicate the name of the patient. If none, type N/A'
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
                UPDATE patient
                SET
                    patient_m = %s,
                    patient_species = %s,
                    patient_color = %s,
                    patient_breed = %s,
                    patient_sex = %s,
                    patient_bd = %s,
                    patient_idiosync = %s
                WHERE
                    patient_id = %s
                    '''
                values = [name, species, color, breed, sex, bd, idiosync, patient]

                db.modifydatabase(sql, values)

            if not all([name, species, color, breed, sex, bd, idiosync]):
                return [alert_color, alert_text, alert_open]
            
            return [alert_color, alert_text, alert_open]
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback( #form and success modal for create patient profile
        [
            Output("edit_patient_profile_modal", "is_open"),
            Output('edit_patient_profile_successmodal', 'is_open'),
        ],
        [
            Input("edit_patient_detail_btn", "n_clicks"),
            Input('edit_patient_profile_submit','n_clicks'),
            Input('close_edit_patient_successmodal','n_clicks'),
        ],
        [
            State("edit_patient_profile_modal", "is_open"),
            State('edit_patient_profile_successmodal', 'is_open'),
            State('edit_patient_species', 'value'),
            State('edit_patient_breed', 'value'),
            State('edit_patient_color', 'value'),
            State('edit_patient_sex', 'value'),
            State('edit_patient_bd', 'date'),
            State('edit_patient_idiosync', 'value'),
        ]
)
def toggle_edit_patient_profile_modal(create, submit, close, form, success, species, breed, color, sex, bd, idiosync):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "edit_patient_detail_btn" and create:
            return [not form, success]
        
        if eventid == "edit_patient_profile_submit" and submit and all([species, color, breed, sex, bd, idiosync]):
            return [not form, not success]
        
        if eventid == "close_edit_patient_successmodal" and close:
            return [form, not success]
           
    return [form, success]





# VET-RELATED

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






# VISIT-RELATED

@app.callback( # Submit Button for visit
    [
        Output('home_visit_returnlink', 'href'),
        Output('visitrecord_alert','color'),
        Output('visitrecord_alert','children'),
        Output('visitrecord_alert','is_open'),
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
def visitrecord_save(submitbtn, client, patient_id, vet, date, prev_prob, vacc_deworm, prob):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        link = ""
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
            new_problem = 'new_problem' in prob_purpose
            follow_and_problem = follow_up == any([prev_prob])
            visit_for_problem = len(prob_purpose) == 1
   
            if not client:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please choose a client'
            elif not patient_id:
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
            elif not follow_and_problem and not new_problem:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Please select the previous problem or tick the 'Follow up to a problem' for this follow-up visit"
            elif not follow_and_problem and new_problem:
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
                values = [patient_id, vet, visit_for_vacc, visit_for_deworm, visit_for_problem, False]
                db.modifydatabase(sql, values)    
                link = f'/home_visit/purpose?mode=add&patient_id={patient_id}'

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
                values = [patient_id, vet, visit_for_vacc, visit_for_deworm, visit_for_problem, prev_prob, False]
                db.modifydatabase(sql, values)
                link = f'/home_visit/purpose?mode=add&patient_id={patient_id}'
            
            if not all([client, patient_id, vet, date, any([follow_and_problem, new_problem]), any([visit_for_problem, visit_for_deworm, visit_for_vacc])]):
                #return [alert_color, alert_text, alert_open, client, patient, vet, date, prev_prob]
                return [link, alert_color, alert_text, alert_open]

            return [link, alert_color, alert_text, alert_open]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback( #visit success modal
    [
        Output('visitrecord_successmodal','is_open'),
    ],
    [
        Input('visitrecord_submit','n_clicks'),
    ],
    [
        State('visitrecord_successmodal','is_open'),
        State('re_clientlist', 'value'),
        State('patientlist','value'),
        State('vetlist','value'),
        State('visitdate', 'value'),
        State('problem_list', 'value'),
        State('visitpurpose', 'value'),
        State('visitpurpose_problem', 'value'),
    ]
)
def toggle_visit_success_modal(visit_btn, visit_success, client, patient, vet, date, prev_prob, vacc_deworm, prob):
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
        follow_up = 'follow_up' in prob_purpose
        new_problem = 'new_problem' in prob_purpose
        follow_and_problem = follow_up == any([prev_prob])
        visit_for_problem = len(prob_purpose) == 1


        if eventid == "visitrecord_submit" and visit_btn and all([client, patient, vet, date, any([follow_and_problem, new_problem]), any([visit_for_problem, visit_for_deworm, visit_for_vacc])]):
            return [not visit_success]
        
    return [visit_success]

@app.callback( #going to visit purpose page
    [
        #Output('home_visit_returnlink', 'href'),
        Output('re_clientlist', 'value'),
        Output('patientlist','value'),
        Output('vetlist','value'),
        Output('visitdate', 'value'),
        Output('problem_list', 'value'),
    ],
    Input('home_visit_returnlink', 'n_clicks'),
    State('patientlist','value'),
)
def returnlink(clicks, patient_id):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'home_visit_returnlink' and clicks:
            #link = f'/home_visit/purpose?mode=add&patient_id={patient_id}'
            #return [link, None, None, None, datetime.now().date(), None]
            return [None, None, None, datetime.now().date(), None]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate



# PROBLEM-RELATED

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

@app.callback( #list of problems for follow up 
    [
        Output('problem_list', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('problem_list', 'value'),
        Input('re_clientlist', 'value'),
        Input('patientlist', 'value'),
    ],
)
def problem_list_reCreP(pathname, searchterm, selected_client_id, selected_patient_id):
    if pathname == "/home_visit"  and not searchterm and selected_client_id and selected_patient_id:
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
                AND patient_id = %s
            """
        values = [selected_patient_id]
        
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

@app.callback( #Update problem status placeholder
        Output('problem_status', 'children'),
        Input('problem_list', 'value'),
        State('problem_list', 'value')
)
def problem_status(_, problem):
    if problem:
        sql = """
            SELECT
                s.problem_status_m
            FROM problem p JOIN problem_status s
            ON p.problem_status_id = s.problem_status_id
            WHERE NOT p.problem_delete_ind and p.problem_id = %s
        """
        values = [problem]
        df = db.querydatafromdatabase(sql, values)
        status = df.loc[0,0]
        return html.H4(f'{status}')
    else:
        return html.H4("")
     




# ADDITIONAL ROW - CLIENT + PATIENT PROFILE

@app.callback( # to show the client patient row
    [
        Output('client_patient_row', 'style')
    ],
    [
        Input('re_clientlist', 'value'),
        Input('patientlist', 'value'),
    ],
)
def client_patient_row_view(client, patient):
    if client and patient:
        return [{'display': 'block'}]
    else:
        return [{'display': 'none'}]

@app.callback( # profile content callbacks
    [
        Output('patient_content', 'children'),
        Output('client_content', 'children'),
    ],
    [
        Input('re_clientlist', 'value'),
        Input('patientlist', 'value'),
    ],
)
def client_patient(client, patient):

    client_content = []  
    patient_content = [] 

    if not client or not patient:
        return [patient_content, client_content]
    
    else:
        # RETRIEVE INFO FOR PATIENT
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
        values = [patient]
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
    
        if patient:
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
        values = [client]
        cols = ['client_name', 'email', 'cn', 'add1', 'add2']
        df = db.querydatafromdatabase(sql,values, cols)

        client_name = df['client_name'][0]
        client_email = df['email'][0]
        client_cn = df['cn'][0]
        client_add1 = df['add1'][0]
        client_add2 = df['add2'][0]
    
        if client:
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

        return [patient_content, client_content]





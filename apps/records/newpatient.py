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

layout = html.Div(
    [
        html.H1("New Patient"),
        html.Hr(),
        dbc.Alert(id='newpatientprofile_alert', is_open=False), # For feedback purposes
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Owner Information")
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Last Name"),
                                        dbc.Input(id='client_ln', type='text', placeholder='Enter Last Name', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("First Name"),
                                        dbc.Input(id='client_fn', type='text', placeholder='Enter First Name', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Middle Initial"),
                                        dbc.Input(id='client_mi', type='text', placeholder='Enter Middle Initial', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Suffix (N/A if none)"),
                                        dbc.Input(id='client_suffix', type='text', placeholder='Enter Suffix', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ), # end of row for owner name
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Email Address"),
                                        dbc.Input(id='client_email', type='text', placeholder='Enter Email Address', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Contact Number"),
                                        dbc.Input(id='client_cn', type='text', placeholder='Enter Contact Number', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Province"),
                                        dbc.Input(id='client_province', type='text', placeholder='Enter Province', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("City"),
                                        dbc.Input(id='client_city', type='text', placeholder='Enter City', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ), # end of row of email address, contact num, province
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Barangay"),
                                        dbc.Input(id='client_barangay', type='text', placeholder='Enter Barangay', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Street"),
                                        dbc.Input(id='client_street', type='text', placeholder='Enter Street', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("House Number"),
                                        dbc.Input(id='client_house_no', type='text', placeholder='Enter House Number', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ) # end of address row part 2
                    ],
                )
            ],
            style={'width':'100%'}
        ), # end of card for owner information
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Patient Information")
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Name"),
                                        dbc.Input(id='patient_m', type='text', placeholder='Enter Patient Name', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Sex"),
                                        dcc.Dropdown(
                                            id='patient_sex',
                                            options=[
                                                {'label':'Male', 'value':'Male'},
                                                {'label':'Female', 'value':'Female'},
                                            ],
                                            placeholder='Select Sex',
                                            style={'width':'86.5%'},
                                        ),
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Type"),
                                        dbc.Input(id='patient_type', type='text', placeholder='Enter Type', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Breed"),
                                        dbc.Input(id='patient_breed', type='text', placeholder='Enter Breed', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ), # end of row for name, sex, breed
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Birthdate"),
                                        dmc.DatePicker(
                                            id='patient_bd',
                                            placeholder="Select Birthdate",
                                            style={'width':'75%'},
                                            inputFormat='MMM DD, YYYY',
                                            dropdownType='modal',
                                        ),
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Idiosyncrasies"),
                                        dbc.Input(id='patient_idiosync', type='text', placeholder='Enter Idiosyncrasies', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Color Markings"),
                                        dbc.Input(id='patient_color', type='text', placeholder='Enter Color Markings', style={'width':'75%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ), # end of row for birthdate, idiosyncrasies, color markings
                    ],  
                ) 
            ],
            style={'width':'100%'}
        ), # end of card for patient information    
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Vaccination and Deworming Details")
                    ]
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(html.H3("Vaccination"), width=2),
                        dbc.Col(dbc.Button("+", id='vaccine-addbutton', className='custom-button', n_clicks=0), width=2),
                        dbc.Col(dbc.Button("-", id='vaccine-deletebutton', className='custom-button', n_clicks=0), width=2),
                    ]),
                    html.Div(id='vaccine-line-items'),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.H3("Deworming"), width=2),
                        dbc.Col(dbc.Button("+", id='deworming-addbutton', className='custom-button', n_clicks=0), width=2),
                        dbc.Col(dbc.Button("-", id='deworming-deletebutton', className='custom-button', n_clicks=0), width=2),
                    ]),
                    html.Div(id='deworming-line-items'),
                ]),
            ],
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Visit Information")
                    ]
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(html.H3("Select Veterinarian"), width=3),
                        dbc.Col(
                                dcc.Dropdown(
                                    id="vetlist_newpatient",
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
                                id='visitdate_newpatient',
                                placeholder="Select Visit Date",
                                value=datetime.datetime.now().date(),
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
                                    {"label": " Vaccination", "style":{"flex-grow": 1}, "value": "vaccination"},
                                    {"label": " Deworming", "style":{"flex-grow": 1}, "value": "deworming"},
                                ],
                                id="visitpurpose_newpatient",
                                inline=True,
                                style={"display": "flex", 
                                    "justify-content": "space-between", 
                                    "fontSize":"1.2rem",
                                    "align-items":"center"},
                            ),
                            width=6,
                        )
                    ]),
                ]),
            ],
        ),
        html.Div(id="visitinputs_newpatient"),
        html.Br(),
        dbc.Button(
            'Submit',
            id = 'newpatientprofile_submit',
            n_clicks = 0, #initialization 
            className='custom-submitbutton',
        ),
        dbc.Modal( # dialog box for successful saving of profile
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    'Edit this message',
                    id = 'newpatientprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Submit",
                        href = '/home', # bring user back to homepage
                        id = 'newpatientprofile_btn_modal',
                    )                    
                )
            ],
            centered=True,
            id='newpatientprofile_successmodal',
            backdrop='static' # dialog box does not go away if you click at the background

        )
    ]
)



vaccine_line_items = []
deworming_line_items = []

@app.callback( #callback for adding a row for vaccines administered
    [
        Output("vaccine-line-items", "children"),
    ],
    [
        Input("vaccine-addbutton", "n_clicks"),
        Input("vaccine-deletebutton", "n_clicks"),
    ],
)
def manage_vaccine_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "vaccine-addbutton" in triggered_id:
        if len(vaccine_line_items) < addclick:
            i = len(vaccine_line_items)
            vaccine_line_items.extend([
                html.Div([
                    html.Div(style={'height':'5px'}),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id={"type": "patient_vaccine_newpatient", "index": i},
                                placeholder='Select Vaccine',
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                            width = 4,
                        ),
                        dbc.Col(
                            dbc.Input(id={"type": "vaccine_dose_newpatient", "index": i}, type='text', placeholder='Enter Dose'),
                            width=2,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "vaccine_date_newpatient", "index": i},
                                placeholder="Select Date Administered",
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                            ),
                            width = 3,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "vaccine_expdate_newpatient", "index": i},
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

    elif triggered_id and "vaccine-deletebutton" in triggered_id:
        if len(vaccine_line_items) > 0:
            vaccine_line_items.pop()
    
    else:
        raise PreventUpdate
    
    return [vaccine_line_items]


@app.callback( #callback for adding a row for deworming medicines administered
    [
        Output("deworming-line-items", "children"),
    ],
    [
        Input("deworming-addbutton", "n_clicks"),
        Input("deworming-deletebutton", "n_clicks"),
    ],
)
def manage_deworming_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "deworming-addbutton" in triggered_id:
        if len(deworming_line_items) < addclick:
            i = len(deworming_line_items)
            deworming_line_items.extend([
                html.Div([
                    html.Div(style={'height':'5px'}),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id={"type": "patient_deworming_newpatient", "index": i},
                                placeholder='Select Deworming Medicine Used',
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                            width = 4,
                        ),
                        dbc.Col(
                            dbc.Input(id={"type": "deworm_dose_newpatient", "index": i}, type='text', placeholder='Enter Dose'),
                            width = 2,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "deworming_date_newpatient", "index": i},
                                placeholder="Select Date Administered",
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                            ),
                            width = 3,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "deworming_expdate_newpatient", "index": i},
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

    elif triggered_id and "deworming-deletebutton" in triggered_id:
        if len(deworming_line_items) > 0:
            deworming_line_items.pop()

    else:
        raise PreventUpdate

    return [deworming_line_items]


@app.callback( #callback to provide the list of vaccines on the dropdown
    [
        Output({"type": "patient_vaccine_newpatient", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "patient_vaccine_newpatient", "index": MATCH}, "value"),
    ]
)
def newpatient_loadvaccines(pathname, searchterm):
    if pathname == "/newrecord/newpatient" and not searchterm:
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
        Output({"type": "patient_deworming_newpatient", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "patient_deworming_newpatient", "index": MATCH}, 'value'),
    ]
)
def newpatient_loaddeworm(pathname, searchterm):
    if pathname == "/newrecord/newpatient" and not searchterm:
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


@app.callback( #callback to provide the list of veterinarians
    [
        Output('vetlist_newpatient', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('vetlist_newpatient', 'value'),
    ]
)
def newvisit_loadvet(pathname, searchterm):
    if pathname == "/newrecord/newpatient" and not searchterm:
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



@app.callback( #callback to add inputs depending on the selected visit purpose
    Output("visitinputs_newpatient", "children"),
    Input("visitpurpose_newpatient", "value"),
    State("visitpurpose_newpatient", "value"),
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
                                    dbc.Col(dbc.Button("+", id='vaccine-addbutton_newpatient', className='custom-button', n_clicks=0), width=2),
                                    dbc.Col(dbc.Button("-", id='vaccine-deletebutton_newpatient', className='custom-button', n_clicks=0), width=2),
                                ]),
                            ]
                        ),
                        dbc.CardBody([
                            html.Div(id='vaccine-line-items_visit'),
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
                                    dbc.Col(dbc.Button("+", id='deworming-addbutton_newpatient', className='custom-button', n_clicks=0), width=2),
                                    dbc.Col(dbc.Button("-", id='deworming-deletebutton_newpatient', className='custom-button', n_clicks=0), width=2),
                                ]),
                            ]
                        ),
                        dbc.CardBody([
                            html.Div(id='deworming-line-items_visit'),
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
                                    dbc.Input(id="problem_newpatient", type='text', placeholder='Enter Problem'),
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Health & food intake"), width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Relevant Medical History"),
                                        dbc.Textarea(id='problem_medhistory', placeholder='Enter Any Relevant Medical History', style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Diet"),
                                        dbc.Textarea(id='problem_diet', placeholder="Enter Patient's Diet", style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Water Source"),
                                        dbc.Textarea(id='problem_water', placeholder="Enter Patient's Water Source", style={"height":75})
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
                                        dbc.Input(id='problem_temp', type='text', placeholder='Enter Temperature')
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Pulse Rate"),
                                        dbc.Input(id='problem_pr', type='text', placeholder="Enter Pulse Rate")
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Respiration Rate"),
                                        dbc.Input(id='problem_rr', type='text', placeholder="Enter Respiration Rate")
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
                                        dbc.Input(id='problem_weight', type='text', placeholder='Enter Weight')
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Body Condition Score"),
                                        dbc.Input(id='problem_bodyconditionscore', type='text', placeholder="Enter Body Condition Score")
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
                                        dbc.Textarea(id='note_differentialdiagnosis', placeholder='Enter Differential Diagnosis', style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Possible Treatment"),
                                        dbc.Textarea(id='note_treatment', placeholder='Enter Treatment Options', style={"height":75})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Tests Needed"),
                                        dbc.Textarea(id='note_tests', placeholder='Enter Tests Needed', style={"height":75})
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
                                            id="note_havebeentested",
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
                                        dbc.Input(id='note_OR_no', type='text', placeholder="Enter OR Number")
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Bill"),
                                        dbc.Input(id='note_bill', type='text', placeholder="Enter Bill")
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Clinical Exam"), width=3),
                                dbc.Col(dbc.Button("+", id='clinicalexam-addbutton-newpatient', className='custom-button', n_clicks=0), width=2),
                                dbc.Col(dbc.Button("-", id='clinicalexam-deletebutton-newpatient', className='custom-button', n_clicks=0), width=2),
                            ]),
                            html.Div(id='clinicalexam-lineitems-newpatient'),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Laboratory Exam"), width=3),
                                dbc.Col(dbc.Button("+", id='labexam-addbutton-newpatient', className='custom-button', n_clicks=0), width=2),
                                dbc.Col(dbc.Button("-", id='labexam-deletebutton-newpatient', className='custom-button', n_clicks=0), width=2),
                            ]),
                            html.Div(id='labexam-lineitems-newpatient'),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Diagnosis & Prescription"), width=3),
                                dbc.Col(
                                    [
                                        dbc.Label("Diagnosis"),
                                        dbc.Textarea(id='problem_diagnosis', placeholder='Enter Diagnosis', style={"height":100})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Prescription"),
                                        dbc.Textarea(id='problem_prescription', placeholder="Enter Prescription", style={"height":100})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Patient instructions"),
                                        dbc.Textarea(id='problem_clienteduc', placeholder="Enter instructions", style={"height":100})
                                    ],
                                    width=3
                                ),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H3("Problem Status"), width=3),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='problem_status',
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


vaccine_lineitem_newpatient = []
deworming_lineitem_newpatient = []

@app.callback( #callback for adding a row for vaccines administered
    [
        Output("vaccine-line-items_visit", "children"),
    ],
    [
        Input("vaccine-addbutton_newpatient", "n_clicks"),
        Input("vaccine-deletebutton_newpatient", "n_clicks"),
    ],
)
def manage_vaccine_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "vaccine-addbutton_newpatient" in triggered_id:
        if len(vaccine_lineitem_newpatient) < addclick:
            i = len(vaccine_lineitem_newpatient)
            vaccine_lineitem_newpatient.extend([
                html.Div([
                    html.Div(style={'height':'5px'}),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id={"type": "patient_vaccine_newpatient-visit", "index": i},
                                placeholder='Select Vaccine',
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                            width = 4,
                        ),
                        dbc.Col(
                            dbc.Input(id={"type": "vaccine_dose_newpatient-visit", "index": i}, type='text', placeholder='Enter Dose'),
                            width = 2,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "vaccine_date_newpatient-visit", "index": i},
                                placeholder="Select Date Administered",
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                            ),
                            width = 3,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "vaccine_expdate_newpatient-visit", "index": i},
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

    elif triggered_id and "vaccine-deletebutton_newpatient" in triggered_id:
        if len(vaccine_lineitem_newpatient) > 0:
            vaccine_lineitem_newpatient.pop()
    
    else:
        raise PreventUpdate
    
    return [vaccine_lineitem_newpatient]


@app.callback( #callback for adding a row for deworming medicines administered
    [
        Output("deworming-line-items_visit", "children"),
    ],
    [
        Input("deworming-addbutton_newpatient", "n_clicks"),
        Input("deworming-deletebutton_newpatient", "n_clicks"),
    ],
)
def manage_deworming_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "deworming-addbutton_newpatient" in triggered_id:
        if len(deworming_lineitem_newpatient) < addclick:
            i = len(deworming_lineitem_newpatient)
            deworming_lineitem_newpatient.extend([
                html.Div([
                    html.Div(style={'height':'5px'}),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id={"type": "patient_deworming_newpatient-visit", "index": i},
                                placeholder='Select Deworming Medicine Used',
                                searchable=True,
                                options=[],
                                value=None,
                            ),
                            width = 4,
                        ),
                        dbc.Col(
                            dbc.Input(id={"type": "deworm_dose_newpatient-visit", "index": i}, type='text', placeholder='Enter Dose'),
                            width = 2,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "deworming_date_newpatient-visit", "index": i},
                                placeholder="Select Date Administered",
                                inputFormat='MMM DD, YYYY',
                                dropdownType='modal',
                            ),
                            width = 3,
                        ),
                        dbc.Col(
                            dmc.DatePicker(
                                id={"type": "deworming_expdate_newpatient-visit", "index": i},
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

    elif triggered_id and "deworming-deletebutton_newpatient" in triggered_id:
        if len(deworming_lineitem_newpatient) > 0:
            deworming_lineitem_newpatient.pop()

    else:
        raise PreventUpdate

    return [deworming_lineitem_newpatient]


@app.callback( #callback to provide the list of vaccines on the dropdown
    [
        Output({"type": "patient_vaccine_newpatient-visit", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "patient_vaccine_newpatient-visit", "index": MATCH}, "value"),
    ]
)
def newpatient_loadvaccines(pathname, searchterm):
    if pathname == "/newrecord/newpatient" and not searchterm:
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
        Output({"type": "patient_deworming_newpatient-visit", "index": MATCH}, 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "patient_deworming_newpatient-visit", "index": MATCH}, 'value'),
    ]
)
def newpatient_loaddeworm(pathname, searchterm):
    if pathname == "/newrecord/newpatient" and not searchterm:
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



clinicalexam_lineitem_newpatient = []
labexam_lineitem_newpatient = []

@app.callback( #callback for adding a row for clinical exam line items
    [
        Output("clinicalexam-lineitems-newpatient", "children"),
    ],
    [
        Input("clinicalexam-addbutton-newpatient", "n_clicks"),
        Input("clinicalexam-deletebutton-newpatient", "n_clicks"),
    ],
)
def manage_clinicalexam_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "clinicalexam-addbutton-newpatient" in triggered_id:
        if len(clinicalexam_lineitem_newpatient) < addclick:
            i = len(clinicalexam_lineitem_newpatient)
            clinicalexam_lineitem_newpatient.extend([
                html.Div([
                    html.Hr(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Clinician"),
                            dcc.Dropdown(
                                id={"type": "clinicianlist_newpatient", "index": i},
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
                                id={"type": "clinicalexamlist_newpatient", "index": i},
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
                                id={"type": "clinicalfindings_newpatient", "index": i},
                                placeholder="Enter Findings",
                                style={'width':'100%', 'height':100}
                            ),
                        ]),
                    ]),
                    html.Br(),
                ])
            ]) 

    elif triggered_id and "clinicalexam-deletebutton-newpatient" in triggered_id:
        if len(clinicalexam_lineitem_newpatient) > 0:
            clinicalexam_lineitem_newpatient.pop()

    else:
        raise PreventUpdate

    return [clinicalexam_lineitem_newpatient]


@app.callback( #callback for adding a row for lab exam line items
    [
        Output("labexam-lineitems-newpatient", "children"),
    ],
    [
        Input("labexam-addbutton-newpatient", "n_clicks"),
        Input("labexam-deletebutton-newpatient", "n_clicks"),
    ],
)
def manage_labexam_line_item(addclick, deleteclick):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id and "labexam-addbutton-newpatient" in triggered_id:
        if len(labexam_lineitem_newpatient) < addclick:
            i = len(labexam_lineitem_newpatient)
            labexam_lineitem_newpatient.extend([
                html.Div([
                    html.Hr(),
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            dbc.Label("Veterinarian In Charge"),
                            dcc.Dropdown(
                                id={"type": "vetexaminerlist_newpatient", "index": i},
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
                                id={"type": "labexamlist_newpatient", "index": i},
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
                                id={"type": "labfindings_newpatient", "index": i},
                                placeholder="Enter Findings",
                                style={'width':'100%', 'height':100}
                            ),
                        ]),
                    ]),
                    html.Br(),
                ])
            ]) 

    elif triggered_id and "labexam-deletebutton-newpatient" in triggered_id:
        if len(labexam_lineitem_newpatient) > 0:
            labexam_lineitem_newpatient.pop()

    else:
        raise PreventUpdate

    return [labexam_lineitem_newpatient]


@app.callback( #callback to provide the list of clinicians on the dropdown
    [
        Output({"type": "clinicianlist_newpatient", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "clinicianlist_newpatient", "index": MATCH}, "value"),
    ]
)
def newpatient_loadclinicians(pathname, searchterm):
    if pathname == "/newrecord/newpatient" and not searchterm:
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
        Output({"type": "clinicalexamlist_newpatient", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "clinicalexamlist_newpatient", "index": MATCH}, "value"),
    ]
)
def newpatient_loadclinicalexam(pathname, searchterm):
    if pathname == "/newrecord/newpatient" and not searchterm:
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
        Output({"type": "vetexaminerlist_newpatient", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "vetexaminerlist_newpatient", "index": MATCH}, "value"),
    ]
)
def newvisit_loadvetlabexam(pathname, searchterm):
    if pathname == "/newrecord/newpatient" and not searchterm:
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
        Output({"type": "labexamlist_newpatient", "index": MATCH}, "options"),
    ],
    [
        Input('url', 'pathname'),
        Input({"type": "labexamlist_newpatient", "index": MATCH}, "value"),
    ]
)
def newpatient_loadlabexam(pathname, searchterm):
    if pathname == "/newrecord/newpatient" and not searchterm:
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


# @app.callback( #callback for profile submission
#     [
#         # dbc.Alert Properties
#         Output('newpatientprofile_alert', 'color'),
#         Output('newpatientprofile_alert', 'children'),
#         Output('newpatientprofile_alert', 'is_open'),
        
#         # dbc.Modal Properties
#         Output('newpatientprofile_successmodal', 'is_open'),
#         Output('newpatientprofile_feedback_message', 'children'),
#         Output('newpatientprofile_btn_modal', 'href')
#     ],
#     [
#         # For buttons, the property n_clicks 
#         Input('newpatientprofile_submit', 'n_clicks'),
#         Input('newpatientprofile_btn_modal', 'n_clicks')
#     ],
#     [
#         # The values of the fields are states 
#         # They are required in this process but they do not trigger this callback
#         State('client_ln', 'value'),
#         State('client_fn', 'value'),
#         State('client_mi', 'value'),
#         State('client_email', 'value'),
#         State('client_cn', 'value'),
#         State('client_province', 'value'),
#         State('client_city', 'value'),
#         State('client_barangay', 'value'),
#         State('client_street', 'value'),
#         State('patient_m', 'value'),
#         State('patient_sex', 'value'),
#         State('patient_breed', 'value'),
#         State('patient_bd', 'value'),
#         State('patient_idiosync', 'value'),
#         State('patient_color', 'value'),
#     ]
# )
# def patientprofile_saveprofile(submitbtn, closebtn, 
#                                client_ln, client_fn, client_mi, client_email, client_cn, 
#                                client_province, client_city, client_barangay, client_street, 
#                                patient_m, patient_sex, patient_breed, patient_bd, patient_idiosync, patient_color):
    
#     ctx = dash.callback_context # the ctx filter -- ensures that only a change in url will activate this callback
    
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid and 'newpatientprofile_submit' in eventid:
#             # submitbtn condition checks if callback was activated by a click and not by having the submit button appear in the layout

#             # Set default outputs
#             alert_color = ''
#             alert_text = ''
#             alert_open = False
#             modal_open = False
#             modal_text = ''
#             modal_href = '#'

#             # check inputs if they have values
#             if not client_ln: # If client_ln is blank, not client_ln = True
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the owner's last name."
#             elif not client_fn:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the owner's first name."
#             elif not client_mi:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the owner's middle initials."
#             elif not client_email:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the owner's email."
#             elif not client_cn:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the owner's contact number."

#             elif not client_province:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the owner's complete address."
#             elif not client_city:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the owner's complete address."
#             elif not client_barangay:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the owner's complete address."
#             elif not client_street:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the owner's complete address."
            
#             elif not patient_m:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the patient's name."
#             elif not patient_sex:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the patient's sex."
#             elif not patient_breed:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the patient's breed."
#             elif not patient_bd:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the patient's birthdate."
#             elif not patient_idiosync:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the patient's idiosyncrasies."
#             elif not patient_color:
#                 alert_open = True
#                 alert_color = 'danger'
#                 alert_text = "Check your inputs. Please supply the patient's markings."

#             else: # all inputs are valid
                
#                 #save to db
#                     sql_client = """ 
#                         INSERT INTO client(
#                         client_ln, client_fn, client_mi, client_email, client_cn, client_province, client_city, client_barangay, client_street
#                         )
#                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#                     """
#                     values_client = [client_ln, client_fn, client_mi, client_email, client_cn, client_province, client_city, client_barangay, client_street]
#                     db.modifydatabase(sql_client,values_client)

#                     db.cursor.execute("SELECT lastval();")
#                     client_id = db.cursor.fetchone()[0]

#                     sql_patient = """
#                         INSERT INTO patient(
#                         patient_m, patient_sex, patient_breed, patient_bd, patient_idiosync, patient_color, client_id
#                         )
#                         VALUES(%s,%s,%s,%s,%s,%s,%s)
#                     """
#                     values_patient = [patient_m, patient_sex, patient_breed, patient_bd, patient_idiosync, patient_color, client_id]
#                     db.modifydatabase(sql_patient, values_patient)  

#                     # If this is successful, we want the successmodal to show
#                     modal_text = "Patient profile has been saved successfully."
#                     modal_href = '/home' #go back to homepage
#                     modal_open = True 
#             return [alert_color, alert_text, alert_open, modal_open, modal_text, modal_href]

#         else: # Callback was not triggered by desired triggers
#             raise PreventUpdate
#     else:
#         raise PreventUpdate
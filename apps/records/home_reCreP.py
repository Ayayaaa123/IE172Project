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
        dbc.Alert(id = 'visitrecord_alert_reCreP', is_open = False),
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
                    dbc.Row([ #Select Client and Patient

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

                    ]),
                    
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
    ])


#SAVE AND SUBMIT CALLBACKS

@app.callback( # Submit Button for visit in reCreP
    [
        Output('visitrecord_alert_reCreP','color'),
        Output('visitrecord_alert_reCreP','children'),
        Output('visitrecord_alert_reCreP','is_open'),
        Output('visitrecord_successmodal_reCreP','is_open'),
        Output('re_clientlist_reCreP', 'value'),
        Output('patientlist_reCreP','value'),
        Output('vetlist_reCreP','value'),
        Output('visitdate_reCreP', 'value'),
    ],
    [
        Input('visitrecord_submit_reCreP','n_clicks'),
        Input('re_clientlist_reCreP', 'value'),
        Input('patientlist_reCreP','value'),
        Input('vetlist_reCreP','value'),
        Input('visitdate_reCreP', 'value'),
    ]
)
def visitrecord_save_reCreP(submitbtn, client, patient, vet, date):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        alert_open = False
        modal_open = False
        alert_color = ''
        alert_text = ''
        
        if eventid == 'visitrecord_submit_reCreP' and submitbtn:
            
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
            else:
                sql = '''
                INSERT INTO visit(
                                patient_id,
                                vet_id,
                                visit_delete_ind
                            )
                            VALUES(%s, %s, %s)
                    '''
                values = [patient, vet, False]

                db.modifydatabase(sql, values)

                modal_open = True
            
            if not all([client, patient, vet, date]):
                return [alert_color, alert_text, alert_open, modal_open, client, patient, vet, date]

            return [alert_color, alert_text, alert_open, modal_open, None, None, None, datetime.now().date()]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


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
            
        if searchterm:
            sql += """ AND (
                client_ln ILIKE %s 
                OR client_fn ILIKE %s
                );
            """
            values = [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]

        cols = ['client_id', 'client_name']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['client_name'], 'value': row['client_id']} for _, row in result.iterrows()]
        return options, 
    else:
        raise PreventUpdate  

    
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
                COALESCE(patient_m, '') ||' - ' || COALESCE(patient_species,'') || ' (' || COALESCE(patient_color, '')|| ')' AS patient_name
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




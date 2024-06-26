from dash import dcc #interpreter recommended to replace 'import dash_core_components as dcc' with 'from dash import dcc'
from dash import html, dash_table #interpreter recommended to replace 'import dash_html_components as html' with 'from dash import html'
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
import psycopg2
from dash import ALL, MATCH
from urllib.parse import urlparse, parse_qs








layout = html.Div(
    [
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="/managedata/existingclinicians", id="editclinicians_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H1("Edit Clinician Profile"),
        html.Hr(),
        dbc.Alert(id='editclinicianprofile_alert', is_open=False),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Personal Information")
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Last Name"),
                                        dbc.Input(id='clinician_ln', type='text', placeholder='Enter Last Name', style={'width': '80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("First Name"),
                                        dbc.Input(id='clinician_fn', type='text', placeholder='Enter First Name', style={'width': '80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Middle Initial"),
                                        dbc.Input(id='clinician_mi', type='text', placeholder='Enter Middle Initial', style={'width': '80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Suffix (leave blank if none)"),
                                        dbc.Input(id='clinician_suffix', type='text', placeholder='Enter Suffix', style={'width': '80%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Email"),
                                        dbc.Input(id='clinician_email', type='text', placeholder='Enter Email Address', style={'width': '80%'}),
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Contact Number"),
                                        dbc.Input(id='clinician_cn', type='text', placeholder='Enter Contact Number', style={'width': '80%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                )
            ],
            style={'width': '100%'}
        ),
        html.Br(),
        html.Br(),
        dbc.Button(
            'Save',
            id='editclinician_savebtn',
            n_clicks=0,
            className='custom-submitbutton',
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4('Save Success')),
                dbc.ModalBody('Clinician profile has been updated', id='editclinicianrprofile_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button("Okay", href='/managedata/existingclinicians', style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, id='editclinicianprofile_btn_modal')
                )
            ],
            centered=True,
            id='editclinicianprofile_successmodal',
            backdrop='static'
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete Profile?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='clinicianprofile_removerecord',
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
        id='clinicianprofile_removerecord_div')
    ]
)

# CALLBACK TO SAVE CHANGES INCLUDING DELETE
@app.callback(
    [
        Output('editclinicianprofile_alert', 'color'),
        Output('editclinicianprofile_alert', 'children'),
        Output('editclinicianprofile_alert', 'is_open'),

        Output('editclinicianprofile_successmodal', 'is_open'),
        Output('editclinicianrprofile_feedback_message', 'children'),
        Output('editclinicianprofile_btn_modal', 'href'),
    ],
   
    [
        Input('editclinician_savebtn', 'n_clicks'),
        Input('editclinicianprofile_btn_modal', 'n_clicks')
    ],


    [
        State('clinician_fn', 'value'),
        State('clinician_ln', 'value'),
        State('clinician_mi', 'value'),
        State('clinician_suffix', 'value'),
        State('clinician_email', 'value'),
        State('clinician_cn', 'value'),
        State('url', 'search'),
        State('clinicianprofile_removerecord', 'value') #for delete
    ]
   
)




def save_clinician_profile(n_clicks_btn, n_clicks_modal, clinician_fn, clinician_ln, clinician_mi, clinician_suffix, clinician_email, clinician_cn, url_search, removerecord):   
    ctx = dash.callback_context # the ctx filter -- ensures that only a change in url will activate this callback
    # print("Triggered:", ctx.triggered)


    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid and 'editclinician_savebtn' in eventid:


            # Set default outputs
            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False
            modal_text = ''
            modal_href = '#'

            parsed = urlparse(url_search)
            query_clinician_id = parse_qs(parsed.query)


            if 'id' in query_clinician_id:
                clinician_id = query_clinician_id['id'][0]
            else:
                # Handle the case when 'id' is not present in the URL
                # raise an error, redirect, or handle it accordingly
                raise PreventUpdate
           
            # check inputs if they have values
            if not clinician_ln: # If vet_ln is blank, not vet_ln = True
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please supply last name."
            elif not clinician_fn:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please supply first name."




            elif not clinician_email:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please supply the vet's email."
            elif not clinician_cn:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please supply the vet's contact number."




            else: #all inputs are valid
                #save to db
                modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
                sql_clinician = """ UPDATE clinician
                                    SET
                                        clinician_ln = %s,
                                        clinician_fn = %s,
                                        clinician_mi = %s,
                                        clinician_suffix = %s,
                                        clinician_email = %s,
                                        clinician_cn= %s,
                                        clinician_modified_date = %s,
                                        clinician_delete_ind = %s
                                    WHERE
                                        clinician_id = %s
                                    """
                to_delete = bool(removerecord) 
                values_clinician = [clinician_ln, clinician_fn, clinician_mi, clinician_suffix, clinician_email, clinician_cn, modified_date, to_delete, clinician_id]
                # print("values_vet:", values_vet)

                db.modifydatabase(sql_clinician, values_clinician)
               
                modal_text = "Changes in Clinician's Profile has been saved successfully."
                modal_href = 'managedata/existingclinicians' #go back to table
                modal_open = True
           
            return [alert_color, alert_text, alert_open, modal_open, modal_text, modal_href]


        else: # Callback was not triggered by desired triggers
            raise PreventUpdate
    else:
        raise PreventUpdate










#CALLBACK TO LOAD EDIT PAGE
@app.callback(
    [
        Output('clinician_fn', 'value'),
        Output('clinician_ln', 'value'),
        Output('clinician_mi', 'value'),
        Output('clinician_suffix', 'value'),
        Output('clinician_email', 'value'),
        Output('clinician_cn', 'value'),  # Corrected column name here
    ],
    [
        Input('url', 'search'),
    ],
)
def current_values(url_search):
    parsed = urlparse(url_search)
    query_clinician_id = parse_qs(parsed.query)


    if 'id' in query_clinician_id:
        clinician_id = query_clinician_id['id'][0]
        sql = """
            SELECT clinician_fn, clinician_ln, clinician_mi, clinician_suffix, clinician_email, clinician_cn  
            FROM clinician
            WHERE clinician_id = %s
        """
        values = [clinician_id]
        col = ['clinician_fn', 'clinician_ln', 'clinician_mi', 'clinician_suffix', 'clinician_email', 'clinician_cn']


        df = db.querydatafromdatabase(sql, values, col)
       
        clinician_fn = df['clinician_fn'][0]
        clinician_ln = df['clinician_ln'][0]
        clinician_mi = df['clinician_mi'][0]
        clinician_suffix = df['clinician_suffix'][0]
        clinician_email = df['clinician_email'][0]
        clinician_cn = df['clinician_cn'][0]


        print(clinician_fn, clinician_ln, clinician_mi, clinician_suffix, clinician_email, clinician_cn)


        return [clinician_fn, clinician_ln, clinician_mi, clinician_suffix, clinician_email, clinician_cn]
    else:
        raise PreventUpdate

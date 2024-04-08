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
        dbc.Alert(id='editclinical_alert', is_open=False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="/managedata", id="editclinicians_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Edit Information")
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Clinical Exam Type"),
                                        dbc.Input(id='clinical_exam_type_m', type='text'),
                                    ],
                                    className="mb-3",
                                ),
                            ]
                        ),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Delete Item?", width=2),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='clinical_removerecord',
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
                        id='clinical_removerecord_div')
                     

                            ]
                        )
                    ]
                ),
        html.Br(),
        html.Br(),
        dbc.Button(
            'Save',
            id='editclinical_savebtn',
            n_clicks=0,
            className='custom-submitbutton',
            ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4('Changes have been saved')),
                # dbc.ModalBody('Clinician profile has been updated', id='editclinicianrprofile_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button("Okay", href='/managedata', id='editclinical_btn_modal')
                )
            ],
            centered=True,
            id='editclinical_successmodal',
            backdrop='static'
        ),    
    ]
)


# CALLBACK TO LOAD 
@app.callback(
    [
        Output('clinical_exam_type_m', 'value'),
    ],
    [
        Input('url', 'search'),
    ],
)

def load_clinical(url_search):
    parsed = urlparse(url_search)
    query_clinical_exam_type_id = parse_qs(parsed.query)

    if 'id' in query_clinical_exam_type_id:
        clinicical_exam_type_id = query_clinical_exam_type_id['id'][0]
        sql = """
            SELECT clinical_exam_type_m
            FROM clinical_exam_type
            WHERE clinical_exam_type_id = %s
        """
        values = [clinicical_exam_type_id]
        col = ['clinicical_exam_type_m']


        df = db.querydatafromdatabase(sql, values, col)
       
        clinicical_exam_type_m = df['clinicical_exam_type_m'][0]
        


        print(clinicical_exam_type_m)


        return [clinicical_exam_type_m]
    else:
        raise PreventUpdate




# CALLBACK TO SAVE CHANGES INCLUDING DELETE
@app.callback(
    [
        Output('editclinical_alert', 'color'),
        Output('editclinical_alert', 'children'),
        Output('editclinical_alert', 'is_open'),

        Output('editclinical_successmodal', 'is_open'),
        # Output('editclinicianrprofile_feedback_message', 'children'),
        Output('editclinical_btn_modal', 'href'),
    ],
   
    [
        Input('editclinical_savebtn', 'n_clicks'),
        Input('editclinical_btn_modal', 'n_clicks')
    ],


    [
        State('clinical_exam_type_m', 'value'),
        State('url', 'search'),
        State('clinical_removerecord', 'value') #for delete
    ]
)


def save_clinical(n_clicks_btn, n_clicks_modal,clinical_exam_type_m, url_search, removerecord):
    ctx = dash.callback_context # the ctx filter -- ensures that only a change in url will activate this callback
    # print("Triggered:", ctx.triggered)


    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid and 'editclinical_savebtn' in eventid:

            # Set default outputs
            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False
            modal_href = '#'
            
            parsed = urlparse(url_search)
            query_clinical_exam_type_id = parse_qs(parsed.query)


            if 'id' in query_clinical_exam_type_id:
                clinical_exam_type_id = query_clinical_exam_type_id['id'][0]
            else:
                # Handle the case when 'id' is not present in the URL
                # raise an error, redirect, or handle it accordingly
                raise PreventUpdate
            
            if not clinical_exam_type_m:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Cannot be blank"

            else: #all inputs are valid
                #save to db
                modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
                sql_clinician = """ UPDATE clinical_exam_type
                                    SET
                                        clinical_exam_type_m = %s,
                                        clinical_exam_type_modified_date = %s,
                                        clinical_exam_type_delete_ind = %s
                                    WHERE
                                        clinical_exam_type_id = %s
                                    """
                to_delete = bool(removerecord) 
                values_clinical = [clinical_exam_type_m, modified_date, to_delete, clinical_exam_type_id]
        

                db.modifydatabase(sql_clinician, values_clinical)
               
                modal_text = "Changes have been saved successfully."
                modal_href = 'managedata' #go back to table
                modal_open = True
           
            return [alert_color, alert_text, alert_open, modal_open, modal_href]


        else: # Callback was not triggered by desired triggers
            raise PreventUpdate
    else:
        raise PreventUpdate
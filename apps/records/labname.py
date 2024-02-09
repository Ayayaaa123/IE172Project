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
        dbc.Alert(id='editlab_alert', is_open=False),
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
                                        dbc.InputGroupText("Laboratory Exam Type"),
                                        dbc.Input(id='lab_exam_type_m', type='text'),
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
                                            id='lab_removerecord',
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
                        id='lab_removerecord_div')
                     

                            ]
                        )
                    ]
                ),
        html.Br(),
        html.Br(),
        dbc.Button(
            'Save',
            id='editlab_savebtn',
            n_clicks=0,
            className='custom-submitbutton',
            ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4('Changes have been saved')),
                # dbc.ModalBody('Clinician profile has been updated', id='editclinicianrprofile_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button("Okay", href='/managedata', id='editlab_btn_modal')
                )
            ],
            centered=True,
            id='editlab_successmodal',
            backdrop='static'
        ),    
    ]
)


# CALLBACK TO LOAD 
@app.callback(
    [
        Output('lab_exam_type_m', 'value'),
    ],
    [
        Input('url', 'search'),
    ],
)

def load_labname(url_search):
    parsed = urlparse(url_search)
    query_lab_exam_type_id = parse_qs(parsed.query)

    if 'id' in query_lab_exam_type_id:
        lab_exam_type_id = query_lab_exam_type_id['id'][0]
        sql = """
            SELECT lab_exam_type_m
            FROM lab_exam_type
            WHERE lab_exam_type_id = %s
        """
        values = [lab_exam_type_id]
        col = ['lab_exam_type_m']


        df = db.querydatafromdatabase(sql, values, col)
       
        lab_exam_type_m = df['lab_exam_type_m'][0]
        
        print(lab_exam_type_m)


        return [lab_exam_type_m]
    else:
        raise PreventUpdate




# CALLBACK TO SAVE CHANGES INCLUDING DELETE
@app.callback(
    [
        Output('editlab_alert', 'color'),
        Output('editlab_alert', 'children'),
        Output('editlab_alert', 'is_open'),

        Output('editlab_successmodal', 'is_open'),
        # Output('editclinicianrprofile_feedback_message', 'children'),
        Output('editlab_btn_modal', 'href'),
    ],
   
    [
        Input('editlab_savebtn', 'n_clicks'),
        Input('editlab_btn_modal', 'n_clicks')
    ],


    [
        State('lab_exam_type_m', 'value'),
        State('url', 'search'),
        State('lab_removerecord', 'value') #for delete
    ]
)


def save_labname(n_clicks_btn, n_clicks_modal, lab_exam_type_m, url_search, removerecord):
    ctx = dash.callback_context # the ctx filter -- ensures that only a change in url will activate this callback
    # print("Triggered:", ctx.triggered)


    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid and 'editlab_savebtn' in eventid:

            # Set default outputs
            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False
            modal_href = '#'
            
            parsed = urlparse(url_search)
            query_lab_exam_type_id = parse_qs(parsed.query)


            if 'id' in query_lab_exam_type_id:
                lab_exam_type_id = query_lab_exam_type_id['id'][0]
            else:
                # Handle the case when 'id' is not present in the URL
                # raise an error, redirect, or handle it accordingly
                raise PreventUpdate
            
            if not lab_exam_type_m:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Cannot be blank"

            else: #all inputs are valid
                #save to db
                sql_labname = """ UPDATE lab_exam_type
                                    SET
                                        lab_exam_type_m = %s,
                                        lab_exam_type_delete_ind = %s
                                    WHERE
                                        lab_exam_type_id = %s
                                    """
                to_delete = bool(removerecord) 
                values_labname = [lab_exam_type_m, to_delete, lab_exam_type_id]
        

                db.modifydatabase(sql_labname, values_labname)
               
                modal_text = "Changes have been saved successfully."
                modal_href = 'managedata' #go back to table
                modal_open = True
           
            return [alert_color, alert_text, alert_open, modal_open, modal_href]


        else: # Callback was not triggered by desired triggers
            raise PreventUpdate
    else:
        raise PreventUpdate
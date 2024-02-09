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
        dbc.Alert(id='editvacc_alert', is_open=False),
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
                                        dbc.InputGroupText("Vaccine Type"),
                                        dbc.Input(id='vacc_m', type='text'),
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
                                            id='vacc_removerecord',
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
                        id='vacc_removerecord_div')
                     

                            ]
                        )
                    ]
                ),
        html.Br(),
        html.Br(),
        dbc.Button(
            'Save',
            id='editvacc_savebtn',
            n_clicks=0,
            className='custom-submitbutton',
            ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4('Changes have been saved')),
                # dbc.ModalBody('Clinician profile has been updated', id='editclinicianrprofile_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button("Okay", href='/managedata', id='editvacc_btn_modal')
                )
            ],
            centered=True,
            id='editvacc_successmodal',
            backdrop='static'
        ),    
    ]
)


# CALLBACK TO LOAD 
@app.callback(
    [
        Output('vacc_m', 'value'),
    ],
    [
        Input('url', 'search'),
    ],
)

def load_vaccname(url_search):
    parsed = urlparse(url_search)
    query_vacc_m_id = parse_qs(parsed.query)

    if 'id' in query_vacc_m_id:
        vacc_m_id = query_vacc_m_id['id'][0]
        sql = """
            SELECT vacc_m
            FROM vacc_m
            WHERE vacc_m_id = %s
        """
        values = [vacc_m_id]
        col = ['vacc_m']


        df = db.querydatafromdatabase(sql, values, col)
       
        vacc_m = df['vacc_m'][0]
        
        # print(lab_exam_type_m)


        return [vacc_m]
    else:
        raise PreventUpdate




# CALLBACK TO SAVE CHANGES INCLUDING DELETE
@app.callback(
    [
        Output('editvacc_alert', 'color'),
        Output('editvacc_alert', 'children'),
        Output('editvacc_alert', 'is_open'),

        Output('editvacc_successmodal', 'is_open'),
        # Output('editclinicianrprofile_feedback_message', 'children'),
        Output('editvacc_btn_modal', 'href'),
    ],
   
    [
        Input('editvacc_savebtn', 'n_clicks'),
        Input('editvacc_btn_modal', 'n_clicks')
    ],


    [
        State('vacc_m', 'value'),
        State('url', 'search'),
        State('vacc_removerecord', 'value') #for delete
    ]
)


def save_vaccname(n_clicks_btn, n_clicks_modal, vacc_m, url_search, removerecord):
    ctx = dash.callback_context # the ctx filter -- ensures that only a change in url will activate this callback
    # print("Triggered:", ctx.triggered)


    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid and 'editvacc_savebtn' in eventid:

            # Set default outputs
            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False
            modal_href = '#'
            
            parsed = urlparse(url_search)
            query_vacc_m_id = parse_qs(parsed.query)


            if 'id' in query_vacc_m_id:
                vacc_m_id = query_vacc_m_id['id'][0]
            else:
                # Handle the case when 'id' is not present in the URL
                # raise an error, redirect, or handle it accordingly
                raise PreventUpdate
            
            if not vacc_m:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Cannot be blank"

            else: #all inputs are valid
                #save to db
                sql_vaccname = """ UPDATE vacc_m
                                    SET
                                        vacc_m = %s,
                                        vacc_m_delete_ind = %s
                                    WHERE
                                        vacc_m_id = %s
                                    """
                to_delete = bool(removerecord) 
                values_vaccname = [vacc_m, to_delete, vacc_m_id]
        

                db.modifydatabase(sql_vaccname, values_vaccname)
               
                modal_text = "Changes have been saved successfully."
                modal_href = 'managedata' #go back to table
                modal_open = True
           
            return [alert_color, alert_text, alert_open, modal_open, modal_href]


        else: # Callback was not triggered by desired triggers
            raise PreventUpdate
    else:
        raise PreventUpdate
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
        dbc.Alert(id='editdeworm_alert', is_open=False),
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
                                        dbc.InputGroupText("Deworming Medicine Name"),
                                        dbc.Input(id='deworm_m', type='text'),
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
                                            id='deworm_removerecord',
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
                        id='deworm_removerecord_div')
                     

                            ]
                        )
                    ]
                ),
        html.Br(),
        html.Br(),
        dbc.Button(
            'Save',
            id='editdeworm_savebtn',
            n_clicks=0,
            className='custom-submitbutton',
            ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4('Changes have been saved')),
                # dbc.ModalBody('Clinician profile has been updated', id='editclinicianrprofile_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button("Okay", href='/managedata', id='editdeworm_btn_modal')
                )
            ],
            centered=True,
            id='editdeworm_successmodal',
            backdrop='static'
        ),    
    ]
)


# CALLBACK TO LOAD 
@app.callback(
    [
        Output('deworm_m', 'value'),
    ],
    [
        Input('url', 'search'),
    ],
)

def load_dewormname(url_search):
    parsed = urlparse(url_search)
    query_deworm_m_id = parse_qs(parsed.query)

    if 'id' in query_deworm_m_id:
        deworm_m_id = query_deworm_m_id['id'][0]
        sql = """
            SELECT deworm_m
            FROM deworm_m
            WHERE deworm_m_id = %s
        """
        values = [deworm_m_id]
        col = ['deworm_m']


        df = db.querydatafromdatabase(sql, values, col)
       
        deworm_m = df['deworm_m'][0]
        
        # print(lab_exam_type_m)


        return [deworm_m]
    else:
        raise PreventUpdate




# CALLBACK TO SAVE CHANGES INCLUDING DELETE
@app.callback(
    [
        Output('editdeworm_alert', 'color'),
        Output('editdeworm_alert', 'children'),
        Output('editdeworm_alert', 'is_open'),

        Output('editdeworm_successmodal', 'is_open'),
        # Output('editclinicianrprofile_feedback_message', 'children'),
        Output('editdeworm_btn_modal', 'href'),
    ],
   
    [
        Input('editdeworm_savebtn', 'n_clicks'),
        Input('editdeworm_btn_modal', 'n_clicks')
    ],


    [
        State('deworm_m', 'value'),
        State('url', 'search'),
        State('deworm_removerecord', 'value') #for delete
    ]
)


def save_dewormname(n_clicks_btn, n_clicks_modal, deworm_m, url_search, removerecord):
    ctx = dash.callback_context # the ctx filter -- ensures that only a change in url will activate this callback
    # print("Triggered:", ctx.triggered)


    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid and 'editdeworm_savebtn' in eventid:

            # Set default outputs
            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False
            modal_href = '#'
            
            parsed = urlparse(url_search)
            query_deworm_m_id = parse_qs(parsed.query)


            if 'id' in query_deworm_m_id:
                deworm_m_id = query_deworm_m_id['id'][0]
            else:
                # Handle the case when 'id' is not present in the URL
                # raise an error, redirect, or handle it accordingly
                raise PreventUpdate
            
            if not deworm_m:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Cannot be blank"

            else: #all inputs are valid
                #save to db
                modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
                sql_dewormname = """ UPDATE deworm_m
                                    SET
                                        deworm_m = %s,
                                        deworm_m_modified_date = %s,
                                        deworm_m_delete_ind = %s
                                    WHERE
                                        deworm_m_id = %s
                                    """
                to_delete = bool(removerecord) 
                values_dewormname = [deworm_m, modified_date, to_delete, deworm_m_id]
        

                db.modifydatabase(sql_dewormname, values_dewormname)
               
                modal_text = "Changes have been saved successfully."
                modal_href = 'managedata' #go back to table
                modal_open = True
           
            return [alert_color, alert_text, alert_open, modal_open, modal_href]


        else: # Callback was not triggered by desired triggers
            raise PreventUpdate
    else:
        raise PreventUpdate
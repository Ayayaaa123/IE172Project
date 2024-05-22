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
from urllib.parse import urlparse, parse_qs


layout = html.Div(
    [
        dbc.Alert(id='addproblemnote_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="addproblemnote_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H2("Note Details"),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Have Been Tested?"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="addproblemnote_tested",
                        searchable=True,
                        options=[
                            {"label": "Yes", "value": True},
                            {"label": "No", "value": False},
                        ]
                    ),
                    width=6,
                ),
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Differential Diagnosis"), width=3),
                dbc.Col(
                    dcc.Textarea(
                        id="addproblemnote_diagnosis",
                        placeholder='Enter Diagnosis',
                        style={"height":75, 'width':'100%'},
                        contentEditable=True
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Possible Treatment"), width=3),
                dbc.Col(
                    dcc.Textarea(
                        id="addproblemnote_treatment",
                        placeholder='Enter Treatment',
                        style={"height":75, 'width':'100%'},
                        contentEditable=True
                    ),
                    width=6,
                )
            ]),
            dbc.Row([
                dbc.Col(html.H4("Tests Needed"), width=3),
                dbc.Col(
                    dcc.Textarea(
                        id="addproblemnote_tests",
                        placeholder='Enter Tests',
                        style={"height":75, 'width':'100%'},
                        contentEditable=True
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Bill"), width=3),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id="addproblemnote_bill",
                        placeholder="Enter Bill",
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
        ]),
        html.Br(),
        dbc.Button(
            'Save',
            id = 'addproblemnote_save',
            n_clicks = 0,
            className='custom-submitbutton',
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H3('Save Success')),
            dbc.ModalFooter(
                dbc.Button(
                    "Return",
                    style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, 
                    href="",
                    id="addproblemnote_return-button",
                )
            )
        ],
        centered = True, 
        id = 'addproblemnote_successmodal',
        backdrop = 'static'
        )
    ]
)



@app.callback(  #initial values
    Output('addproblemnote_return-link', 'href'),
    Input('url','search'),
)
def addproblemnote_initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    return_link= ""

    if 'patient_id' in query_ids and 'problem_id' in query_ids:
        patient_id = query_ids.get('patient_id', [None])[0]
        problem_id = query_ids.get('problem_id', [None])[0]

        return_link = f'/editproblem?mode=add&problem_id={problem_id}&patient_id={patient_id}'

        return return_link

    else:
        raise PreventUpdate
    


@app.callback( #save changes
    Output('addproblemnote_alert','color'),
    Output('addproblemnote_alert','children'),
    Output('addproblemnote_alert','is_open'),
    Output('addproblemnote_successmodal', 'is_open'),
    Output('addproblemnote_return-button', 'href'),
    Input('addproblemnote_save', 'n_clicks'),
    Input('url','search'),
    Input('addproblemnote_tested','value'),
    Input('addproblemnote_diagnosis','value'),
    Input('addproblemnote_treatment','value'),
    Input('addproblemnote_tests','value'),
    Input('addproblemnote_bill','value')
)
def save_addnote_record(submitbtn, url_search, note_tested, note_diagnosis, note_treatment, note_tests, note_bill):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'addproblemnote_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            return_link = ''

            problem_id = query_ids.get('problem_id', [None])[0]
            patient_id = query_ids.get('patient_id', [None])[0]

            if note_tested is None:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select test status'
            elif not note_diagnosis:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter diagnosis'
            elif not note_treatment:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter treatment'
            elif not note_bill:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please enter bill"
            else:
                sql = """
                    SELECT MAX(visit_id)
                    FROM visit
                    """
                values = []
                df = db.querydatafromdatabase(sql,values)
                visit_id = int(df.loc[0,0])
                
                sql = """
                    SELECT MAX(note_no)
                    FROM note
                    WHERE problem_id = %s
                    """
                values = [problem_id]
                df = db.querydatafromdatabase(sql,values)
                note_no_before = int(df.loc[0,0]) if not pd.isna(df.loc[0,0]) else 0
                note_no_new = note_no_before + 1

                sql = """
                    SELECT MAX(note_or_no)
                    FROM note
                    """
                values = []
                df = db.querydatafromdatabase(sql,values)
                note_or_no_before = int(df.loc[0,0]) if not pd.isna(df.loc[0,0]) else 0
                note_or_no_new = note_or_no_before + 1

                sql = """
                    INSERT INTO note(
                        visit_id,
                        problem_id,
                        note_no,
                        note_have_been_tested,
                        note_differential_diagnosis,
                        note_treatment,
                        note_for_testing,
                        note_or_no,
                        note_bill,
                        note_delete_ind
                    )
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                values = [visit_id, problem_id, note_no_new, note_tested, note_diagnosis, note_treatment, note_tests, note_or_no_new, note_bill, False]
                db.modifydatabase(sql, values)

                modal_open = True

                return_link = f'/editproblem?mode=add&problem_id={problem_id}&patient_id={patient_id}'

            return [alert_color, alert_text, alert_open, modal_open, return_link]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
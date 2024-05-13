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
        dbc.Alert(id='addproblemclinicalexam_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="addproblemclinicalexam_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H2("Clinical Exam Details"),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Clinical Exam Type"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="addproblemclinicalexam_namelist",
                        placeholder='Select Clinical Exam Type',
                        searchable=True,
                        options=[],
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Clinical Exam Findings"), width=3),
                dbc.Col(
                    dcc.Textarea(
                        id="addproblemclinicalexam_findings",
                        placeholder='Enter findings',
                        style={"height":100, 'width':'100%'},
                        contentEditable=True
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Clinician"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="addproblemclinician_namelist",
                        placeholder='Select Clinician',
                        searchable=True,
                        options=[],
                        multi=True
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
        ]),
        html.Br(),
        dbc.Button(
            'Save',
            id = 'addproblemclinicalexam_save',
            n_clicks = 0,
            className='custom-submitbutton',
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H3('Save Success')),
            dbc.ModalFooter(
                dbc.Button(
                    "Return",
                    href="",
                    id="addproblemclinicalexam_return-button",
                )
            )
        ],
        centered = True, 
        id = 'addproblemclinicalexam_successmodal',
        backdrop = 'static'
        )
    ]
)



@app.callback(  #initial values
    Output('addproblemclinicalexam_namelist', 'options'),
    Output('addproblemclinician_namelist', 'options'),
    Output('addproblemclinicalexam_return-link', 'href'),
    Input('url','search'),
)
def addproblemclinicalexam_initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    return_link= ""

    if 'patient_id' in query_ids and 'problem_id' in query_ids:
        patient_id = query_ids.get('patient_id', [None])[0]
        problem_id = query_ids.get('problem_id', [None])[0]

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
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['clinical_exam_type_m'], 'value': row['clinical_exam_type_id']} for _, row in result.iterrows()]

        sql = """
            SELECT 
                clinician_id,
                COALESCE(clinician_ln, '') || ', ' || COALESCE (clinician_fn, '') || ' ' || COALESCE (clinician_mi, '') AS clinician_name
            FROM 
                clinician
            WHERE 
                NOT clinician_delete_ind
        """
        values = []
        cols = ['clinician_id', 'clinician_name']
        result = db.querydatafromdatabase(sql, values, cols)
        options2 = [{'label': row['clinician_name'], 'value': row['clinician_id']} for _, row in result.iterrows()]

        return_link = f'/editproblem?mode=add&problem_id={problem_id}&patient_id={patient_id}'

        return (options, options2, return_link)
    
    else:
        raise PreventUpdate
    


@app.callback( #save changes
    Output('addproblemclinicalexam_alert','color'),
    Output('addproblemclinicalexam_alert','children'),
    Output('addproblemclinicalexam_alert','is_open'),
    Output('addproblemclinicalexam_successmodal', 'is_open'),
    Output('addproblemclinicalexam_return-button', 'href'),
    Input('addproblemclinicalexam_save', 'n_clicks'),
    Input('url','search'),
    Input('addproblemclinicalexam_namelist','value'),
    Input('addproblemclinicalexam_findings','value'),
    Input('addproblemclinician_namelist','value'),
)
def save_clinicalexam_record(submitbtn, url_search, clinicalexam_name, clinicalexam_findings, clinician):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'addproblemclinicalexam_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            patient_link = ''
       
            patient_id = query_ids.get('patient_id', [None])[0]
            problem_id = query_ids.get('problem_id', [None])[0]

            if not clinicalexam_name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select clinical exam type'
            elif not clinicalexam_findings:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter clinical exam findings'
            elif not clinician:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select clinician'
            else:
                modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
                sql = """
                    SELECT MAX(clinical_exam_no)
                    FROM clinical_exam
                    WHERE problem_id = %s
                    """
                values = [problem_id]
                df = db.querydatafromdatabase(sql,values)
                clinicalexam_no_before = int(df.loc[0,0]) if not pd.isna(df.loc[0,0]) else 0
                clinicalexam_no_new = clinicalexam_no_before + 1

                sql = """
                    INSERT INTO clinical_exam(
                        clinical_exam_no,
                        problem_id,
                        clinical_exam_type_id,
                        clinical_exam_ab_findings,
                        clinical_exam_modified_date,
                        clinical_exam_delete_ind
                    )
                    VALUES(%s, %s, %s, %s, %s, %s)
                """
                values = [clinicalexam_no_new, problem_id, clinicalexam_name, clinicalexam_findings, modified_date, False]
                db.modifydatabase(sql, values)

                sql = """
                    SELECT MAX(clinical_exam_id)
                    FROM clinical_exam
                    """
                values = []
                df = db.querydatafromdatabase(sql,values)
                clinical_id = int(df.loc[0,0])

                for clinician_id in clinician:
                    sql = """
                            INSERT INTO clinician_assignment(
                                clinical_exam_id, 
                                clinician_id, 
                                clinician_assignment_modified_date,
                                clinician_assignment_delete_ind
                            )
                            VALUES (%s, %s, %s, %s)
                        """
                    values = [clinical_id, clinician_id, modified_date, False]
                    db.modifydatabase(sql, values)
                
                modal_open = True

                patient_link = f'/editproblem?mode=add&problem_id={problem_id}&patient_id={patient_id}'

            return [alert_color, alert_text, alert_open, modal_open, patient_link]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
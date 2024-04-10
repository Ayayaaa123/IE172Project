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
        dbc.Alert(id='problemclinicalexam_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="problemclinicalexam_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H2("Clinical Exam Details"),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Clinical Exam Type"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="problemclinicalexam_namelist",
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
                        id="problemclinicalexam_findings",
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
                        id="problemclinician_namelist",
                        placeholder='Select Clinician',
                        searchable=True,
                        options=[],
                        multi=True
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Delete Record?"), width=3),
                dbc.Col(
                    dbc.Checklist(
                        id='problemclinicalexam_delete',
                        options=[
                            {
                                'label': "Mark for Deletion",
                                'value': 1
                            }
                        ],
                        style={'fontWeight': 'bold'},
                    ),
                    width=6,
                ),
            ]),
        ]),
        html.Br(),
        dbc.Button(
            'Save',
            id = 'problemclinicalexam_save',
            n_clicks = 0,
            className='custom-submitbutton',
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H3('Save Success')),
            dbc.ModalFooter(
                dbc.Button(
                    "Return",
                    href="",
                    id="problemclinicalexam_return-button",
                )
            )
        ],
        centered = True, 
        id = 'problemclinicalexam_successmodal',
        backdrop = 'static'
        )
    ]
)



@app.callback(  #initial values
    Output('problemclinicalexam_namelist', 'options'),
    Output('problemclinicalexam_namelist', 'value'),
    Output('problemclinician_namelist', 'options'),
    Output('problemclinician_namelist', 'value'),
    Output('problemclinicalexam_findings', 'value'),
    Output('problemclinicalexam_return-link', 'href'),
    Input('url','search'),
)
def problemclinicalexam_initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    patient_link= ""

    if 'patient_id' in query_ids and 'problem_id' in query_ids and 'clinical_id' in query_ids:
        patient_id = query_ids.get('patient_id', [None])[0]
        problem_id = query_ids.get('problem_id', [None])[0]
        clinical_id = query_ids.get('clinical_id', [None])[0]
        mode = query_ids.get('mode', [None])[0]

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
        
        sql = """
            SELECT DISTINCT clinical_exam.clinical_exam_type_id, clinician.clinician_id, clinical_exam_ab_findings
            FROM clinician
            INNER JOIN clinician_assignment ON clinician.clinician_id = clinician_assignment.clinician_id
            INNER JOIN clinical_exam ON clinician_assignment.clinical_exam_id = clinical_exam.clinical_exam_id
            INNER JOIN problem ON clinical_exam.problem_id = problem.problem_id
            INNER JOIN visit ON problem.problem_id = visit.problem_id
            INNER JOIN patient ON visit.patient_id = patient.patient_id
            WHERE clinical_exam.clinical_exam_id = %s AND problem.problem_id = %s AND patient.patient_id = %s AND clinician_assignment_delete_ind = false
        """
        values = [clinical_id, problem_id, patient_id]
        col = ['clinical_exam_type', 'clinician', 'clinical_exam_findings']
        df = db.querydatafromdatabase(sql, values, col)

        clinical_exam_type = df['clinical_exam_type'][0]
        clinician_ids = df['clinician'].tolist()
        clinical_exam_findings = df['clinical_exam_findings'][0]

        if mode == "add":
            patient_link = f'/editproblem?mode=add&problem_id={problem_id}&patient_id={patient_id}'
        elif mode == "edit":
            patient_link = f'/editproblem?mode=edit&problem_id={problem_id}&patient_id={patient_id}'
        else:
            patient_link = f'/editproblem?mode=edit&problem_id={problem_id}&patient_id={patient_id}'

        return (options, clinical_exam_type, options2, clinician_ids, clinical_exam_findings, patient_link)
    
    else:
        raise PreventUpdate
    


@app.callback( #save changes
    Output('problemclinicalexam_alert','color'),
    Output('problemclinicalexam_alert','children'),
    Output('problemclinicalexam_alert','is_open'),
    Output('problemclinicalexam_successmodal', 'is_open'),
    Output('problemclinicalexam_return-button', 'href'),
    Input('problemclinicalexam_save', 'n_clicks'),
    Input('url','search'),
    Input('problemclinicalexam_namelist','value'),
    Input('problemclinicalexam_findings','value'),
    Input('problemclinician_namelist','value'),
    Input('problemclinicalexam_delete','value'),
)
def save_clinicalexam_record(submitbtn, url_search, clinicalexam_name, clinicalexam_findings, clinician, clinicalexam_delete):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'problemclinicalexam_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            patient_link = ''
       
            patient_id = query_ids.get('patient_id', [None])[0]
            problem_id = query_ids.get('problem_id', [None])[0]
            clinical_id = query_ids.get('clinical_id', [None])[0]  
            mode = query_ids.get('mode', [None])[0]

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
                to_delete = bool(clinicalexam_delete)
                modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
                sql = """
                    UPDATE clinical_exam
                    SET 
                        clinical_exam_type_id = %s,
                        clinical_exam_ab_findings = %s,
                        clinical_exam_modified_date = %s,
                        clinical_exam_delete_ind = %s
                    FROM problem
                    INNER JOIN visit ON problem.problem_id = visit.problem_id
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                    WHERE problem.problem_id = %s AND patient.patient_id = %s AND clinical_exam_id = %s
                """
                values = [clinicalexam_name, clinicalexam_findings, modified_date, to_delete, problem_id, patient_id, clinical_id]
                db.modifydatabase(sql, values)

                for clinician_id in clinician:
                    sql_check = """
                            SELECT COUNT(*)
                            FROM clinician_assignment
                            WHERE clinical_exam_id = %s AND clinician_id = %s
                    """
                    values_check = [clinical_id, clinician_id]
                    count = db.querydatafromdatabase(sql_check, values_check)

                    if count.iloc[0, 0] == 0:
                        sql = """
                            INSERT INTO clinician_assignment (clinical_exam_id, clinician_id, clinician_assignment_modified_date)
                            VALUES (%s, %s, %s)
                        """
                        values = [clinical_id, clinician_id, modified_date]
                        db.modifydatabase(sql, values)

                    elif count.iloc[0, 0] == 1:
                        sql = """
                            UPDATE clinician_assignment
                            SET clinician_assignment_delete_ind = false,
                                clinician_assignment_modified_date = %s
                            WHERE clinical_exam_id = %s AND clinician_id = %s
                        """
                        values = [modified_date, clinical_id, clinician_id]
                        db.modifydatabase(sql, values)
                
                sql_delete = """
                    UPDATE clinician_assignment
                    SET clinician_assignment_delete_ind = true,
                        clinician_assignment_modified_date = %s
                    WHERE clinical_exam_id = %s AND clinician_id NOT IN %s
                """
                values_delete = [modified_date, clinical_id, tuple(clinician)]
                db.modifydatabase(sql_delete, values_delete)
                
                modal_open = True

                if mode == "add":
                    patient_link = f'/editproblem?mode=add&problem_id={problem_id}&patient_id={patient_id}'
                elif mode == "edit":
                    patient_link = f'/editproblem?mode=edit&problem_id={problem_id}&patient_id={patient_id}'
                else:
                    patient_link = f'/editproblem?mode=edit&problem_id={problem_id}&patient_id={patient_id}'

            return [alert_color, alert_text, alert_open, modal_open, patient_link]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
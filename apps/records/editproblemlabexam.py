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
        dbc.Alert(id='problemlabexam_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="problemlabexam_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H2("Lab Exam Details"),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Lab Exam Type"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="problemlabexam_namelist",
                        placeholder='Select Lab Exam Type',
                        searchable=True,
                        options=[],
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Lab Exam Results"), width=3),
                dbc.Col(
                    dcc.Textarea(
                        id="problemlabexam_results",
                        placeholder='Enter results',
                        style={"height":100, 'width':'100%'},
                        contentEditable=True
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Lab Exam From Vetmed?"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="problemlabexam_fromvetmed",
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
                dbc.Col(html.H4("Vetmed Examiner"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="problemlabexam_examiner",
                        placeholder='Select Lab Examiner (if from vetmed)',
                        searchable=True,
                        options=[],
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Delete Record?"), width=3),
                dbc.Col(
                    dbc.Checklist(
                        id='problemlabexam_delete',
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
            id = 'problemlabexam_save',
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
                    id="problemlabexam_return-button",
                )
            )
        ],
        centered = True, 
        id = 'problemlabexam_successmodal',
        backdrop = 'static'
        )
    ]
)



@app.callback(  #initial values
    Output('problemlabexam_namelist', 'options'),
    Output('problemlabexam_namelist', 'value'),
    Output('problemlabexam_results', 'value'),
    Output('problemlabexam_fromvetmed', 'value'),
    Output('problemlabexam_examiner', 'options'),
    Output('problemlabexam_examiner', 'value'),
    Output('problemlabexam_return-link', 'href'),
    Input('url','search'),
)
def problemclinicalexam_initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    patient_link= ""

    if 'note_id' in query_ids and 'lab_id' in query_ids:
        note_id = query_ids.get('note_id', [None])[0]
        lab_id = query_ids.get('lab_id', [None])[0]
        mode = query_ids.get('mode', [None])[0]

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
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['lab_exam_type_m'], 'value': row['lab_exam_type_id']} for _, row in result.iterrows()]

        sql = """
            SELECT 
                vet_id,
                COALESCE(vet_ln, '') || ', ' || COALESCE (vet_fn, '') || ' ' || COALESCE (vet_mi, '') AS vet_name
            FROM 
                vet
            WHERE 
                NOT vet_delete_ind
        """
        values = []
        cols = ['vet_id', 'vet_name']
        result = db.querydatafromdatabase(sql, values, cols)
        options2 = [{'label': row['vet_name'], 'value': row['vet_id']} for _, row in result.iterrows()]
        
        sql = """
            SELECT lab_exam_type_id, lab_exam_results, lab_exam_from_vetmed, lab_exam_vetmed_examiner_id
            FROM lab_exam
            WHERE lab_exam_type_id = %s AND note_id = %s AND lab_exam_delete_ind = false
        """
        values = [lab_id, note_id]
        col = ['lab_exam_type', 'lab_exam_results', 'from_vetmed', 'lab_exam_examiner']
        df = db.querydatafromdatabase(sql, values, col)

        lab_exam_type = df['lab_exam_type'][0]
        lab_exam_results = df['lab_exam_results'][0]
        from_vetmed = df['from_vetmed'][0]
        lab_exam_examiner = df['lab_exam_examiner'][0]

        sql = """
            SELECT problem.problem_id, patient.patient_id
            FROM lab_exam
            INNER JOIN note ON lab_exam.note_id = note.note_id
            INNER JOIN problem ON note.problem_id = problem.problem_id
            INNER JOIN visit ON note.visit_id = visit.visit_id
            INNER JOIN patient ON visit.patient_id = patient.patient_id
            WHERE lab_exam_type_id = %s AND note.note_id = %s
        """
        values = [lab_id, note_id]
        col = ['problem_id', 'patient_id']
        df = db.querydatafromdatabase(sql, values, col)

        problem_id = df['problem_id'][0]
        patient_id = df['patient_id'][0]

        if mode == "add":
            patient_link = f'/editproblemnote?mode=add&note_id={note_id}&problem_id={problem_id}&patient_id={patient_id}'
        elif mode == "edit":
            patient_link = f'/editproblemnote?mode=edit&note_id={note_id}&problem_id={problem_id}&patient_id={patient_id}'
        else:
            patient_link = f'/editproblemnote?mode=edit&note_id={note_id}&problem_id={problem_id}&patient_id={patient_id}'

        return (options, lab_exam_type, lab_exam_results, from_vetmed, options2, lab_exam_examiner, patient_link)
    
    else:
        raise PreventUpdate
    


@app.callback( #save changes
    Output('problemlabexam_alert','color'),
    Output('problemlabexam_alert','children'),
    Output('problemlabexam_alert','is_open'),
    Output('problemlabexam_successmodal', 'is_open'),
    Output('problemlabexam_return-button', 'href'),
    Input('problemlabexam_save', 'n_clicks'),
    Input('url','search'),
    Input('problemlabexam_namelist', 'value'),
    Input('problemlabexam_results', 'value'),
    Input('problemlabexam_fromvetmed', 'value'),
    Input('problemlabexam_examiner', 'value'),
    Input('problemlabexam_delete','value'),
)
def save_labexam_record(submitbtn, url_search, lab_type, results, fromvetmed, examiner, delete):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'problemlabexam_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            patient_link = ''

            lab_id = query_ids.get('lab_id', [None])[0]
            note_id = query_ids.get('note_id', [None])[0]    
            mode = query_ids.get('mode', [None])[0]

            if not lab_type:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select lab exam type'
            elif not results:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter results'
            elif fromvetmed is None:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select if lab exam is done on vetmed or not'
            else:
                to_delete = bool(delete)
                modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
                
                sql = """
                    SELECT problem.problem_id, patient.patient_id
                    FROM lab_exam
                    INNER JOIN note ON lab_exam.note_id = note.note_id
                    INNER JOIN problem ON note.problem_id = problem.problem_id
                    INNER JOIN visit ON note.visit_id = visit.visit_id
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                    WHERE lab_exam_type_id = %s AND note.note_id = %s
                """
                values = [lab_id, note_id]
                col = ['problem_id', 'patient_id']
                df = db.querydatafromdatabase(sql, values, col)

                problem_id = df['problem_id'][0]
                patient_id = df['patient_id'][0]

                if mode == "add":
                    patient_link = f'/editproblemnote?mode=add&note_id={note_id}&problem_id={problem_id}&patient_id={patient_id}'
                elif mode == "edit":
                    patient_link = f'/editproblemnote?mode=edit&note_id={note_id}&problem_id={problem_id}&patient_id={patient_id}'
                else:
                    patient_link = f'/editproblemnote?mode=edit&note_id={note_id}&problem_id={problem_id}&patient_id={patient_id}'

                sql = """
                    UPDATE lab_exam
                    SET 
                        lab_exam_type_id = %s,
                        lab_exam_results = %s,
                        lab_exam_from_vetmed = %s,
                        lab_exam_vetmed_examiner_id = %s,
                        lab_exam_modified_date = %s,
                        lab_exam_delete_ind = %s 
                    FROM note
                        WHERE note.note_id = %s AND lab_exam_type_id = %s
                    """
                values = [lab_type, results, fromvetmed, examiner, modified_date, to_delete, note_id, lab_id]
                db.modifydatabase(sql, values)

                modal_open = True

            return [alert_color, alert_text, alert_open, modal_open, patient_link]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
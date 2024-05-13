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
        dbc.Alert(id='addproblemlabexam_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="addproblemlabexam_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H2("Lab Exam Details"),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Lab Exam Type"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="addproblemlabexam_namelist",
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
                        id="addproblemlabexam_results",
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
                        id="addproblemlabexam_fromvetmed",
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
                        id="addproblemlabexam_examiner",
                        placeholder='Select Lab Examiner (if from vetmed)',
                        searchable=True,
                        options=[],
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
        ]),
        html.Br(),
        dbc.Button(
            'Save',
            id = 'addproblemlabexam_save',
            n_clicks = 0,
            className='custom-submitbutton',
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H3('Save Success')),
            dbc.ModalFooter(
                dbc.Button(
                    "Return",
                    href="",
                    id="addproblemlabexam_return-button",
                )
            )
        ],
        centered = True, 
        id = 'addproblemlabexam_successmodal',
        backdrop = 'static'
        )
    ]
)



@app.callback(  #initial values
    Output('addproblemlabexam_namelist', 'options'),
    Output('addproblemlabexam_examiner', 'options'),
    Output('addproblemlabexam_return-link', 'href'),
    Input('url','search'),
)
def problemclinicalexam_initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    return_link= ""

    if 'note_id' in query_ids and 'problem_id' in query_ids and 'patient_id' in query_ids:
        patient_id = query_ids['patient_id'][0]
        problem_id = query_ids['problem_id'][0]
        note_id = query_ids['note_id'][0]

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
        
        return_link = f'/editproblemnote?mode=add&note_id={note_id}&problem_id={problem_id}&patient_id={patient_id}'

        return (options, options2, return_link)
    
    else:
        raise PreventUpdate
    


@app.callback( #save changes
    Output('addproblemlabexam_alert','color'),
    Output('addproblemlabexam_alert','children'),
    Output('addproblemlabexam_alert','is_open'),
    Output('addproblemlabexam_successmodal', 'is_open'),
    Output('addproblemlabexam_return-button', 'href'),
    Input('addproblemlabexam_save', 'n_clicks'),
    Input('url','search'),
    Input('addproblemlabexam_namelist', 'value'),
    Input('addproblemlabexam_results', 'value'),
    Input('addproblemlabexam_fromvetmed', 'value'),
    Input('addproblemlabexam_examiner', 'value'),
)
def save_labexam_record(submitbtn, url_search, lab_type, results, fromvetmed, examiner):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'addproblemlabexam_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            patient_link = ''

            note_id = query_ids.get('note_id', [None])[0]
            patient_id = query_ids.get('patient_id', [None])[0]
            problem_id = query_ids.get('problem_id', [None])[0]

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
                modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
                sql = """
                    SELECT MAX(lab_exam_no)
                    FROM lab_exam
                    WHERE note_id = %s
                    """
                values = [note_id]
                df = db.querydatafromdatabase(sql,values)
                labexam_no_before = int(df.loc[0,0]) if not pd.isna(df.loc[0,0]) else 0
                labexam_no_new = labexam_no_before + 1

                sql = """
                    INSERT INTO lab_exam(
                        note_id,
                        lab_exam_no,
                        lab_exam_type_id,
                        lab_exam_results,
                        lab_exam_from_vetmed,
                        lab_exam_vetmed_examiner_id,
                        lab_exam_modified_date,
                        lab_exam_delete_ind
                    )
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [note_id, labexam_no_new, lab_type, results, fromvetmed, examiner, modified_date, False]
                db.modifydatabase(sql, values)

                patient_link = f'/editproblemnote?mode=add&note_id={note_id}&problem_id={problem_id}&patient_id={patient_id}'

                modal_open = True

            return [alert_color, alert_text, alert_open, modal_open, patient_link]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
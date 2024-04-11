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
        dbc.Alert(id='problemnote_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="problemnote_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H2("Note Details"),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Have Been Tested?"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="problemnote_tested",
                        searchable=True,
                        options=[
                            {"label": "Yes", "value": True},
                            {"label": "No", "value": False},
                        ]
                    ),
                    width=6,
                ),
            ]),
            html.Br(),
            html.Br(),
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.H2("Laboratory Exams", className = 'flex-grow-1'),
                        html.Div(dbc.Button("Add Laboratory Exam", id = "problem_labexam_btn"), className = "ml-2 d-flex"),
                    ], className = "d-flex align-items-center justify-content-between")
                ]),
                dbc.CardBody([
                    html.Div([
                        html.Div(id='labexams-table'),   
                    ])
                ])
            ]),
            html.Br(),
            html.Br(),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Differential Diagnosis"), width=3),
                dbc.Col(
                    dcc.Textarea(
                        id="problemnote_diagnosis",
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
                        id="problemnote_treatment",
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
                        id="problemnote_tests",
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
                        id="problemnote_bill",
                        placeholder="Enter Bill",
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Delete Record?"), width=3),
                dbc.Col(
                    dbc.Checklist(
                        id='problemnote_delete',
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
            id = 'problemnote_save',
            n_clicks = 0,
            className='custom-submitbutton',
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H3('Save Success')),
            dbc.ModalFooter(
                dbc.Button(
                    "Return",
                    href="",
                    id="problemnote_return-button",
                )
            )
        ],
        centered = True, 
        id = 'problemnote_successmodal',
        backdrop = 'static'
        )
    ]
)



@app.callback( #laboratory exam table
    Output('labexams-table', 'children'),
    Input('url', 'search'),
)
def labexam_table(url_search):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)

    if 'patient_id' in query_id and 'problem_id' in query_id and 'note_id' in query_id:
        patient_id = query_id.get('patient_id', [None])[0]
        problem_id = query_id.get('problem_id', [None])[0]
        note_id = query_id.get('note_id', [None])[0]
        mode = query_id.get('mode', [None])[0]

        sql = """
        SELECT 
            lab_exam_type_m, lab_exam_results, lab_exam_from_vetmed,
            COALESCE(vet_ln, '') || ', ' || COALESCE (vet_fn, '') || ' ' || COALESCE (vet_mi, '') AS vet_name,
            lab_exam.lab_exam_type_id, note.note_id
        FROM 
            lab_exam
        INNER JOIN lab_exam_type ON lab_exam.lab_exam_type_id = lab_exam_type.lab_exam_type_id
        INNER JOIN vet ON lab_exam.lab_exam_vetmed_examiner_id = vet.vet_id
        INNER JOIN note ON lab_exam.note_id = note.note_id
        WHERE note.note_id = %s AND lab_exam_delete_ind = false
        """
        values = [note_id]
        sql += "ORDER BY lab_exam_no DESC"
        col = ['Lab Exam Type', 'Lab Exam Results', 'From Vetmed?', 'Vetmed Examiner', 'Lab_ID', 'Note_ID']
        df = db.querydatafromdatabase(sql, values, col)

        if df.shape:
            df['From Vetmed?'] = df['From Vetmed?'].apply(lambda x: 'Yes' if x else 'No')

            buttons = []
            for note_id, lab_id, in zip(df['Note_ID'], df['Lab_ID']):
                if mode == "add":
                    hreflab = f'/editproblemlabexam?mode=add&note_id={note_id}&lab_id={lab_id}'
                elif mode == "edit":
                    hreflab = f'/editproblemlabexam?mode=edit&note_id={note_id}&lab_id={lab_id}'
                else:
                    hreflab = f'/editproblemlabexam?mode=edit&note_id={note_id}&lab_id={lab_id}'
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=hreflab, size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Lab Exam Type', 'Lab Exam Results', 'From Vetmed?', 'Vetmed Examiner', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate



@app.callback(  #initial values
    Output('problemnote_tested', 'value'),
    Output('problemnote_diagnosis', 'value'),
    Output('problemnote_treatment', 'value'),
    Output('problemnote_tests', 'value'),
    Output('problemnote_bill', 'value'),
    Output('problemnote_return-link', 'href'),
    Input('url','search'),
)
def problemnote_initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    patient_link= ""

    if 'patient_id' in query_ids and 'problem_id' in query_ids and 'note_id' in query_ids:
        patient_id = query_ids.get('patient_id', [None])[0]
        problem_id = query_ids.get('problem_id', [None])[0]
        note_id = query_ids.get('note_id', [None])[0]
        mode = query_ids.get('mode', [None])[0]
        
        sql = """
            SELECT note_have_been_tested, note_differential_diagnosis, note_treatment, note_for_testing, note_bill
            FROM note
            INNER JOIN problem ON note.problem_id = problem.problem_id
            INNER JOIN visit ON note.visit_id = visit.visit_id
            INNER JOIN patient ON visit.patient_id = patient.patient_id
            WHERE note_id = %s AND problem.problem_id = %s AND patient.patient_id = %s
        """
        values = [note_id, problem_id, patient_id]
        col = ['tested', 'diagnosis', 'treatment', 'testing', 'bill']
        df = db.querydatafromdatabase(sql, values, col)

        tested = df['tested'][0]
        diagnosis = df['diagnosis'][0]
        treatment = df['treatment'][0]
        testing = df['testing'][0]
        bill = df['bill'][0]

        if mode == "add":
            patient_link = f'/editproblem?mode=add&problem_id={problem_id}&patient_id={patient_id}'
        elif mode == "edit":
            patient_link = f'/editproblem?mode=edit&problem_id={problem_id}&patient_id={patient_id}'
        else:
            patient_link = f'/editproblem?mode=edit&problem_id={problem_id}&patient_id={patient_id}'

        return (tested, diagnosis, treatment, testing, bill, patient_link)
    
    else:
        raise PreventUpdate
    


@app.callback( #save changes
    Output('problemnote_alert','color'),
    Output('problemnote_alert','children'),
    Output('problemnote_alert','is_open'),
    Output('problemnote_successmodal', 'is_open'),
    Output('problemnote_return-button', 'href'),
    Input('problemnote_save', 'n_clicks'),
    Input('url','search'),
    Input('problemnote_tested','value'),
    Input('problemnote_diagnosis','value'),
    Input('problemnote_treatment','value'),
    Input('problemnote_tests','value'),
    Input('problemnote_bill','value'),
    Input('problemnote_delete','value'),
)
def save_note_record(submitbtn, url_search, note_tested, note_diagnosis, note_treatment, note_tests, note_bill, note_delete):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'problemnote_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            patient_link = ''

            problem_id = query_ids.get('problem_id', [None])[0]
            patient_id = query_ids.get('patient_id', [None])[0]
            note_id = query_ids.get('note_id', [None])[0]    
            mode = query_ids.get('mode', [None])[0]

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
                to_delete = bool(note_delete)
                sql = """
                    UPDATE note
                    SET 
                        note_have_been_tested = %s,
                        note_differential_diagnosis = %s,
                        note_treatment = %s,
                        note_for_testing = %s,
                        note_bill = %s,
                        note_delete_ind = %s 
                    FROM visit
                        INNER JOIN patient ON visit.patient_id = patient.patient_id
                        WHERE visit.problem_id = %s AND patient.patient_id = %s AND note.note_id = %s
                    """
                values = [note_tested, note_diagnosis, note_treatment, note_tests, note_bill, to_delete, problem_id, patient_id, note_id]
                db.modifydatabase(sql, values)

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
    

@app.callback( #disable add button if mode=edit
    Output('problem_labexam_btn', 'disabled'),
    Input('url', 'search')
)
def disablebuttons(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    disabled = False
    if 'mode' in query_ids:
        mode = query_ids.get('mode', [None])[0]
        if mode == "add":
            return [disabled]
        elif mode == "edit":
            disabled = True
            return [disabled]
        else:
            return [disabled]
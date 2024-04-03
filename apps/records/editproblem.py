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
        dbc.Alert(id='problem_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="problem_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        dbc.Row([
                dbc.Col(html.H2("Problem Chief Complaint"), width=3),
                dbc.Col(
                    dbc.Textarea(
                        id="problem_complaint",
                        placeholder="Describe the overall problem",
                        style={"height":50, 'width':'100%'},
                    ),
                    width=6,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="problem_status",
                        placeholder="Select Problem Status",
                        searchable=True,
                        options=[],
                    ),
                    width=3,
                )
            ]),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Medical History"), width=3),
                dbc.Col(
                    dbc.Textarea(
                        id="problem_medhistory",
                        placeholder='Enter any relevant medical history',
                        style={"height":50, 'width':'100%'},
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Diet"), width=3),
                dbc.Col(
                    dbc.Textarea(
                        id="problem_diet",
                        placeholder="Enter patient's general diet",
                        style={"height":50, 'width':'100%'},
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Water Source"), width=3),
                dbc.Col(
                    dbc.Textarea(
                        id="problem_watersource",
                        placeholder="Enter patient's general source of hydration",
                        style={"height":50, 'width':'100%'},
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Age"), width=3),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id="problem_age",
                        placeholder="Enter patient's age",
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Temperature"), width=3),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id="problem_temperature",
                        placeholder="Enter patient's temperature in °C",
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Weight"), width=3),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id="problem_weight",
                        placeholder="Enter patient's weight in kilogram",
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Pulse Rate"), width=3),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id="problem_pulserate",
                        placeholder="Enter patient's pulse rate per min",
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Respiration Rate"), width=3),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id="problem_respirationrate",
                        placeholder="Enter patient's respiration rate per min",
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Body Condition Score"), width=3),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id="problem_bodyconditionscore",
                        placeholder="Enter patient's condition score (1-9)",
                    ),
                    width=6,
                )
            ]),
            html.Br(),
            html.Br(),
            dbc.Card([
                dbc.CardHeader([
                    html.H2('Clinical Exams')
                ]),
                dbc.CardBody([
                    html.Div([
                        html.Div(id='clinicalexams-table'),   
                    ])
                ])
            ]),
            html.Br(),
            dbc.Card([
                dbc.CardHeader([
                    html.H2('Progress Notes')
                ]),
                dbc.CardBody([
                    html.Div([
                        html.Div(id='progressnotes-table'),   
                    ])
                ])
            ]),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col(html.H4("Diagnosis"), width=3),
                dbc.Col(
                    dbc.Textarea(
                        id="problem_diagnosis",
                        placeholder='Enter Diagnosis',
                        style={"height":50, 'width':'100%'},
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Prescription"), width=3),
                dbc.Col(
                    dbc.Textarea(
                        id="problem_prescription",
                        placeholder='Enter Prescription',
                        style={"height":50, 'width':'100%'},
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Patient Instructions"), width=3),
                dbc.Col(
                    dbc.Textarea(
                        id="problem_clienteduc",
                        placeholder='Enter Instructions',
                        style={"height":50, 'width':'100%'},
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Delete Record?"), width=3),
                dbc.Col(
                    dbc.Checklist(
                        id='problem_delete',
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
            id = 'problem_save',
            n_clicks = 0,
            className='custom-submitbutton',
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H3('Save Success')),
            dbc.ModalFooter(
                dbc.Button(
                    "Return",
                    href="",
                    id="problem_return-button",
                )
            )
        ],
        centered = True, 
        id = 'problem_successmodal',
        backdrop = 'static'
        )
    ]
)


@app.callback( #clinical exam table
    Output('clinicalexams-table', 'children'),
    Input('url', 'search'),
)
def clinicalexam_table(url_search):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)

    if 'patient_id' in query_id and 'problem_id' in query_id:
        patient_id = query_id.get('patient_id', [None])[0]
        problem_id = query_id.get('problem_id', [None])[0]
        sql = """
        SELECT 
            clinical_exam_type_m, clinical_exam_ab_findings, clinical_exam.clinical_exam_id, problem.problem_id, patient.patient_id
        FROM 
            clinical_exam
        INNER JOIN problem ON clinical_exam.problem_id = problem.problem_id
        INNER JOIN clinical_exam_type ON clinical_exam.clinical_exam_type_id = clinical_exam_type.clinical_exam_type_id
        INNER JOIN visit ON problem.problem_id = visit.problem_id
        INNER JOIN patient ON visit.patient_id = patient.patient_id
        WHERE patient.patient_id = %s AND problem.problem_id = %s AND clinical_exam_delete_ind = false
        """
        values = [patient_id, problem_id]
        sql += "ORDER BY clinical_exam_no DESC"
        col = ['Clinical Exam', 'Findings', 'Clinical_ID', 'Problem_ID', 'Patient_ID']
        df = db.querydatafromdatabase(sql, values, col)

        if df.shape:
            buttons = []
            for clinical_id, problem_id, patient_id in zip(df['Clinical_ID'], df['Problem_ID'], df['Patient_ID']):
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editproblemclinicalexam?mode=edit&clinical_id={clinical_id}&problem_id={problem_id}&patient_id={patient_id}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Clinical Exam', 'Findings', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate
    

@app.callback( #progress notes table
    Output('progressnotes-table', 'children'),
    Input('url', 'search'),
)
def clinicalexam_table(url_search):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)

    if 'patient_id' in query_id and 'problem_id' in query_id:
        patient_id = query_id.get('patient_id', [None])[0]
        problem_id = query_id.get('problem_id', [None])[0]
        sql = """
        SELECT 
            visit_date, note_differential_diagnosis, note_treatment, note_for_testing, note.note_id, problem.problem_id, patient.patient_id
        FROM 
            note
        INNER JOIN problem ON note.problem_id = problem.problem_id
        INNER JOIN visit ON note.visit_id = visit.visit_id
        INNER JOIN patient ON visit.patient_id = patient.patient_id
        WHERE patient.patient_id = %s AND problem.problem_id = %s AND note_delete_ind = false
        """
        values = [patient_id, problem_id]
        sql += "ORDER BY visit_date DESC"
        col = ['Visit Date', 'Differential Diagnosis', 'Treatment', 'Tests Needed', 'Note_ID', 'Problem_ID', 'Patient_ID']
        df = db.querydatafromdatabase(sql, values, col)

        if df.shape:
            buttons = []
            for note_id, problem_id, patient_id in zip(df['Note_ID'], df['Problem_ID'], df['Patient_ID']):
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editproblemnote?mode=edit&note_id={note_id}&problem_id={problem_id}&patient_id={patient_id}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Visit Date', 'Differential Diagnosis', 'Treatment', 'Tests Needed', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate
    

@app.callback(  #initial values
    Output('problem_status', 'options'),
    Output('problem_status', 'value'),
    Output('problem_complaint', 'value'),
    Output('problem_medhistory', 'value'),
    Output('problem_diet', 'value'),
    Output('problem_watersource', 'value'),
    Output('problem_age', 'value'),
    Output('problem_temperature', 'value'),
    Output('problem_weight', 'value'),
    Output('problem_pulserate', 'value'),
    Output('problem_respirationrate', 'value'),
    Output('problem_bodyconditionscore', 'value'),
    Output('problem_diagnosis', 'value'),
    Output('problem_prescription', 'value'),
    Output('problem_clienteduc', 'value'),
    Output('problem_return-link', 'href'),
    Input('url','search'),
)
def problem_initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    patient_link= ""

    if 'patient_id' in query_ids and 'problem_id' in query_ids:
        patient_id = query_ids.get('patient_id', [None])[0]
        problem_id = query_ids.get('problem_id', [None])[0]

        sql = """
            SELECT 
                problem_status_id,
                problem_status_m
            FROM 
                problem_status 
            WHERE 
                NOT problem_status_delete_ind
        """
        values = []
        cols = ['problem_status_id', 'problem_status_m']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['problem_status_m'], 'value': row['problem_status_id']} for _, row in result.iterrows()]
        
        sql = """
            SELECT problem.problem_status_id, problem_chief_complaint, problem_medical_history, problem_diet_source, problem_water_source, problem_animalage, problem_temp, 
            problem_weight, problem_pr, problem_rr, problem_bodycondition_score, problem_diagnosis, problem_prescription, problem_client_educ
            FROM problem
            INNER JOIN visit ON problem.problem_id = visit.problem_id
            INNER JOIN patient ON visit.patient_id = patient.patient_id
            WHERE problem.problem_id = %s AND patient.patient_id = %s
        """
        values = [problem_id, patient_id]
        col = ['problem_status', 'problem_complaint', 'problem_medhistory', 'problem_diet', 'problem_watersource', 'problem_age', 'problem_temperature', 'problem_weight', 'problem_pulserate',
               'problem_respirationrate', 'problem_bodyconditionscore', 'problem_diagnosis', 'problem_prescription', 'problem_clienteduc']
        df = db.querydatafromdatabase(sql, values, col)

        problem_status = df['problem_status'][0]
        problem_complaint = df['problem_complaint'][0]
        problem_medhistory = df['problem_medhistory'][0]
        problem_diet = df['problem_diet'][0]
        problem_watersource = df['problem_watersource'][0]
        problem_age = df['problem_age'][0]
        problem_temperature = df['problem_temperature'][0]
        problem_weight = df['problem_weight'][0]
        problem_pulserate = df['problem_pulserate'][0]
        problem_respirationrate = df['problem_respirationrate'][0]
        problem_bodyconditionscore = df['problem_bodyconditionscore'][0]
        problem_diagnosis = df['problem_diagnosis'][0]
        problem_prescription = df['problem_prescription'][0]
        problem_clienteduc = df['problem_clienteduc'][0]


        patient_link = f'/editrecord?mode=edit&id={patient_id}'

        return (options, problem_status, problem_complaint, problem_medhistory, problem_diet, problem_watersource, problem_age, problem_temperature, problem_weight, problem_pulserate, 
                problem_respirationrate, problem_bodyconditionscore, problem_diagnosis, problem_prescription, problem_clienteduc, patient_link)
    else:
        raise PreventUpdate
    

@app.callback( #save changes
    Output('problem_alert','color'),
    Output('problem_alert','children'),
    Output('problem_alert','is_open'),
    Output('problem_successmodal', 'is_open'),
    Output('problem_return-button', 'href'),
    Input('problem_save', 'n_clicks'),
    Input('url','search'),
    Input('problem_status', 'value'),
    Input('problem_complaint', 'value'),
    Input('problem_medhistory', 'value'),
    Input('problem_diet', 'value'),
    Input('problem_watersource', 'value'),
    Input('problem_age', 'value'),
    Input('problem_temperature', 'value'),
    Input('problem_weight', 'value'),
    Input('problem_pulserate', 'value'),
    Input('problem_respirationrate', 'value'),
    Input('problem_bodyconditionscore', 'value'),
    Input('problem_diagnosis', 'value'),
    Input('problem_prescription', 'value'),
    Input('problem_clienteduc', 'value'),
    Input('problem_delete','value'),
)
def save_deworm_record(submitbtn, url_search, problem_status, problem_complaint, problem_medhistory, problem_diet, problem_watersource, problem_age, problem_temperature, problem_weight,
                       problem_pulserate, problem_respirationrate, problem_bodyconditionscore, problem_diagnosis, problem_prescription, problem_clienteduc, problem_delete):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'problem_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            patient_link = ''

            problem_id = query_ids.get('problem_id', [None])[0]
            patient_id = query_ids.get('patient_id', [None])[0]    

            if not problem_status:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select problem status'
            elif not problem_complaint:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter chief complaint'
            elif not problem_medhistory:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter relevant medical history'
            elif not problem_diet:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please enter patient's diet"
            elif not problem_watersource:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please enter patient's water source"
            elif not problem_age:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please enter patient's age"
            elif not problem_temperature:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter temperature'
            elif not problem_weight:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter weight'
            elif not problem_pulserate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter pulse rate'
            elif not problem_respirationrate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter respiration rate'
            elif not problem_bodyconditionscore:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter body condition score'
            elif not problem_diagnosis:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter diagnosis'
            elif not problem_prescription:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter prescription'
            elif not problem_clienteduc:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter instructions'
            else:
                sql = """
                        SELECT 
                            problem_status_id
                        FROM problem
                        INNER JOIN visit ON problem.problem_id = visit.problem_id
                        INNER JOIN patient ON visit.patient_id = patient.patient_id
                        WHERE
                            problem.problem_id = %s AND patient.patient_id = %s
                    """
                values = [problem_id, patient_id]
                cols = ['problem_status_id']
                df = db.querydatafromdatabase(sql, values, cols)

                problem_status_current = df['problem_status_id'][0]

                if problem_status_current != 1 and problem_status == 1:
                    to_delete = bool(problem_delete)
                    modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    sql = """
                        UPDATE problem
                        SET 
                            problem_status_id = %s,
                            problem_chief_complaint = %s,
                            problem_medical_history = %s,
                            problem_diet_source = %s,
                            problem_water_source = %s,
                            problem_animalage = %s, 
                            problem_temp = %s, 
                            problem_weight = %s,
                            problem_pr = %s,
                            problem_rr = %s,
                            problem_bodycondition_score = %s,
                            problem_diagnosis = %s,
                            problem_prescription = %s,
                            problem_client_educ = %s,
                            problem_modified_date = %s,
                            problem_date_resolved = %s,
                            problem_delete_ind = %s
                        FROM visit
                        INNER JOIN patient ON visit.patient_id = patient.patient_id
                        WHERE problem.problem_id = %s AND patient.patient_id = %s
                    """
                    values = [problem_status, problem_complaint, problem_medhistory, problem_diet, problem_watersource, problem_age, problem_temperature, problem_weight,
                            problem_pulserate, problem_respirationrate, problem_bodyconditionscore, problem_diagnosis, problem_prescription, problem_clienteduc, modified_date,
                            modified_date, to_delete, problem_id, patient_id]
                    db.modifydatabase(sql, values)
                else:
                    to_delete = bool(problem_delete)
                    modified_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    sql = """
                        UPDATE problem
                        SET 
                            problem_status_id = %s,
                            problem_chief_complaint = %s,
                            problem_medical_history = %s,
                            problem_diet_source = %s,
                            problem_water_source = %s,
                            problem_animalage = %s, 
                            problem_temp = %s, 
                            problem_weight = %s,
                            problem_pr = %s,
                            problem_rr = %s,
                            problem_bodycondition_score = %s,
                            problem_diagnosis = %s,
                            problem_prescription = %s,
                            problem_client_educ = %s,
                            problem_modified_date = %s,
                            problem_delete_ind = %s
                        FROM visit
                        INNER JOIN patient ON visit.patient_id = patient.patient_id
                        WHERE problem.problem_id = %s AND patient.patient_id = %s
                    """
                    values = [problem_status, problem_complaint, problem_medhistory, problem_diet, problem_watersource, problem_age, problem_temperature, problem_weight,
                            problem_pulserate, problem_respirationrate, problem_bodyconditionscore, problem_diagnosis, problem_prescription, problem_clienteduc, modified_date, 
                            to_delete, problem_id, patient_id]
                    db.modifydatabase(sql, values)

                modal_open = True

                patient_link = f'/editrecord?mode=edit&id={patient_id}'

            return [alert_color, alert_text, alert_open, modal_open, patient_link]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
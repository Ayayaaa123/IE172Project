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
from datetime import datetime, timedelta
from dash import ALL, MATCH
from urllib.parse import urlparse, parse_qs
import plotly.graph_objs as go
import plotly.express as px

layout = html.Div(
    [
        html.H1("Generate Reports"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Row([
                            dbc.Col(html.H2("Select the Type of Report:"), width=3),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='reporttype',
                                    options=[
                                        {'label':'Number of Visits per Purpose per Period', 'value':'visitspurposeperiod'},
                                        {'label':'Monthly Number of Unresolved Problems', 'value':'monthlyunresolvedproblems'},
                                        {'label':'Number of Lab Exams per Type per Period', 'value':'labexamstypeperiod'},
                                        {'label':'Length of Processing', 'value':'lengthofprocessing'},
                                        {'label':'Number of Vaccine/Deworming Administered per Period', 'value':'vaccinedewormingadministeredperiod'},
                                    ],
                                    placeholder="Select Type of Report",
                                    multi=True,
                                ),
                                width=9,
                            ),
                        ]),
                    ]
                ),
                dbc.CardBody(
                    html.Div(id='reportdetails')
                ),
            ]
        ),
        html.Br(),
        dbc.Button(
            "Save",
            id = 'savebutton',
            n_clicks = 0, 
            className='custom-submitbutton',
        ),
        dcc.Download(id="savefiles")
    ]
)


@app.callback(
    Output("reportdetails", "children"),
    Input("reporttype", "value"),
)
def reportdetails(reporttype):
    if reporttype is None:
        return []
    
    inputs = []
    if 'visitspurposeperiod' in reporttype:
        inputs.extend([
            html.Div([
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Number of Visits per Purpose per Period")),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(html.H3("Select Time Period"), width=3),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='visitspurpose_timeperiod',
                                        options=[
                                            {'label':'Overall', 'value':'overall'},
                                            {'label':'Today', 'value':'today'},
                                            {'label':'This Week (Last 7 Days)', 'value':'thisweek'},
                                            {'label':'This Month', 'value':'thismonth'},
                                            {'label':'Custom', 'value':'custom'},
                                        ],
                                        value='overall'
                                    ),
                                    width=9,
                                ),
                            ]),
                            dcc.Store(id='visitspurpose_customdate_store'),
                            html.Div(id='visitspurpose_customdate'),
                            html.Br(),
                            html.Div([
                                dcc.Loading(
                                    id="visitspurpose_loading",
                                    type="circle",
                                    children=[
                                        dcc.Graph(id='visitspurpose_graphgenerated')
                                    ],
                                ),
                            ],
                            style={'width':'100%',"border": "3px #5c5c5c solid",} 
                            ),
                            html.Br(),
                            html.Div(id='visitspurpose_reportgenerated')
                        ]),
                    ],
                ),
                html.Br(),
            ])
        ])
    if 'monthlyunresolvedproblems' in reporttype:
        inputs.extend([
            html.Div([
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Monthly Number of Unresolved Problems")),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(html.H3("Select Year"), width=3),
                                dbc.Col(
                                    dcc.Dropdown(
                                        options=[{'label':x, 'value': x} for x in range(datetime.now().year, 2009, -1)],
                                        id='unresolvedproblems_selectedyear',
                                        searchable=True,
                                        placeholder="Select Year",
                                    ),
                                    width=9,
                                ),
                            ]),
                            html.Br(),
                            html.Div([
                                dcc.Loading(
                                    id="unresolvedproblems_loading",
                                    type="circle",
                                    children=[
                                        dcc.Graph(id='unresolvedproblems_graphgenerated')
                                    ],
                                ),
                            ],
                            style={'width':'100%',"border": "3px #5c5c5c solid",} 
                            ),
                            html.Br(),
                            html.Div(id='unresolvedproblems_reportgenerated')
                        ]),
                    ],
                ),
                html.Br(),
            ])
        ])
    if 'labexamstypeperiod' in reporttype:
        inputs.extend([
            html.Div([
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Number of Lab Exams per Type per Period")),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(html.H3("Select Time Period"), width=3),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='labexams_timeperiod',
                                        options=[
                                            {'label':'Overall', 'value':'overall'},
                                            {'label':'Today', 'value':'today'},
                                            {'label':'This Week (Last 7 Days)', 'value':'thisweek'},
                                            {'label':'This Month', 'value':'thismonth'},
                                            {'label':'Custom', 'value':'custom'},
                                        ],
                                        value='overall'
                                    ),
                                    width=9,
                                ),
                            ]),
                            dcc.Store(id='labexams_customdate_store'),
                            html.Div(id='labexams_customdate'),
                            html.Br(),
                            html.Div([
                                dcc.Loading(
                                    id="labexams_loading",
                                    type="circle",
                                    children=[
                                        dcc.Graph(id='labexams_graphgenerated')
                                    ],
                                ),
                            ],
                            style={'width':'100%',"border": "3px #5c5c5c solid",} 
                            ),
                            html.Br(),
                            html.Div(id='labexams_reportgenerated')
                        ]),
                    ],
                ),
                html.Br(),
            ])
        ])
    if 'lengthofprocessing' in reporttype:
        inputs.extend([
            html.Div([
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Length of Processing")),
                        dbc.CardBody([
                            html.Div([
                                dcc.Loading(
                                    id="processing_loading",
                                    type="circle",
                                    children=[
                                        dcc.Graph(id='processing_graphgenerated')
                                    ],
                                ),
                            ],
                            style={'width':'100%',"border": "3px #5c5c5c solid",} 
                            ),
                            html.Br(),
                            html.Div(id='processing_reportgenerated')
                        ]),
                    ],
                ),
                html.Br(),
            ])
        ])
    if 'vaccinedewormingadministeredperiod' in reporttype:
        inputs.extend([
            html.Div([
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Number of Vaccine/Deworming Administered per Period")),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(html.H3("Select Time Period"), width=3),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='vaccinesdeworming_timeperiod',
                                        options=[
                                            {'label':'Overall', 'value':'overall'},
                                            {'label':'Today', 'value':'today'},
                                            {'label':'This Week (Last 7 Days)', 'value':'thisweek'},
                                            {'label':'This Month', 'value':'thismonth'},
                                            {'label':'Custom', 'value':'custom'},
                                        ],
                                        value='overall'
                                    ),
                                    width=9,
                                ),
                            ]),
                            dcc.Store(id='vaccinesdeworming_customdate_store'),
                            html.Div(id='vaccinesdeworming_customdate'),
                            html.Br(),
                            html.Div([
                                dcc.Loading(
                                    id="vaccinesdeworming_loading",
                                    type="circle",
                                    children=[
                                        dcc.Graph(id='vaccinesdeworming_graphgenerated')
                                    ],
                                ),
                            ],
                            style={'width':'100%',"border": "3px #5c5c5c solid",} 
                            ),
                            html.Br(),
                            html.Div(id='vaccinesdeworming_reportgenerated')
                        ]),
                    ],
                ),
                html.Br(),
            ])
        ])
    
    return inputs
                    


@app.callback( #callback if customdate (visitpurpose)
    Output('visitspurpose_customdate', 'children'),
    Input('visitspurpose_timeperiod', 'value'),
)
def visitspurpose_customdate(selectedperiod):
    additionalinput = []
    if selectedperiod and 'custom' in selectedperiod:
        additionalinput.extend([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Start Date"),
                        dmc.DatePicker(
                            id='visitspurpose_startdate',
                            placeholder="Select Start Date",
                            inputFormat='MMM DD, YYYY',
                            dropdownType='modal',
                        ),
                    ],
                        width=6,
                    ),
                    dbc.Col([
                        dbc.Label("End Date"),
                        dmc.DatePicker(
                            id='visitspurpose_enddate',
                            placeholder="Select End Date",
                            inputFormat='MMM DD, YYYY',
                            dropdownType='modal',
                        ),
                    ],
                        width=6,
                    ),
                ])
            ])
        ])
    if selectedperiod and not 'custom' in selectedperiod:
        additionalinput = []
  
    return additionalinput

@app.callback( #callback to store custom date (visit purpose)
    Output('visitspurpose_customdate_store', 'data'),
    Input('visitspurpose_startdate', 'value'),
    Input('visitspurpose_enddate', 'value'),
)
def store_customdates_visitpurpose(start_date, end_date):
    return {'start_date':start_date, 'end_date':end_date}


@app.callback ( #callback to generate report 1
    Output('visitspurpose_reportgenerated', 'children'),
    Output('visitspurpose_graphgenerated', 'figure'),
    Input('reporttype', 'value'),
    Input('visitspurpose_timeperiod', 'value'),
    Input('visitspurpose_customdate_store', 'data')
)
def generatevisitpurpose(reporttype, timeperiod, stored_custom_dates):
    if 'visitspurposeperiod' in reporttype:
        start_date = ""
        end_date = ""
        startdate = None
        enddate = None
        if timeperiod == "today":
            start_date =  datetime.now().strftime("%Y-%m-%d")
            end_date =  datetime.now().strftime("%Y-%m-%d")
        elif timeperiod == "thisweek":
            start_date = (datetime.now() - timedelta(days = 6)).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
        elif timeperiod == "thismonth":
            start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
        elif timeperiod == "custom":
            if stored_custom_dates:
                startdate = stored_custom_dates.get('start_date', '')
                enddate = stored_custom_dates.get('end_date', '')
                if startdate and enddate != None:
                    start_date = datetime.strptime(startdate, "%Y-%m-%d").strftime("%Y-%m-%d")
                    end_date = datetime.strptime(enddate, "%Y-%m-%d").strftime("%Y-%m-%d")
        else:
            start_date = ""
            end_date = ""

        values = []
        
        sql = """
        SELECT
            'Vaccine' AS visit_purpose,
            COUNT(*) AS count
        FROM 
            visit
        WHERE visit_for_vacc = true
        """

        if timeperiod == "today" or timeperiod == "thisweek" or timeperiod == "thismonth" or (timeperiod == "custom" and (startdate and enddate != None)):
            sql += """
                    AND visit_date BETWEEN %s AND %s
                UNION
                SELECT
                    'Deworming' AS visit_purpose,
                    COUNT(*) AS count
                FROM 
                    visit
                WHERE visit_for_deworm = true
            """
            values += [f"{start_date}", f"{end_date}"]
        else:
            sql += """
                UNION
                SELECT
                    'Deworming' AS visit_purpose,
                    COUNT(*) AS count
                FROM 
                    visit
                WHERE visit_for_deworm = true
            """
        
        if timeperiod == "today" or timeperiod == "thisweek" or timeperiod == "thismonth" or (timeperiod == "custom" and (startdate and enddate != None)):
            sql += """
                AND visit_date BETWEEN %s AND %s
                UNION
                SELECT
                    'Problem' AS visit_purpose,
                    COUNT(*) AS count
                FROM 
                    visit
                WHERE visit_for_problem = true
            """
            values += [f"{start_date}", f"{end_date}"]
        else:
            sql += """
                UNION
                SELECT
                    'Problem' AS visit_purpose,
                    COUNT(*) AS count
                FROM 
                    visit
                WHERE visit_for_problem = true
            """
            
        if timeperiod == "today" or timeperiod == "thisweek" or timeperiod == "thismonth" or (timeperiod == "custom" and (startdate and enddate != None)):
            sql += """
                AND visit_date BETWEEN %s AND %s
                ;
            """
            values += [f"{start_date}", f"{end_date}"]
        else:
            sql += ";"

        cols = ['Visit Purpose', 'Count']

        df = db.querydatafromdatabase(sql, values, cols)

        num_visit_purpose = len(df['Visit Purpose'])
        colors = px.colors.qualitative.Set1[:num_visit_purpose]

        bar_trace = go.Bar(
                    x=df['Visit Purpose'],
                    y=df['Count'],
                    name='Count of Visit Purpose',
                    marker=dict(color=colors)
                )

        layout = go.Layout(
            xaxis={'title': "Visit Purpose"},
            yaxis={'title': "Count"},
            barmode='group',
            height = 500,
            width = 1500,
            margin={'b': 50, 't': 20, 'l': 175},
            hovermode='closest',
            autosize=False,
            dragmode='zoom',
        )

        figure = {'data':[bar_trace], 'layout':layout}

        table = dbc.Table.from_dataframe(df,striped=True,bordered=True,hover=True,size='sm')
        

        if df.shape[0]:
            return [table,figure]
        else:
            return ['No records to display', 'No figure to display']
    else:
        raise PreventUpdate
    


@app.callback( #callback to generate report 2
    Output('unresolvedproblems_reportgenerated', 'children'),
    Output('unresolvedproblems_graphgenerated', 'figure'),
    Input('reporttype', 'value'),
    Input('unresolvedproblems_selectedyear', 'value')
)
def generateunresolvedproblems(reporttype, selected_year):
    if 'monthlyunresolvedproblems' in reporttype:
        if selected_year:
            sql = """
            SELECT 
                TO_CHAR(problem_date_created, 'Month') AS month,
                COUNT(*) AS new_problems,
                SUM(CASE WHEN problem_date_resolved IS NULL THEN 1 ELSE 0 END) AS unresolved_problems
            FROM
                problem
            WHERE
                EXTRACT(YEAR FROM problem_date_created) = %s
            GROUP BY
                TO_CHAR(problem_date_created, 'Month')
            ORDER BY
                MIN(problem_date_created);
            """
            values = [f"{selected_year}"]

            cols = ['Month', 'New Problems', 'Unresolved Problems']

            df = db.querydatafromdatabase(sql, values, cols)

            if df is not None and not df.empty:
                num_month = len(df['Month'])
                colors = px.colors.qualitative.Set1[:num_month]
            
                bar_trace = go.Bar(
                        x=df['Month'],
                        y=df['Unresolved Problems'],
                        name='Number of Unresolved Problems',
                        marker=dict(color=colors)
                    )

                layout = go.Layout(
                    xaxis={'title': "Month"},
                    yaxis={'title': "Unresolved Problems"},
                    barmode='group',
                    height = 500,
                    width = 1500,
                    margin={'b': 50, 't': 20, 'l': 175},
                    hovermode='closest',
                    autosize=False,
                    dragmode='zoom',
                )

                figure = {'data':[bar_trace], 'layout':layout}

                table = dbc.Table.from_dataframe(df,striped=True,bordered=True,hover=True,size='sm')
                

                if df.shape[0]:
                    return [table, figure]
                else:
                    return ['No records to display', 'No figure to display']
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
        

@app.callback( #callback if customdate (labexams)
    Output('labexams_customdate', 'children'),
    Input('labexams_timeperiod', 'value'),
)
def labexams_customdate(selectedperiod):
    additionalinput = []
    if selectedperiod and 'custom' in selectedperiod:
        additionalinput.extend([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Start Date"),
                        dmc.DatePicker(
                            id='labexams_startdate',
                            placeholder="Select Start Date",
                            inputFormat='MMM DD, YYYY',
                            dropdownType='modal',
                        ),
                    ],
                        width=6,
                    ),
                    dbc.Col([
                        dbc.Label("End Date"),
                        dmc.DatePicker(
                            id='labexams_enddate',
                            placeholder="Select End Date",
                            inputFormat='MMM DD, YYYY',
                            dropdownType='modal',
                        ),
                    ],
                        width=6,
                    ),
                ])
            ])
        ])
    if selectedperiod and not 'custom' in selectedperiod:
        additionalinput = []
  
    return additionalinput


@app.callback( #callback to store custom date (labexams)
    Output('labexams_customdate_store', 'data'),
    Input('labexams_startdate', 'value'),
    Input('labexams_enddate', 'value'),
)
def store_customdates_labexams(start_date, end_date):
    return {'start_date':start_date, 'end_date':end_date}



@app.callback ( #callback to generate report 3
    Output('labexams_reportgenerated', 'children'),
    Output('labexams_graphgenerated', 'figure'),
    Input('reporttype', 'value'),
    Input('labexams_timeperiod', 'value'),
    Input('labexams_customdate_store', 'data')
)
def generatelabexams(reporttype, timeperiod, stored_custom_dates):
    if 'labexamstypeperiod' in reporttype:
        start_date = ""
        end_date = ""
        startdate = None
        enddate = None
        if timeperiod == "today":
            start_date =  datetime.now().strftime("%Y-%m-%d")
            end_date =  datetime.now().strftime("%Y-%m-%d")
        elif timeperiod == "thisweek":
            start_date = (datetime.now() - timedelta(days = 6)).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
        elif timeperiod == "thismonth":
            start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
        elif timeperiod == "custom":
            if stored_custom_dates:
                startdate = stored_custom_dates.get('start_date', '')
                enddate = stored_custom_dates.get('end_date', '')
                if startdate and enddate != None:
                    start_date = datetime.strptime(startdate, "%Y-%m-%d").strftime("%Y-%m-%d")
                    end_date = datetime.strptime(enddate, "%Y-%m-%d").strftime("%Y-%m-%d")
        else:
            start_date = ""
            end_date = ""

        sql = """
        SELECT
            lab_exam_type.lab_exam_type_m,
            COUNT(lab_exam.lab_exam_type_id) AS exam_count
        FROM
            lab_exam
        INNER JOIN 
            lab_exam_type ON lab_exam.lab_exam_type_id = lab_exam_type.lab_exam_type_id
        WHERE lab_exam_from_vetmed = 'true'
        """
        values = []

        if timeperiod == "today" or timeperiod == "thisweek" or timeperiod == "thismonth" or (timeperiod == "custom" and (startdate and enddate != None)):
            sql += "AND lab_exam_modified_date between %s and %s"
            values += [f"{start_date}", f"{end_date}"]
            
        sql += "GROUP BY lab_exam_type.lab_exam_type_id, lab_exam_type.lab_exam_type_m;"

        cols = ['Lab Exam Type', 'Count']

        df = db.querydatafromdatabase(sql, values, cols)

        num_lab_exam_types = len(df['Lab Exam Type'])
        colors = px.colors.qualitative.Set1[:num_lab_exam_types]

        bar_trace = go.Bar(
                    x=df['Lab Exam Type'],
                    y=df['Count'],
                    name='Count of Lab Exam Type',
                    marker=dict(color=colors)
                )

        layout = go.Layout(
            xaxis={'title': "Lab Exam Type"},
            yaxis={'title': "Count"},
            barmode='group',
            height = 500,
            width = 1500,
            margin={'b': 50, 't': 20, 'l': 175},
            hovermode='closest',
            autosize=False,
            dragmode='zoom',
        )

        figure = {'data':[bar_trace], 'layout':layout}

        table = dbc.Table.from_dataframe(df,striped=True,bordered=True,hover=True,size='sm')
        

        if df.shape[0]:
            return [table,figure]
        else:
            return ['No records to display', 'No figure to display']
    else:
        raise PreventUpdate
    

@app.callback( #callback to generate report 4
    Output('processing_reportgenerated', 'children'),
    Output('processing_graphgenerated', 'figure'),
    Input('reporttype', 'value'),
)
def generateunresolvedproblems(reporttype):
    if 'lengthofprocessing' in reporttype:
        sql = """
        SELECT CASE 
	        WHEN problem_date_resolved IS NULL THEN 'N/A'
	        ELSE CAST(problem_date_resolved - problem_date_created AS varchar)
            END AS resolution_time_in_days,
            COUNT(*) AS count
        FROM 
   	        problem
	    INNER JOIN 
            problem_status ON problem.problem_status_id = problem_status.problem_status_id
	    INNER JOIN 
            (SELECT DISTINCT patient_id, problem_id FROM visit) AS visits ON problem.problem_id = visits.problem_id
	    GROUP BY resolution_time_in_days
	    ORDER BY resolution_time_in_days
        """
        values = []

        cols = ['Number of Days', 'Count']

        df = db.querydatafromdatabase(sql, values, cols)

        if df is not None and not df.empty:
            num_days = len(df['Number of Days'])
            colors = px.colors.qualitative.Set1[:num_days]
            
            bar_trace = go.Bar(
                    x=df['Number of Days'],
                    y=df['Count'],
                    name='Length of Processing',
                    marker=dict(color=colors)
                )

            layout = go.Layout(
                xaxis={'title': "Number of Days"},
                yaxis={'title': "Count"},
                barmode='group',
                height = 500,
                width = 1500,
                margin={'b': 50, 't': 20, 'l': 175},
                hovermode='closest',
                autosize=False,
                dragmode='zoom',
            )

            figure = {'data':[bar_trace], 'layout':layout}

            table = dbc.Table.from_dataframe(df,striped=True,bordered=True,hover=True,size='sm')
                

            if df.shape[0]:
                return [table, figure]
            else:
                return ['No records to display', 'No figure to display']
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    


@app.callback( #callback if customdate (vaccinesdeworming)
    Output('vaccinesdeworming_customdate', 'children'),
    Input('vaccinesdeworming_timeperiod', 'value'),
)
def labexams_customdate(selectedperiod):
    additionalinput = []
    if selectedperiod and 'custom' in selectedperiod:
        additionalinput.extend([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Start Date"),
                        dmc.DatePicker(
                            id='vaccinesdeworming_startdate',
                            placeholder="Select Start Date",
                            inputFormat='MMM DD, YYYY',
                            dropdownType='modal',
                        ),
                    ],
                        width=6,
                    ),
                    dbc.Col([
                        dbc.Label("End Date"),
                        dmc.DatePicker(
                            id='vaccinesdeworming_enddate',
                            placeholder="Select End Date",
                            inputFormat='MMM DD, YYYY',
                            dropdownType='modal',
                        ),
                    ],
                        width=6,
                    ),
                ])
            ])
        ])
    if selectedperiod and not 'custom' in selectedperiod:
        additionalinput = []
  
    return additionalinput


@app.callback( #callback to store custom date (vaccinesdeworming)
    Output('vaccinesdeworming_customdate_store', 'data'),
    Input('vaccinesdeworming_startdate', 'value'),
    Input('vaccinesdeworming_enddate', 'value'),
)
def store_customdates_labexams(start_date, end_date):
    return {'start_date':start_date, 'end_date':end_date}



@app.callback ( #callback to generate report 5
    Output('vaccinesdeworming_reportgenerated', 'children'),
    Output('vaccinesdeworming_graphgenerated', 'figure'),
    Input('reporttype', 'value'),
    Input('vaccinesdeworming_timeperiod', 'value'),
    Input('vaccinesdeworming_customdate_store', 'data')
)
def generatelabexams(reporttype, timeperiod, stored_custom_dates):
    if 'vaccinedewormingadministeredperiod' in reporttype:
        start_date = ""
        end_date = ""
        startdate = None
        enddate = None
        if timeperiod == "today":
            start_date =  datetime.now().strftime("%Y-%m-%d")
            end_date =  datetime.now().strftime("%Y-%m-%d")
        elif timeperiod == "thisweek":
            start_date = (datetime.now() - timedelta(days = 6)).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
        elif timeperiod == "thismonth":
            start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
        elif timeperiod == "custom":
            if stored_custom_dates:
                startdate = stored_custom_dates.get('start_date', '')
                enddate = stored_custom_dates.get('end_date', '')
                if startdate and enddate != None:
                    start_date = datetime.strptime(startdate, "%Y-%m-%d").strftime("%Y-%m-%d")
                    end_date = datetime.strptime(enddate, "%Y-%m-%d").strftime("%Y-%m-%d")
        else:
            start_date = ""
            end_date = ""

        values = []
        
        sql = """
        SELECT 
	        'Vaccine' AS administered,
	        COUNT(*) AS count
        FROM
	        vacc
        WHERE
	        vacc_from_vetmed = true
        """

        if timeperiod == "today" or timeperiod == "thisweek" or timeperiod == "thismonth" or (timeperiod == "custom" and (startdate and enddate != None)):
            sql += """
                AND vacc_date_administered BETWEEN %s and %s
            UNION
            SELECT
	            'Deworming' AS administered,
	            COUNT(*) AS count
            FROM
	            deworm
            WHERE
	            deworm_from_vetmed = true
            """
            values += [f"{start_date}", f"{end_date}"]
        else:
            sql += """
            UNION
            SELECT
	            'Deworming' AS administered,
	            COUNT(*) AS count
            FROM
	            deworm
            WHERE
	            deworm_from_vetmed = true
            """
        
        if timeperiod == "today" or timeperiod == "thisweek" or timeperiod == "thismonth" or (timeperiod == "custom" and (startdate and enddate != None)):
            sql += "AND deworm_administered BETWEEN %s and %s;"
            values += [f"{start_date}", f"{end_date}"]
        else:
            sql += ";"

        cols = ['Administered', 'Count']

        df = db.querydatafromdatabase(sql, values, cols)

        num_administered = len(df['Administered'])
        colors = px.colors.qualitative.Set1[:num_administered]

        bar_trace = go.Bar(
                    x=df['Administered'],
                    y=df['Count'],
                    name='Count of Administered Vaccine/Deworming',
                    marker=dict(color=colors)
                )

        layout = go.Layout(
            xaxis={'title': "Administered Vaccine/Deworming"},
            yaxis={'title': "Count"},
            barmode='group',
            height = 500,
            width = 1500,
            margin={'b': 50, 't': 20, 'l': 175},
            hovermode='closest',
            autosize=False,
            dragmode='zoom',
        )

        figure = {'data':[bar_trace], 'layout':layout}

        table = dbc.Table.from_dataframe(df,striped=True,bordered=True,hover=True,size='sm')
        

        if df.shape[0]:
            return [table,figure]
        else:
            return ['No records to display', 'No figure to display']
    else:
        raise PreventUpdate

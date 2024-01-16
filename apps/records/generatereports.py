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


layout = html.Div(
    [
        html.H1("Generate Reports"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Row([
                            dbc.Col(html.H2("Select the Type of Report:"), width=6),
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
                                width=6,
                            ),
                        ]),
                    ]
                ),
                dbc.CardBody(
                    html.Div(id='reportdetails')
                ),
            ]
        )
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
                                dbc.Col(html.H3("Select Time Period"), width=6),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='visitspurpose_timeperiod',
                                        options=[
                                            {'label':'Today', 'value':'today'},
                                            {'label':'This Week (Last 7 Days)', 'value':'thisweek'},
                                            {'label':'This Month', 'value':'thismonth'},
                                            {'label':'Custom', 'value':'custom'},
                                        ],
                                    ),
                                    width=6,
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
    else:
        raise PreventUpdate
    
    return inputs
                    


@app.callback( #callback if customdate
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

@app.callback(
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

        sql = """
        SELECT
            COUNT(*) FILTER (WHERE visit_for_vacc = true) AS vacc_count,
            COUNT(*) FILTER (WHERE visit_for_deworm = true) AS deworm_count,
            COUNT(*) FILTER (WHERE visit_for_problem = true) AS problem_count
        FROM 
            visit
        """
        values = []

        if timeperiod == "today" or timeperiod == "thisweek" or timeperiod == "thismonth" or (timeperiod == "custom" and (startdate and enddate != None)):
            sql += "WHERE (visit_date BETWEEN %s AND %s)"
            values += [f"{start_date}", f"{end_date}"]
            
        cols = ['Vaccine', 'Deworming', 'Problem']

        df = db.querydatafromdatabase(sql, values, cols)

        traces = {}
        for column in df.columns:
            traces[f'tracebar_{column}'] = go.Bar(
                x=[column],
                y=[df.iloc[0][column]],
                name=column
            )
            
        data = list(traces.values())

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

        figure = {'data':data, 'layout':layout}

        table = dbc.Table.from_dataframe(df,striped=True,bordered=True,hover=True,size='sm')
        

        if df.shape[0]:
            return [table,figure]
        else:
            return ['No records to display', 'No figure to display']
    else:
        raise PreventUpdate
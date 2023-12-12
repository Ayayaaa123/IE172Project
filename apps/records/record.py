from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_mantine_components as dmc
from app import app
from apps import dbconnect as db
from datetime import datetime

layout = html.Div(
    [
        html.H1("New Visit"),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.H4("Select Patient"),
                            dcc.Dropdown(
                                id="searchfilter_patientvisit",
                                searchable=True,
                                options=[],
                                value=None,
                                clearable=False,
                            ),
                        ]
                    )
                ),
                html.Div(id="searchlist_patientvisit"),
            ]
        ),
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.H4("Select Veterinarian"),
                            dcc.Dropdown(
                                id="searchfilter_vetvisit",
                                searchable=True,
                                options=[],
                                value=None,
                                clearable=False,
                            ),
                        ]
                    )
                ),
                html.Div(id="searchlist_vetvisit"),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Visit Date"),
                        dmc.DatePicker(
                            id='visit_date',
                            placeholder="Select Visit Date",
                            value=datetime.now().date(),
                            inputFormat='MMM DD, YYYY',
                            dropdownType='modal',
                            ),
                    ],
                ),    
            ]
        ),
        html.Br(),
        dbc.Col(html.H4("Visit Purpose")),
        dcc.Checklist(
            options=[
                {"label": "New Problem", "style":{"flex-grow": 1}, "value": "new_problem"},
                {"label": "Follow up to a Problem", "style":{"flex-grow": 1}, "value": "follow_up"},
                {"label": "Vaccination", "style":{"flex-grow": 1}, "value": "vaccination"},
                {"label": "Deworming", "style":{"flex-grow": 1}, "value": "deworming"},
            ],
            id="visit_purpose",
            inline=True,
            style={"display": "flex", 
                   "justify-content": "space-between", 
                   "fontSize":"1.2rem",
                   "align-items":"center"},
        ),
        html.Div(id="additional-inputs"),
    ]
)

@app.callback(
    Output("additional-inputs", "children"),
    [Input("visit_purpose", "value")],
    [State("visit_purpose", "value")]
)
def update_additional_inputs(_, selected_services):
    if selected_services is None:
        return []
    
    inputs = []
    if 'vaccination' in selected_services:
        inputs.extend([
            html.Br(),
            html.H4("Select Vaccine/s"),
            dcc.Dropdown(
                id="vaccine_list",
                searchable=True,
                options=[],
                value=None,
                multi=True,
                clearable=False,
            ),
        ])
    if 'new_problem' in selected_services:
        inputs.extend([
            html.Br(),
            html.H4("Chief Complaint"),
            dcc.Input(
                id='new-problem-input',
                type='text',
                placeholder='Enter Problem',
                style={'width':'50%'},
            ),
            html.Br(),
        ])
    if 'follow_up' in selected_services:
        inputs.extend([
            html.Br(),
            html.H4("Select Problem"),
            dcc.Dropdown(
                id="problem_list",
                searchable=True,
                options=[],
                value=None,
                clearable=False,
            ),
            html.Br(),
            dcc.Checklist(
                id='follow-up-options',
                options=[
                    {'label': 'Create Progress Notes', 'value': 'progress_notes'},
                    {'label': 'Create Lab Exam Records', 'value': 'lab_exam_records'}
                ],
                style={"fontSize":"1.15rem"},
                value=[]
            )
        ])
    return inputs



# @app.callback(
#     [
#         Output('searchlist_patientvisit', 'children')
#     ],
#     [
#         Input('url', 'pathname'),
#         Input('searchfilter_patientvisit', 'value'),
#     ]
# )
# def moviehome_loadmovielist(pathname, searchterm):
#     if pathname == "/newrecord/visit":
#         sql = """ SELECT
#             FROM
#                 INNER JOIN 
#             WHERE
#         """
#         values = []
        
#     else:
#         raise PreventUpdate
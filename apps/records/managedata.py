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
from dash import ALL
from urllib.parse import urlparse, parse_qs


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H4('List of Vaccines')
                                ]
                            ),
                            dbc.CardBody(
                                [
                                    html.Hr(),
                                    html.Div(  # create section to show list of records
                                        [
                                            html.Div(
                                                dbc.Form(
                                                    dbc.Row(
                                                        [
                                                            dbc.Label("Search", width=2),  # search
                                                            dbc.Col(
                                                                dbc.Input(
                                                                    type='text',
                                                                    id='vaccinelist_filter',
                                                                    placeholder='Vaccine Name'
                                                                ),
                                                                width=5
                                                            ),
                                                        ],
                                                        className='mb-3'  # need to edit this
                                                    )
                                                )
                                            ),
                                            html.Div(
                                                "Table will go here.",
                                                id='managedata_vaccinelist'
                                            ),
                                            html.Div(  # add new vaccine form
                                                [
                                                    dbc.Form(
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("Add Vaccine", width=2),  # search
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        type='text',
                                                                        id='vaccine_add',
                                                                        placeholder='Add Vaccine Name Here'
                                                                    ),
                                                                    width=5
                                                                ),
                                                            ],
                                                            className='mb-3'  # need to edit this
                                                        )
                                                    ),
                                                    dbc.Button(
                                                        "Add",
                                                        color="secondary",
                                                        id='vaccine_addbtn',
                                                        n_clicks=0,  # initialization
                                                        className='custom-submitbutton',
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    width=6  # Adjust the width as needed
                ),  # card for vaccine ends here

                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H4('List of Deworming Medicines')
                                ]
                            ),
                            dbc.CardBody(
                                [
                                    html.Hr(),
                                    html.Div(  # create section to show list of records
                                        [
                                            html.Div(
                                                dbc.Form(
                                                    dbc.Row(
                                                        [
                                                            dbc.Label("Search", width=2),  # search
                                                            dbc.Col(
                                                                dbc.Input(
                                                                    type='text',
                                                                    id='dewormlist_filter',
                                                                    placeholder='Deworming Medicine Name'
                                                                ),
                                                                width=5
                                                            ),
                                                        ],
                                                        className='mb-3'
                                                    )
                                                )
                                            ),
                                            html.Div(
                                                "Table will go here.",
                                                id='managedata_dewormlist'
                                            ),
                                            html.Div(  # add new deworming form
                                                [
                                                    dbc.Form(
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("Add Deworming Medicine", width=3),
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        type='text',
                                                                        id='deworm_add',
                                                                        placeholder='Add Deworming Medicine Name Here'
                                                                    ),
                                                                    width=5
                                                                ),
                                                            ],
                                                            className='mb-3'  # need to edit this
                                                        )
                                                    ),
                                                    dbc.Button(
                                                        "Add",
                                                        color="secondary",
                                                        id='deworm_addbtn',
                                                        n_clicks=0,  # initialization
                                                        className='custom-submitbutton',
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    width=6  # Adjust the width as needed
                )  # end of deworm here
            ]
        )
    ]
)



@app.callback(
    [
        Output('managedata_vaccinelist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('vaccinelist_filter', 'value'),
        Input('vaccine_addbtn', 'n_clicks'),
    ],
    [
        State('vaccine_add', 'value'),
    ]
)
def managedata_vaccinelist(pathname, searchterm, n_clicks, new_vaccine):
    if pathname == '/managedata':
        # Obtain records from DB through SQL
        if n_clicks > 0 and new_vaccine:
            sql = """
                INSERT INTO vacc_m (vacc_m)
                VALUES (%s)
            """
            values = [new_vaccine]
            db.modifydatabase(sql, values)


        sql = """
            SELECT
                vm.vacc_m
            FROM vacc_m vm
            WHERE NOT vm.vacc_m_delete_ind
        """
        values = []
        cols = ['Vaccine Name']


        if searchterm:
            sql += """ AND (
                vm.vacc_m ILIKE %s
                );
                """
            values = [f"%{searchterm}%"]


        df = db.querydatafromdatabase(sql, values, cols)


        df = df[['Vaccine Name']]


        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm',
                                         style={'text-align': 'center'})
        return [table]


    else:
        raise PreventUpdate
    

@app.callback(
    [
        Output('managedata_dewormlist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('dewormlist_filter', 'value'),
        Input('deworm_addbtn', 'n_clicks'),
    ],
    [
        State('deworm_add', 'value'),
    ]
)
def managedata_dewormlist(pathname, searchterm, n_clicks, new_deworm):
    if pathname == '/managedata':
        # Obtain records from DB through SQL
        if n_clicks > 0 and new_deworm:
            sql = """
                INSERT INTO deworm_m (deworm_m)
                VALUES (%s)
            """
            values = [new_deworm]
            db.modifydatabase(sql, values)


        sql = """
            SELECT
                dwm.deworm_m
            FROM deworm_m dwm
            WHERE NOT dwm.deworm_m_delete_ind
        """
        values = []
        cols = ['Deworming Medicine Name']


        if searchterm:
            sql += """ AND (
                dwm.deworm_m ILIKE %s
                );
                """
            values = [f"%{searchterm}%"]


        df = db.querydatafromdatabase(sql, values, cols)


        df = df[['Deworming Medicine Name']]


        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm',
                                         style={'text-align': 'center'})
        return [table]


    else:
        raise PreventUpdate




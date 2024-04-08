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
                                    html.H4('List of Clinical Exam Types')
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
                                                                    id='clinicallist_filter',
                                                                    placeholder='Clinical Exam'
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
                                                id='managedata_clinicallist'
                                            ),
                                            html.Div(  # add new clinical form
                                                [
                                                    dbc.Form(
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("Add Here", width=2),  # search
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        type='text',
                                                                        id='clinical_add',
                                                                        placeholder='Clinical Exam'
                                                                    ),
                                                                    width=5
                                                                ),
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ),
                                                    dbc.Button(
                                                        "Add",
                                                        color="secondary",
                                                        id='clinical_addbtn',
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
                    width=6  
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H4('List of Laboratory Exam Types')
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
                                                                    id='labexamlist_filter',
                                                                    placeholder='Laboratory Exam Type'
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
                                                id='managedata_labexamlist'
                                            ),
                                            html.Div(  # add new labexam form
                                                [
                                                    dbc.Form(
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("Add Here", width=2),  # search
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        type='text',
                                                                        id='labexam_add',
                                                                        placeholder='Laboratory Exam Type'
                                                                    ),
                                                                    width=5
                                                                ),
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ),
                                                    dbc.Button(
                                                        "Add",
                                                        color="secondary",
                                                        id='labexam_addbtn',
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
                    width=6  
                ),
            ]
        ), #clinical and lab row ends here
        html.Div('', style={'margin-bottom': '40px'}),
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
                                                                dbc.Label("Add Here", width=2),  # search
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        type='text',
                                                                        id='vaccine_add',
                                                                        placeholder='Add Vaccine Name Here'
                                                                    ),
                                                                    width=5
                                                                ),
                                                            ],
                                                            className='mb-3'  
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
                    width=6  
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
                                                                dbc.Label("Add Here", width=3),
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        type='text',
                                                                        id='deworm_add',
                                                                        placeholder='Add Deworming Medicine Name Here'
                                                                    ),
                                                                    width=5
                                                                ),
                                                            ],
                                                            className='mb-3'  
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
                    width=6  
                )  # end of deworm here
            ]
        ) # row of vacc and deworm ends here
    ]
)

@app.callback(
    [
        Output('managedata_clinicallist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('clinicallist_filter', 'value'),
        Input('clinical_addbtn', 'n_clicks'),
    ],
    [
        State('clinical_add', 'value'),
    ]
)

def managedata_clinicallist(pathname, searchterm, n_clicks, new_clinical):
    if pathname == '/managedata':
        # Obtain records from DB through SQL
        if n_clicks > 0 and new_clinical:
            sql = """
                INSERT INTO clinical_exam_type (clinical_exam_type_m)
                VALUES (%s)
            """
            values = [new_clinical]
            db.modifydatabase(sql, values)


        sql = """
            SELECT
                clinical_exam_type_m,
                clinical_exam_type_id
            FROM clinical_exam_type
            WHERE NOT clinical_exam_type_delete_ind
        """
        values = []
        cols = ['Clinical Exam Type', 'ID']


        if searchterm:
            sql += """ AND (
                clinical_exam_type_m ILIKE %s
                );
                """
            values = [f"%{searchterm}%"]
        df = db.querydatafromdatabase(sql, values, cols)


        if df.shape:
            buttons = []
            for clinical_exam_type_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editclinicalexam?mode=edit&id={clinical_exam_type_id}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]
            df['Action'] = buttons
            df = df[['Clinical Exam Type', 'Action']]


            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm',
                                            style={'text-align': 'center'})
            return [table]


    else:
        raise PreventUpdate



## LAB EXAM TYPE
@app.callback(
    [
        Output('managedata_labexamlist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('labexamlist_filter', 'value'),
        Input('labexam_addbtn', 'n_clicks'),
    ],
    [
        State('labexam_add', 'value'),
    ]
)

def managedata_labexamlist(pathname, searchterm, n_clicks, new_labexam):
    if pathname == '/managedata':
        # Obtain records from DB through SQL
        if n_clicks > 0 and new_labexam:
            sql = """
                INSERT INTO lab_exam_type (lab_exam_type_m)
                VALUES (%s)
            """
            values = [new_labexam]
            db.modifydatabase(sql, values)


        sql = """
            SELECT
                lab_exam_type_m, 
                lab_exam_type_id
            FROM lab_exam_type
            WHERE NOT lab_exam_type_delete_ind
        """
        values = []
        cols = ['Laboratory Exam Type', 'ID']


        if searchterm:
            sql += """ AND (
                lab_exam_type_m ILIKE %s
                );
                """
            values = [f"%{searchterm}%"]
        df = db.querydatafromdatabase(sql, values, cols)



        if df.shape:
            buttons = []
            for lab_exam_type_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editlabexamtype?mode=edit&id={lab_exam_type_id}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]
            df['Action'] = buttons
            df = df[['Laboratory Exam Type', 'Action']]


        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm',
                                         style={'text-align': 'center'})
        return [table]


    else:
        raise PreventUpdate


# VACCINE LIST

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
                vm.vacc_m,
                vm.vacc_m_id
            FROM vacc_m vm
            WHERE NOT vm.vacc_m_delete_ind
        """
        values = []
        cols = ['Vaccine Name', 'ID']


        if searchterm:
            sql += """ AND (
                vm.vacc_m ILIKE %s
                );
                """
            values = [f"%{searchterm}%"]
        df = db.querydatafromdatabase(sql, values, cols)

        
        if df.shape:
            buttons = []
            for vacc__m_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editvaccinename?mode=edit&id={vacc__m_id}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]
            df['Action'] = buttons
            df = df[['Vaccine Name', 'Action']]


        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm',
                                         style={'text-align': 'center'})
        return [table]


    else:
        raise PreventUpdate
    


# DEWORM LIST

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
                dwm.deworm_m,
                dwm.deworm_m_id
            FROM deworm_m dwm
            WHERE NOT dwm.deworm_m_delete_ind
        """
        values = []
        cols = ['Deworming Medicine Name', 'ID']


        if searchterm:
            sql += """ AND (
                dwm.deworm_m ILIKE %s
                );
                """
            values = [f"%{searchterm}%"]
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for deworm_m_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editdewormtype?mode=edit&id={deworm_m_id}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]
            df['Action'] = buttons
            df = df[['Deworming Medicine Name', 'Action']]

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm',
                                         style={'text-align': 'center'})
        return [table]


    else:
        raise PreventUpdate




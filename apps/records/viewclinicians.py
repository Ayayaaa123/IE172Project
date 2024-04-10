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








layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H4('Clinician Records')
                    ]
                ),
                dbc.CardBody(
                    [
                        html.Div( #add new user button
                            [
                                dbc.Button(
                                    "Add New Clinician Profile",
                                    color="secondary",
                                    href='/managedata/newclinicians'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div( # create section to show list of records
                            [
                                html.Div(
                                dbc.Form(
                                    dbc.Row(
                                        [
                                            dbc.Label("Search", width=1), #search
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id='clinicianlist_filter',
                                                    placeholder='Clinician Name'
                                                ),
                                                width=5
                                            ),
                                        ],
                                        className = 'mb-3' #need to edit this
                                    )
                                )
                                ),
                                html.Div(
                                    "Table goes here.",
                                    id='view_clinicianlist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)








@app.callback(
        [
            Output('view_clinicianlist', 'children'),
        ],
        [
            Input('url', 'pathname'),
            Input('clinicianlist_filter', 'value'),
        ]
)
def view_clinicianlist(pathname, searchterm):
    if pathname == '/managedata/existingclinicians':
        # Obtain records from DB through SQL
        sql = """
        SELECT
                COALESCE(clinician_ln, '') || ', ' || COALESCE(clinician_suffix, '') || ' ' || COALESCE(clinician_fn, '') || ' ' || COALESCE(clinician_mi, '') AS clinician_name,
                clinician_email,
                clinician_id
            FROM clinician
            WHERE NOT clinician_delete_ind
        """
        values = []
        cols = ['Clinician Name', 'Email', 'ID']




        if searchterm:
            sql += """ AND (
                clinician_ln ILIKE %s
                OR clinician_fn ILIKE %s
                )
            """
            values.extend([f"%{searchterm}%", f"%{searchterm}%"])
        
        sql += " ORDER BY clinician_id;"




        df = db.querydatafromdatabase(sql, values, cols)




        if df.shape:
            buttons = []
            for clinician_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editclinician?mode=edit&id={clinician_id}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]
            df['Action'] = buttons
            df = df[['Clinician Name', 'Email', 'Action']]




            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})




            return [table]
    else:
        raise PreventUpdate

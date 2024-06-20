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
                        html.H4('Veterinarian Records')
                    ]
                ),
                dbc.CardBody(
                    [
                        html.Div( #add new user button
                            [
                                dbc.Button(
                                    "Add New User Profile",
                                    color="secondary",
                                    href='/newuser'
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
                                                    id='userlist_filter',
                                                    placeholder='Vet Name'
                                                ),
                                                width=5
                                            ),
                                        ],
                                        className = 'mb-3' #need to edit this
                                    )
                                )
                                ),
                                html.Div(
                                    "Table with vets go here.",
                                    id='viewrecord_vetlist'
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
        Output('viewrecord_vetlist', 'children'),
        #Output('viewrecord_visitlist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('userlist_filter', 'value'),
        #Input('recordlist_filter','value'),
    ]
)


def viewrecord_vetlist(pathname, searchterm):
    if pathname == '/viewuser':
        # Obtain records from DB through SQL
       
        #edit vet email to username 
        sql = """
            SELECT
                COALESCE(vet_ln, '') || ', ' || COALESCE (vet_fn, '') || ' ' || COALESCE (vet_mi, '') AS vet_name,
                vet_email, 
                vet_id
            FROM vet
            WHERE NOT vet_delete_ind
        """
        values = []
        #cols = ['Patient ID', 'Patient Name']
        cols = ['Veterinarian Name', 'Username', 'ID']
       
        if searchterm:
            sql += """ AND (
                vet_ln ILIKE %s
                OR vet_fn ILIKE %s
                )
            """
            values.extend([f"%{searchterm}%", f"%{searchterm}%"])

        sql += " ORDER BY vet_id;"
       
        df = db.querydatafromdatabase(sql, values, cols)
       
        if df.shape:
            buttons = []
            for vet_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/edituser?mode=edit&id={vet_id}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]


            df['Action'] = buttons
            df = df[['Veterinarian Name', 'Username', 'Action']]


            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]


    else:
        raise PreventUpdate
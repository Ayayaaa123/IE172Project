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
                        html.H4('Patient Records')
                    ]
                ),
                dbc.CardBody(
                    [
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
                                                    id='recordlist_filter',
                                                    placeholder='Client/Patient Name'
                                                ),
                                                width=5
                                            ),
                                            # dbc.Label("Show", width=1), #dropdown
                                            # dbc.Col(
                                            #     dbc.Input(
                                            #         type='text',
                                            #         id='recordlist_filter',
                                            #         placeholder='Client Name'
                                            #     ),
                                            #     width=5
                                            # )
                                        ],
                                        className = 'mb-3' #need to edit this
                                    )
                                )
                                ),
                                html.Div(
                                    "Table with patients will go here.",
                                    id='viewrecord_patientlist'
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
        Output('viewrecord_patientlist', 'children'),
        #Output('viewrecord_visitlist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('recordlist_filter', 'value'),
        #Input('recordlist_filter','value'),
    ]
)

def viewrecord_loadpatientlist(pathname, searchterm):
    if pathname == '/viewrecord':
        # Obtain records from DB through SQL
        # What information do we need to see
        sql = """
            SELECT 
                patient_m,
                COALESCE(client_ln, '') || ', ' || COALESCE (client_fn, '') || ' ' || COALESCE (client_mi, '') AS client_name,
                client_cn,
                patient_id
            FROM patient p
                INNER JOIN client c on p.client_id = c.client_id
            WHERE NOT patient_delete_ind
        """
        values = []
        #cols = ['Patient ID', 'Patient Name']
        cols = ['Patient Name', 'Client Name', 'Contact Number', 'ID']
        
        if searchterm:
            sql += """ AND (
                patient_m ILIKE %s 
                OR client_ln ILIKE %s 
                OR client_fn ILIKE %s
                )
            """
            values.extend([f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"])
        
        sql += " ORDER BY patient_id;"

        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape:
            buttons = []
            for patient_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editrecord?mode=edit&id={patient_id}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Patient Name', 'Client Name', 'Contact Number', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate

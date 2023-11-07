import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Owner Information"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3("Contact Person")
                    ]
                ),
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Label("Last Name"),
                                dbc.Col(
                                    dbc.Input(id='owner_ln', type='text', placeholder='Enter Last Name')  
                                ),
                                dbc.Label("First Name"),
                                dbc.Col(
                                    dbc.Input(id='owner_fn', type='text', placeholder='Enter First Name')
                                ),
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)
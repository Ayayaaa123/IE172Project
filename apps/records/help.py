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
from datetime import datetime, timedelta


layout = html.Div(
    [
        html.H1("Help"),
        html.Hr(),
        html.H3("Access the User Manual at this link:"),
        html.H3(html.A("http://tinyurl.com/VetMedUserManual", href="http://tinyurl.com/VetMedUserManual", target="blank")),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H3("For any concerns, please contact the developers at:"),
        html.H3("Sabino B. Cangas - sbcangas@up.edu.ph"),
        html.H3("Kathleen Mae Q. Basa - kqbasa@up.edu.ph"),
        html.H3("Ma. Colline G. Foralan - mgforalan@up.edu.ph"),
        html.H3("Paul Kristian M. Telan - pmtelan@up.edu.ph")
    ]
)

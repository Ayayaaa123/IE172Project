import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import webbrowser
from app import app

navlink_style = {
    'color': '#fff'
}

navbar = dbc.Navbar(
    [
        dbc.NavLink("Owner Information", href="/newrecord/owner", active="exact", className="active-link", style=navlink_style),
        dbc.NavLink("Patient Information", href="/newrecord/patient", active="exact", className="active-link", style=navlink_style),
        dbc.NavLink("Patient Visit Details", href="/newrecord/visit", active="exact", className="active-link", style=navlink_style),
    ],
    dark=True,
    color='dark',
    style={'margin-left':'16rem'}
)
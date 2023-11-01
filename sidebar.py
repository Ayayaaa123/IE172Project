import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import webbrowser
from app import app

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#333",
}

upvetmed_style = {
    "font-size": "2rem",
    "text-align": "center",
    "text-decoration": "underline",
    "color": "#fff",
    "margin-top": "-20px",
}

mainelement_style = {
    "font-size": "1.5rem",
    "color": "#fff",
    "margin-bottom": "0",
}

subelement_style = {
    "font-size": "1rem",
    "margin-left": "1.5em",
    "color": "#fff",
    "margin-bottom": "0",
}

sidebar = dbc.Nav(
    [
        dbc.NavLink("UP VETMED", href="/home", style=upvetmed_style),
        dbc.NavLink("Patient Records", href="/records", active="exact", style=mainelement_style),
        html.Hr(style={"border-bottom":"2px solid white", "margin-top":"0", "margin-bottom":"0"}),
        dbc.Nav(
            [
                dbc.NavLink("New Record", href="/records/new", active="exact", style=subelement_style),
                html.Hr(style={"border-bottom":"1px solid white", "margin-top":"0", "margin-bottom":"0"}),
                dbc.NavLink("View Records", href="/records/view", active="exact", style=subelement_style),
                html.Hr(style={"border-bottom":"1px solid white", "margin-top":"0", "margin-bottom":"0"}),
            ],
        ),
        dbc.NavLink("User Management", href="/user", active="exact", style=mainelement_style),
        html.Hr(style={"border-bottom":"2px solid white", "margin-top":"0", "margin-bottom":"0"}),
        dbc.Nav(
            [
                dbc.NavLink("New User", href="/user/new", active="exact", style=subelement_style),
                html.Hr(style={"border-bottom":"1px solid white", "margin-top":"0", "margin-bottom":"0"}),
                dbc.NavLink("View Users", href="/user/view", active="exact", style=subelement_style),
                html.Hr(style={"border-bottom":"1px solid white", "margin-top":"0", "margin-bottom":"0"}),
            ]
        ),
        dbc.NavLink("Reports", href="/reports", active="exact", style=mainelement_style),
        html.Hr(style={"border-bottom":"2px solid white", "margin-top":"0", "margin-bottom":"0"}),
        dbc.Nav(
            [
                dbc.NavLink("Generate Report", href="/reports/generate", active="exact", style=subelement_style),
                html.Hr(style={"border-bottom":"1px solid white", "margin-top":"0", "margin-bottom":"0"}),
                dbc.NavLink("View Generated Reports", href="/reports/view", active="exact", style=subelement_style),
                html.Hr(style={"border-bottom":"1px solid white", "margin-top":"0", "margin-bottom":"0"}),
            ]
        ),
        dbc.NavLink("Help", href="/help", active="exact", style=mainelement_style),
        html.Hr(style={"border-bottom":"2px solid white", "margin-top":"0", "margin-bottom":"0"}),
    ],
    vertical=True,
    pills=True,
    style=SIDEBAR_STYLE
)
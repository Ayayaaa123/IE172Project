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
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#333",
}

mainelement_style = {
    "font-size": "1.5rem",
    "color": "#fff",
    "margin-bottom": "0",
}

subelement_style = {
    "font-size": "0.93rem",
    "margin-left": "1em",
    "color": "#fff",
    "margin-bottom": "0",
}

line_style = {
    "border-bottom":"2px solid white", 
    "margin-top":"0", 
    "margin-bottom":"0",
}


sidebar = dbc.Nav(
    [      
        dbc.NavLink(html.Img(src="assets/logo.webp", height="100px"), href="/home", active="exact", className=subelement_style),
        html.Br(),
        
        dbc.Nav(
            [
                dbc.NavLink("Home Page", href="/home", active="exact", className="active-link", style=subelement_style),
            ],
        ),
        html.H2("Patient Records", className="h2-normal", style=mainelement_style),
        html.Hr(style=line_style),
        dbc. Accordion(
            [
                dbc.AccordionItem( #indent needs to be fixed or uncomment ln 10889 in bootstrap.css
                    [
                        dbc.NavLink("New Patient", href="/newrecord/newpatient", active="exact", className="active-link", style=subelement_style),
                        dbc.NavLink("Existing Patient", href="/newrecord/existingpatient", active="exact", className="active-link", style=subelement_style),
                    ],
                    #title="Add New Record", 
                    id="add-new-link",
                ),
                
        #         dbc.AccordionItem(
        #             [
        #                 dbc.NavLink("Patient Records", href="/viewrecord/patient", active="exact", className="active-link", style=subelement_style),
        #                 dbc.NavLink("Visit Records", href="/viewrecord/visit", active="exact", className="active-link", style=subelement_style),
        #             ],
        #             title="View Records", 
        #             id="add-new-link",
        #         ),
            ],
            className="custom-accordion",
            start_collapsed=True,
        ), 
        
        dbc.Nav(
            [
                dbc.NavLink("View Records", href="/viewrecord", active="exact", className="active-link", style=subelement_style),
            ],
        ),
        html.Br(),
        
        html.H2("User Management", className="h2-normal", style=mainelement_style),
        html.Hr(style=line_style),
        dbc.Nav(
            [
                dbc.NavLink("New User", href="/newuser", active="exact", className="active-link", style=subelement_style),
                dbc.NavLink("View Users", href="/viewuser", active="exact", className="active-link", style=subelement_style),
                dbc.NavLink("Manage Data", href="/managedata", active="exact", className="active-link", style=subelement_style),
            ]
        ),
        html.Br(),
        
        html.H2("Reports", className="h2-normal", style=mainelement_style),
        html.Hr(style=line_style),
        dbc.Nav(
            [
                dbc.NavLink("Generate Report", href="/newreport", active="exact", className="active-link", style=subelement_style),
                dbc.NavLink("View Generated Reports", href="/viewreport", active="exact", className="active-link", style=subelement_style),
            ]
        ),
        html.Br(),
        
        dbc.NavLink("Help", href="/help", active="exact", className="active-link", style=mainelement_style),

        dbc.NavLink("Logout", href = "/logout", active="exact", className="active-link", style=mainelement_style), 
    ],
    vertical=True,
    pills=True,
    style=SIDEBAR_STYLE
)
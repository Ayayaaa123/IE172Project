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
from dash import ALL, MATCH
from urllib.parse import urlparse, parse_qs


layout = html.Div(
    [
        dbc.Alert(id='adddeworm_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="adddeworm_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H2("Deworming Details"),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Deworming Medication"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="adddeworm_namelist",
                        placeholder='Select Deworming Medicine',
                        searchable=True,
                        options=[],
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Deworming Dosage"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="adddeworm_dose",
                        placeholder='Select Dosage',
                        searchable=True,
                        options=[
                            {'label':'1st', 'value':'1st'},
                            {'label':'2nd', 'value':'2nd'},
                            {'label':'3rd', 'value':'3rd'},
                            {'label':'4th', 'value':'4th'},
                            {'label':'Booster', 'value':'booster'},
                        ],
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Date Administered"), width=3),
                dbc.Col(
                    dmc.DatePicker(
                        id="adddeworm_dateadministered",
                        placeholder="Select Date Administered",
                        inputFormat='MMM DD, YYYY',
                        dropdownType='modal',
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Expiration Date"), width=3),
                dbc.Col(
                    dmc.DatePicker(
                        id="adddeworm_expdate",
                        placeholder="Select Expiration Date",
                        inputFormat='MMM DD, YYYY',
                        dropdownType='modal',
                    ),
                    width=6,
                ),
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Deworming From VetMed?"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="adddeworm_fromvetmed",
                        searchable=True,
                        options=[
                            {"label": "Yes", "value": True},
                            {"label": "No", "value": False},
                        ]
                    ),
                    width=6,
                ),
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
        ]),
        html.Br(),
        dbc.Button(
            'Save',
            id = 'adddeworm_save',
            n_clicks = 0,
            className='custom-submitbutton',
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H3('Save Success')),
            dbc.ModalFooter(
                dbc.Button(
                    "Return",
                    href="",
                    id="adddeworm_return-button",
                )
            )
        ],
        centered = True, 
        id = 'adddeworm_successmodal',
        backdrop = 'static'
        )
    ]
)


@app.callback(  
    Output("adddeworm_namelist", "options"),
    Output('adddeworm_return-link', 'href'),
    Input('url','search'),
)
def adddeworm_initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    return_link= ""

    if 'patient_id' in query_ids:
        patient_id = query_ids.get('patient_id', [None])[0]
        sql = """
            SELECT 
                deworm_m_id,
                deworm_m
            FROM 
                deworm_m 
            WHERE 
                NOT deworm_m_delete_ind
        """
        values = []
        cols = ['deworm_id', 'deworm_m']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['deworm_m'], 'value': row['deworm_id']} for _, row in result.iterrows()]

        return_link = f'/home_visit/purpose?mode=add&patient_id={patient_id}'

        return (options, return_link)
    else:
        raise PreventUpdate
    

@app.callback(
    Output('adddeworm_alert','color'),
    Output('adddeworm_alert','children'),
    Output('adddeworm_alert','is_open'),
    Output('adddeworm_successmodal', 'is_open'),
    Output('adddeworm_return-button', 'href'),
    Input('adddeworm_save', 'n_clicks'),
    Input('url','search'),
    Input('adddeworm_namelist','value'),
    Input('adddeworm_dose','value'),
    Input('adddeworm_dateadministered','value'),
    Input('adddeworm_expdate','value'),
    Input('adddeworm_fromvetmed','value'),
)
def save_adddeworm_record(submitbtn, url_search, deworm_name, deworm_dose, deworm_dateadministered, deworm_expdate, deworm_fromvetmed):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'adddeworm_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            return_link = ''

            patient_id = query_ids.get('patient_id', [None])[0]  

            if not deworm_name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select deworming medicine name'
            elif not deworm_dose:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select deworming dosage'
            elif not deworm_dateadministered:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select date administered'
            elif not deworm_expdate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select expiration date'
            elif deworm_fromvetmed is None:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select if vaccine is from vetmed'
            else:
                sql = """
                    SELECT MAX(visit_id)
                    FROM visit
                    """
                values = []
                df = db.querydatafromdatabase(sql,values)
                visit_id = int(df.loc[0,0])

                sql = """
                    SELECT MAX(deworm_no)
                    FROM deworm
                    INNER JOIN visit ON deworm.visit_id = visit.visit_id
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                    WHERE patient.patient_id = %s
                    """
                values = [patient_id]
                df = db.querydatafromdatabase(sql,values)
                deworm_no_before = int(df.loc[0,0]) if not pd.isna(df.loc[0,0]) else 0
                deworm_no_new = deworm_no_before + 1
                
                sql = """
                    INSERT INTO deworm(
                        deworm_no,
                        deworm_m_id,
                        deworm_dose,
                        deworm_administered,
                        deworm_exp,
                        deworm_from_vetmed,
                        deworm_delete_ind,
                        visit_id
                    )
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [deworm_no_new, deworm_name, deworm_dose, deworm_dateadministered, deworm_expdate, deworm_fromvetmed, False, visit_id]
                db.modifydatabase(sql, values)

                modal_open = True

                return_link = f'/home_visit/purpose?mode=add&patient_id={patient_id}'
                
            return [alert_color, alert_text, alert_open, modal_open, return_link]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
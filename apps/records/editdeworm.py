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
        dbc.Alert(id='deworm_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="deworm_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H2("Deworming Details"),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Deworming Medication"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="deworm_namelist",
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
                        id="deworm_dose",
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
                        id="deworm_dateadministered",
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
                        id="deworm_expdate",
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
                        id="deworm_fromvetmed",
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
            dbc.Row([
                dbc.Col(html.H4("Delete Record?"), width=3),
                dbc.Col(
                    dbc.Checklist(
                        id='deworm_delete',
                        options=[
                            {
                                'label': "Mark for Deletion",
                                'value': 1
                            }
                        ],
                        style={'fontWeight': 'bold'},
                    ),
                    width=6,
                ),
            ]),
        ]),
        html.Br(),
        dbc.Button(
            'Save',
            id = 'deworm_save',
            n_clicks = 0,
            className='custom-submitbutton',
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H3('Save Success')),
            dbc.ModalFooter(
                dbc.Button(
                    "Return",
                    href="",
                    id="deworm_return-button",
                )
            )
        ],
        centered = True, 
        id = 'deworm_successmodal',
        backdrop = 'static'
        )
    ]
)


@app.callback(  
    Output("deworm_namelist", "options"),
    Output('deworm_namelist','value'),
    Output('deworm_dose','value'),
    Output('deworm_dateadministered','value'),
    Output('deworm_expdate','value'),
    Output('deworm_fromvetmed','value'),
    Output('deworm_return-link', 'href'),
    Input('url','search'),
)
def initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    patient_link= ""

    if 'deworm_id' in query_ids and 'patient_id' in query_ids:
        deworm_id = query_ids.get('deworm_id', [None])[0]
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

        sql = """
            SELECT deworm.deworm_m_id, deworm_dose, deworm_administered, deworm_exp, deworm_from_vetmed
            FROM deworm
            INNER JOIN deworm_m ON deworm.deworm_m_id = deworm_m.deworm_m_id
            INNER JOIN visit ON deworm.visit_id = visit.visit_id
            INNER JOIN patient ON visit.patient_id = patient.patient_id
            WHERE deworm_id = %s AND patient.patient_id = %s
        """
        values = [deworm_id, patient_id]
        col = ['deworm_m_id', 'deworm_dose', 'deworm_administered', 'deworm_exp', 'deworm_from_vetmed']
        df = db.querydatafromdatabase(sql, values, col)

        deworm_name = df['deworm_m_id'][0]
        deworm_dose = df['deworm_dose'][0]
        deworm_dateadministered = df['deworm_administered'][0]
        deworm_expdate = df['deworm_exp'][0]
        deworm_fromvetmed = df['deworm_from_vetmed'][0]

        patient_link = f'/editrecord?mode=edit&id={patient_id}'

        return (options, deworm_name, deworm_dose, deworm_dateadministered, deworm_expdate, deworm_fromvetmed, patient_link)
    else:
        raise PreventUpdate
    

@app.callback(
    Output('deworm_alert','color'),
    Output('deworm_alert','children'),
    Output('deworm_alert','is_open'),
    Output('deworm_successmodal', 'is_open'),
    Output('deworm_return-button', 'href'),
    Input('deworm_save', 'n_clicks'),
    Input('url','search'),
    Input('deworm_namelist','value'),
    Input('deworm_dose','value'),
    Input('deworm_dateadministered','value'),
    Input('deworm_expdate','value'),
    Input('deworm_fromvetmed','value'),
    Input('deworm_delete','value'),
)
def save_deworm_record(submitbtn, url_search, deworm_name, deworm_dose, deworm_dateadministered, deworm_expdate, deworm_fromvetmed, deworm_delete):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'deworm_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            patient_link = ''

            deworm_id = query_ids.get('deworm_id', [None])[0]
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
            elif deworm_delete is None:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select if vaccine should be deleted'
            else:
                to_delete = bool(deworm_delete)
                sql = """
                    UPDATE deworm
                    SET 
                        deworm_m_id = %s,
                        deworm_dose = %s,
                        deworm_administered = %s,
                        deworm_exp = %s,
                        deworm_from_vetmed = %s,
                        deworm_delete_ind = %s
                    FROM visit
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                    WHERE deworm_id = %s AND patient.patient_id = %s
                """
                values = [deworm_name, deworm_dose, deworm_dateadministered, deworm_expdate, deworm_fromvetmed, to_delete, deworm_id, patient_id]
                db.modifydatabase(sql, values)

                modal_open = True

                patient_link = f'/editrecord?mode=edit&id={patient_id}'

            return [alert_color, alert_text, alert_open, modal_open, patient_link]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
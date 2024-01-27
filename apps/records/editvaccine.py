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
        dbc.Alert(id='vaccine_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="vaccine_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H2("Vaccine Details"),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Vaccine Medication"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="vaccine_namelist",
                        placeholder='Select Vaccine',
                        searchable=True,
                        options=[],
                    ),
                    width=6,
                )
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Vaccine Dosage"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="vaccine_dose",
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
                        id="vaccine_dateadministered",
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
                        id="vaccine_expdate",
                        placeholder="Select Expiration Date",
                        inputFormat='MMM DD, YYYY',
                        dropdownType='modal',
                    ),
                    width=6,
                ),
            ]),
            html.Div(style={'margin-bottom':'1rem'}),
            dbc.Row([
                dbc.Col(html.H4("Vaccine From VetMed?"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="vacc_fromvetmed",
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
                    dcc.Dropdown(
                        id="vacc_delete",
                        searchable=True,
                        options=[
                            {"label": "Yes", "value": True},
                            {"label": "No", "value": False},
                        ]
                    ),
                    width=6,
                ),
            ]),
        ]),
        html.Br(),
        dbc.Button(
            'Save',
            id = 'vaccine_save',
            n_clicks = 0,
            className='custom-submitbutton',
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H3('Save Success')),
            dbc.ModalFooter(
                dbc.Button(
                    "Return",
                    href="",
                    id="vaccine_return-button",
                )
            )
        ],
        centered = True, 
        id = 'vaccine_successmodal',
        backdrop = 'static'
        )
    ]
)


@app.callback(  
    Output("vaccine_namelist", "options"),
    Output('vaccine_namelist','value'),
    Output('vaccine_dose','value'),
    Output('vaccine_dateadministered','value'),
    Output('vaccine_expdate','value'),
    Output('vacc_fromvetmed','value'),
    Output('vacc_delete','value'),
    Output('vaccine_return-link', 'href'),
    Input('url','search'),
)
def initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    patient_link= ""

    if 'vacc_id' in query_ids and 'patient_id' in query_ids:
        vaccine_id = query_ids.get('vacc_id', [None])[0]
        patient_id = query_ids.get('patient_id', [None])[0]
        sql = """
            SELECT 
                vacc_m_id,
                vacc_m
            FROM 
                vacc_m 
            WHERE 
                NOT vacc_m_delete_ind
        """
        values = []
        cols = ['vacc_id', 'vacc_m']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['vacc_m'], 'value': row['vacc_id']} for _, row in result.iterrows()]

        sql = """
            SELECT vacc.vacc_m_id, vacc_dose, vacc_date_administered, vacc_exp, vacc_from_vetmed, vacc_delete_ind
            FROM vacc
            INNER JOIN vacc_m ON vacc.vacc_m_id = vacc_m.vacc_m_id
            INNER JOIN visit ON vacc.visit_id = visit.visit_id
            INNER JOIN patient ON visit.patient_id = patient.patient_id
            WHERE vacc_id = %s AND patient.patient_id = %s
        """
        values = [vaccine_id, patient_id]
        col = ['vacc_m_id', 'vacc_dose', 'vacc_date_administered', 'vacc_exp', 'vacc_from_vetmed', 'vacc_delete_ind']
        df = db.querydatafromdatabase(sql, values, col)

        vaccine_name = df['vacc_m_id'][0]
        vaccine_dose = df['vacc_dose'][0]
        vaccine_dateadministered = df['vacc_date_administered'][0]
        vaccine_expdate = df['vacc_exp'][0]
        vaccine_fromvetmed = df['vacc_from_vetmed'][0]
        vaccine_delete = df['vacc_delete_ind'][0]

        patient_link = f'/editrecord?mode=edit&id={patient_id}'

        return (options, vaccine_name, vaccine_dose, vaccine_dateadministered, vaccine_expdate, vaccine_fromvetmed, vaccine_delete, patient_link)
    else:
        raise PreventUpdate
    

@app.callback(
    Output('vaccine_alert','color'),
    Output('vaccine_alert','children'),
    Output('vaccine_alert','is_open'),
    Output('vaccine_successmodal', 'is_open'),
    Output('vaccine_return-button', 'href'),
    Input('vaccine_save', 'n_clicks'),
    Input('url','search'),
    Input('vaccine_namelist','value'),
    Input('vaccine_dose','value'),
    Input('vaccine_dateadministered','value'),
    Input('vaccine_expdate','value'),
    Input('vacc_fromvetmed','value'),
    Input('vacc_delete','value'),
)
def save_vacc_record(submitbtn, url_search, vaccine_name, vaccine_dose, vaccine_dateadministered, vaccine_expdate, vacc_fromvetmed, vacc_delete):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'vaccine_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            patient_link = ''

            vaccine_id = query_ids.get('vacc_id', [None])[0]
            patient_id = query_ids.get('patient_id', [None])[0]    

            if not vaccine_name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select vaccine name'
            elif not vaccine_dose:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select vaccine dosage'
            elif not vaccine_dateadministered:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select date administered'
            elif not vaccine_expdate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select expiration date'
            elif vacc_fromvetmed is None:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select if vaccine is from vetmed'
            elif vacc_delete is None:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select if vaccine should be deleted'
            else:
                sql = """
                    UPDATE vacc
                    SET 
                        vacc_m_id = %s,
                        vacc_dose = %s,
                        vacc_date_administered = %s,
                        vacc_exp = %s,
                        vacc_from_vetmed = %s,
                        vacc_delete_ind = %s
                    FROM visit
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                    WHERE vacc_id = %s AND patient.patient_id = %s
                """
                values = [vaccine_name, vaccine_dose, vaccine_dateadministered, vaccine_expdate, vacc_fromvetmed, vacc_delete, vaccine_id, patient_id]
                db.modifydatabase(sql, values)

                modal_open = True

                patient_link = f'/editrecord?mode=edit&id={patient_id}'

            return [alert_color, alert_text, alert_open, modal_open, patient_link]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
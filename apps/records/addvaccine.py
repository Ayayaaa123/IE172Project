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
        dbc.Alert(id='addvaccine_alert', is_open = False),
        dbc.Nav(dbc.NavItem(dbc.NavLink("<  Return", active=True, href="", id="addvaccine_return-link", style={"font-size": "1.25rem", 'margin-left':0, 'font-weight': 'bold'}))),
        html.Div(style={'margin-bottom':'1rem'}),
        html.H2("Vaccine Details"),
        html.Hr(),
        dbc.Form([
            dbc.Row([
                dbc.Col(html.H4("Vaccine Medication"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="addvaccine_namelist",
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
                        id="addvaccine_dose",
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
                        id="addvaccine_dateadministered",
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
                        id="addvaccine_expdate",
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
                        id="addvacc_fromvetmed",
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
            id = 'addvaccine_save',
            n_clicks = 0,
            className='custom-submitbutton',
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H3('Save Success')),
            dbc.ModalFooter(
                dbc.Button(
                    "Return",
                    style={"backgroundColor": "#333", "borderColor": "#333" , "color": "white"}, 
                    href="",
                    id="addvaccine_return-button",
                )
            )
        ],
        centered = True, 
        id = 'addvaccine_successmodal',
        backdrop = 'static'
        )
    ]
)


@app.callback(  
    Output("addvaccine_namelist", "options"),
    Output('addvaccine_return-link', 'href'),
    Input('url','search'),
)
def addvaccine_initial_values(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    return_link= ""

    if 'patient_id' in query_ids:
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

        return_link = f'/home_visit/purpose?mode=add&patient_id={patient_id}'

        return (options, return_link)
    else:
        raise PreventUpdate
    

@app.callback(
    Output('addvaccine_alert','color'),
    Output('addvaccine_alert','children'),
    Output('addvaccine_alert','is_open'),
    Output('addvaccine_successmodal', 'is_open'),
    Output('addvaccine_return-button', 'href'),
    Input('addvaccine_save', 'n_clicks'),
    Input('url','search'),
    Input('addvaccine_namelist','value'),
    Input('addvaccine_dose','value'),
    Input('addvaccine_dateadministered','value'),
    Input('addvaccine_expdate','value'),
    Input('addvacc_fromvetmed','value'),
)
def save_addvacc_record(submitbtn, url_search, vaccine_name, vaccine_dose, vaccine_dateadministered, vaccine_expdate, vacc_fromvetmed):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'addvaccine_save' and submitbtn:
            parsed = urlparse(url_search)
            query_ids = parse_qs(parsed.query)  

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            return_link = ''

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
            else:
                sql = """
                    SELECT MAX(visit_id)
                    FROM visit
                    """
                values = []
                df = db.querydatafromdatabase(sql,values)
                visit_id = int(df.loc[0,0])

                sql = """
                    SELECT MAX(vacc_no)
                    FROM vacc
                    INNER JOIN visit ON vacc.visit_id = visit.visit_id
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                    WHERE patient.patient_id = %s
                    """
                values = [patient_id]
                df = db.querydatafromdatabase(sql,values)
                vacc_no_before = int(df.loc[0,0]) if not pd.isna(df.loc[0,0]) else 0
                vacc_no_new = vacc_no_before + 1
                
                sql = """
                    INSERT INTO vacc(
                        vacc_no,
                        vacc_m_id,
                        vacc_dose,
                        vacc_date_administered,
                        vacc_exp,
                        vacc_from_vetmed,
                        vacc_delete_ind,
                        visit_id
                    )
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [vacc_no_new, vaccine_name, vaccine_dose, vaccine_dateadministered, vaccine_expdate, vacc_fromvetmed, False, visit_id]
                db.modifydatabase(sql, values)

                modal_open = True

                return_link = f'/home_visit/purpose?mode=add&patient_id={patient_id}'

            return [alert_color, alert_text, alert_open, modal_open, return_link]
        
        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
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
        html.H1("Edit User Profile"),
        html.Hr(),
        dbc.Alert(id='edituserprofile_alert', is_open=False), # For feedback purposes
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Personal Information")
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Last Name"),
                                        dbc.Input(id='vet_ln', type='text', placeholder='Enter Last Name', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("First Name"),
                                        dbc.Input(id='vet_fn', type='text', placeholder='Enter First Name', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Middle Initial"),
                                        dbc.Input(id='vet_mi', type='text', placeholder='Enter Middle Initial', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Suffix (N/A if none)"),
                                        dbc.Input(id='vet_suffix', type='text', placeholder='Enter Suffix', style={'width':'80%'})
                                       
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ), # end of row for owner name
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        # dbc.InputGroupText("@"), dbc.Input(placeholder='Enter Username')
                                        dbc.Label("Email/Username"),
                                        dbc.Input(id='vet_email', type='text', placeholder='Enter Email Address', style={'width':'80%'}),
                                        # dbc.FormText(
                                        #     "example@gmail.com",
                                        #     color = "secondary",
                                        # )
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Contact Number"),
                                        dbc.Input(id='vet_cn', type='text', placeholder='Enter Contact Number', style={'width':'80%'})
                                    ],
                                    width=3
                                ),
                            ],
                            className="mb-3",
                        ),  # end of row
                    ],
                )
            ],
            style={'width':'100%'}
        ), # end
       
        html.Br(),
        # dbc.Card(
        #     [
        #         dbc.CardHeader(
        #             [
        #                 html.H2("Account Information")
        #             ]
        #         ),
        #         dbc.CardBody(
        #             [
        #                 dbc.Row(
        #                     [
        #                         dbc.Col(
        #                             [
        #                                 dbc.Label("Username"),
        #                                 dbc.Input(id='vet_user_name', type='text', placeholder='Create Account Username', style={'width':'75%'})
        #                             ],
        #                             width=3
        #                         ),
        #                     ],
        #                     className="mb-3",
        #                 ),
        #                 dbc.Row(
        #                     [
        #                         dbc.Col(
        #                             [
        #                                 dbc.Label("Create Password"),
        #                                 dbc.Input(id='vet_user_password', type='password', placeholder='Enter Password', style={'width':'75%'})
        #                             ],
        #                             width=3
        #                         ),
        #                     ],
        #                     className = "mb-3",
        #                 ),
        #                 dbc.Row(
        #                     [
        #                         dbc.Col(
        #                             [
        #                                 dbc.Label("Confirm Password"),
        #                                 dbc.Input(id='vet_user_confirm_password', type='password', placeholder='Re-Enter Password', style={'width':'75%'})
        #                             ],
        #                             width=3
        #                         ),
        #                     ],
        #                     className = "mb-3",
        #                 ),
        #             ]
        #         )
        #     ]
       
        # ),
        html.Br(),
        dbc.Button(
            'Save',
            id = 'edituser_savebtn',
            n_clicks = 0, #initialization
            className='custom-submitbutton',
        ),
        dbc.Modal( # dialog box for successful saving of profile
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    'Your profile has been updated',
                    id = 'edituserprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay",
                        href = '/viewuser', # bring user back to table
                        id = 'edituserprofile_btn_modal',
                    )                    
                )
            ],
            centered=True,
            id='edituserprofile_successmodal',
            backdrop='static' # dialog box does not go away if you click at the background


        )
    ]
)






# CALLBACK TO SAVE CHANGES
@app.callback(
    [
        Output('edituserprofile_alert', 'color'),
        Output('edituserprofile_alert', 'children'),
        Output('edituserprofile_alert', 'is_open'),


        Output('edituserprofile_successmodal', 'is_open'),
        Output('edituserprofile_feedback_message', 'children'),
        Output('edituserprofile_btn_modal', 'href'),
    ],
   
    [
        Input('edituser_savebtn', 'n_clicks'),
        Input('edituserprofile_btn_modal', 'n_clicks')

    ],

    [
        State('vet_fn', 'value'),
        State('vet_ln', 'value'),
        State('vet_mi', 'value'),
        State('vet_suffix', 'value'),
        State('vet_email', 'value'),
        State('vet_cn', 'value'),
        State('url', 'search'),
    ]
   
)


def save_user_profile(n_clicks_btn, n_clicks_modal, vet_fn, vet_ln, vet_mi, vet_suffix, vet_email, vet_cn, url_search):
#def save_user_profile(savebtn, n_clicks, vet_fn, vet_ln, vet_mi, vet_suffix, vet_email, vet_cn):
   
    ctx = dash.callback_context # the ctx filter -- ensures that only a change in url will activate this callback
    print("Triggered:", ctx.triggered)


    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid and 'edituser_savebtn' in str(eventid):
        #if eventid and 'edituser_savebtn' in eventid:
            # savebtn condition checks if callback was activated by a click and not by having the save button appear in the layout


            # Set default outputs
            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False
            modal_text = ''
            modal_href = '#'


            parsed = urlparse(url_search)
            query_vet_id = parse_qs(parsed.query)

            if 'id' in query_vet_id:
                vet_id = query_vet_id['id'][0]
            else:
                # Handle the case when 'id' is not present in the URL
                # raise an error, redirect, or handle it accordingly
                raise PreventUpdate
           
            # check inputs if they have values
            if not vet_ln: # If vet_ln is blank, not vet_ln = True
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please supply the vet's last name."
            elif not vet_fn:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please supply the vet's first name."


            elif not vet_email:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please supply the vet's email."
            elif not vet_cn:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please supply the vet's contact number."


            else: #all inputs are valid


                #save to db
                sql_vet = """ UPDATE vet
                    SET
                        vet_ln = %s,
                        vet_fn = %s,
                        vet_mi = %s,
                        vet_suffix = %s,
                        vet_email = %s,
                        vet_cn= %s
                    WHERE
                        vet_id = %s
                    """
                   
                values_vet = [vet_ln, vet_fn, vet_mi, vet_suffix, vet_email, vet_cn, vet_id]
                print("values_vet:", values_vet)


                db.modifydatabase(sql_vet, values_vet)
               
                modal_text = "Changes in Vet Profile has been saved successfully."
                modal_href = '/viewuser' #go back to table
                modal_open = True
           
            return [alert_color, alert_text, alert_open, modal_open, modal_text, modal_href]


        else: # Callback was not triggered by desired triggers
            raise PreventUpdate
    else:
        raise PreventUpdate





#CALLBACK TO LOAD EDIT PAGE
@app.callback(
    [
        Output('vet_fn', 'value'),
        Output('vet_ln', 'value'),
        Output('vet_mi', 'value'),
        Output('vet_suffix', 'value'),
        Output('vet_email', 'value'),
        Output('vet_cn', 'value'),
    ],
    [
        Input('url', 'search'),
    ],
)




def current_values(url_search):
    parsed = urlparse(url_search)
    query_vet_id = parse_qs(parsed.query)




    if 'id' in query_vet_id:
        vet_id = query_vet_id['id'][0]
        sql = """
            SELECT vet_fn, vet_ln, vet_mi, vet_suffix,vet_email, vet_cn




            FROM vet
            WHERE vet_id = %s
        """
        values = [vet_id]
        col = ['vet_fn', 'vet_ln', 'vet_mi', 'vet_suffix', 'vet_email', 'vet_cn']




        df = db.querydatafromdatabase(sql, values, col)
       
        vet_fn = df['vet_fn'][0]
        vet_ln = df['vet_ln'][0]
        vet_mi = df['vet_mi'][0]
        vet_suffix = df['vet_suffix'][0]
        vet_email = df['vet_email'][0]
        vet_cn = df['vet_cn'][0]




        print(vet_fn, vet_ln, vet_mi, vet_suffix, vet_email, vet_cn)




        return [vet_fn, vet_ln, vet_mi, vet_suffix,vet_email, vet_cn]
   
    else:
        raise PreventUpdate

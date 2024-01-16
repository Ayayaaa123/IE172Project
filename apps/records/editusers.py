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
        dbc.Alert(id='newuserprofile_alert', is_open=False), # For feedback purposes
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
                                        dbc.Label("Username/Username"),
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




# @app.callback(
#     [
#         Output('newuserprofile_alert', 'is_open'),
   
#     [
#         Input('edituser_savebtn', 'n_clicks')
#     ],


#     [
#         State('vet_fn', 'value'),
#         State('vet_ln', 'value'),
#         State('vet_mi', 'value'),
#         State('vet_suffix', 'value'),
#         State('vet_email', 'value'),
#         State('vet_cn', 'value')
#     ],
#     ]
# )


# def save_user_profile(edituser_savebtn, n_clicks, vet_fn, vet_ln, vet_mi, vet_suffix, vet_email, vet_cn):
#     # Your save logic here
#     print(n_clicks, vet_fn, vet_ln, vet_mi, vet_suffix, vet_email, vet_cn)


#     # The ctx filter -- ensures that only a change in url will activate this callback
#     ctx = dash.callback_context
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid ==  edituser_savebtn:






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

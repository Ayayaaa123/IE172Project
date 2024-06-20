"""
        html.Div([ # problem table
            html.Br(),
            dbc.Card(
                [
                    dbc.CardHeader(
                    html.Div([
                        html.H2("Problem", className = 'flex-grow-1'),
                    ], className = "d-flex align-items-center justify-content-between")
                    ),
                    dbc.CardBody(
                        [
                            html.Div([
                                html.Div(id='homevisit_problem-table'),
                            ])
                        ]
                    )
                ]
            ),
        ], id = 'new_problem_card', style = {'display': 'none'}),

      #modal for editing visit details
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Edit Visit Details", style={'text-align': 'center', 'width': '100%'})),
            dbc.ModalBody([
                dbc.Alert(id = "homevisit_visitdetails_alert", is_open = False),
                dbc.Row([
                    dbc.Col(html.H4("Veterinarian Assigned"), width=6),
                    dbc.Col(
                        dcc.Dropdown(
                            id='homevisit_visitdetails_vetassigned',
                            options=[],
                            placeholder = "Select Veterinarian"
                        ),
                        width=6,
                    )
                ]),
                html.Div(style={'margin-bottom':'1rem'}),
                dbc.Row([
                    dbc.Col(html.H4("Visit Date"), width=6),
                    dbc.Col(
                        dmc.DatePicker(
                            id='homevisit_visitdetails_date',
                            dropdownType='modal',
                            inputFormat='MMM DD, YYYY',
                            placeholder = "Choose Date"
                        ),
                        width=6,
                    )
                ]),
                html.Div(style={'margin-bottom':'1rem'}),
                html.H3("Visit Purpose"),
                html.Hr(),
                dbc.Row([
                    dbc.Col(html.H4("For Vaccine?"), width=6),
                    dbc.Col(
                        dcc.Dropdown(
                            id='homevisit_visitdetails_forvaccine',
                            options=[
                                {"label": "Yes", "value": True},
                                {"label": "No", "value": False},
                            ],
                            placeholder='Visit Purpose: Vaccine?',
                        ), 
                        width=6,
                    )
                ]),
                html.Div(style={'margin-bottom':'1rem'}),
                dbc.Row([
                    dbc.Col(html.H4("For Deworm?"), width=6),
                    dbc.Col(
                        dcc.Dropdown(
                            id='homevisit_visitdetails_fordeworm',
                            options=[
                                {"label": "Yes", "value": True},
                                {"label": "No", "value": False},
                            ],
                            placeholder='Visit Purpose: Deworming?',
                        ), 
                        width=6,
                    )
                ]),
                html.Div(style={'margin-bottom':'1rem'}),
                dbc.Row([
                    dbc.Col(html.H4("For Problem?"), width=6),
                    dbc.Col(
                        dcc.Dropdown(
                            id='homevisit_visitdetails_forproblem',
                            options=[
                                {"label": "Yes", "value": True},
                                {"label": "No", "value": False},
                            ],
                            placeholder='Visit Purpose: Problem?',
                        ), 
                        width=6,
                    )
                ]),
                html.Div(style={'margin-bottom':'1rem'}),
                dbc.Row([
                    dbc.Col(html.H4("Problem Chief Complaint"), width=6),
                    dbc.Col(
                        dcc.Dropdown(
                            id='homevisit_visitdetails_problemname',
                            options=[],
                            placeholder='Select Problem',
                        ), 
                        width=6,
                    )
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Submit Visit Details", id = "homevisit_visitdetails_submit", className = "ms-auto"),
            ]),
        ], centered = True, id = "homevisit_visitdetails_modal", is_open = False, backdrop = "static", size = 'lg'),

        dbc.Modal(children = [ # successful saving of visit details
            dbc.ModalHeader(html.H4('Visit Details Recorded Successfully!', style={'text-align': 'center', 'width': '100%'}), close_button = False),
            dbc.ModalFooter([
                dbc.Button("Close", id = 'homevisit_visitdetails_close_successmodal', className = "btn btn-primary ms-auto", href=""),
                #dbc.Button("Close", id = "close_patient_successmodal", className = "ms-auto"),
            ]),
        ], centered = True, id = 'homevisit_visitdetails_successmodal', backdrop = 'static', is_open = False, keyboard = False),
  
        
"""


@app.callback( #opens and close form and success modal for editing client profile
        [
            Output('homevisit_client_modal', 'is_open'),
            Output('homevisit_client_successmodal', 'is_open'),
        ],
        [
            Input('homevisit_clientdetails', 'n_clicks'),
            Input('homevisit_client_submit','n_clicks'),
            Input('homevisit_client_close_successmodal','n_clicks'),
        ],
        [
            State('homevisit_client_modal', 'is_open'),
            State('homevisit_client_successmodal', 'is_open'),
            State('homevisit_client_fn', 'value'),
            State('homevisit_client_ln', 'value'),
            State('homevisit_client_contact_no', 'value'),
            State('homevisit_client_email', 'value'),
            State('homevisit_client_street', 'value'),
            State('homevisit_client_barangay', 'value'),
            State('homevisit_client_city', 'value'),
            State('homevisit_client_region', 'value'),
        ]
)
def homevisit_client_modal(create, submit, close, form, success, fn, ln, cn, email, street, brgy, city, region):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "homevisit_clientdetails" and create:
            return [not form, success]
            
        if eventid == 'homevisit_client_submit' and submit and all([fn, ln, cn, email, street, brgy, city, region]):
            return [not form, not success]
            
        if eventid == 'homevisit_client_close_successmodal' and close:
            return [form, not success]
            
    return [form, success]

@app.callback( #modal initial values
    [
        Output('homevisit_client_fn', 'value'),
        Output('homevisit_client_ln', 'value'),
        Output('homevisit_client_mi', 'value'),
        Output('homevisit_client_suffix', 'value'),
        Output('homevisit_client_contact_no', 'value'),
        Output('homevisit_client_email', 'value'),
        Output('homevisit_client_house_no', 'value'),
        Output('homevisit_client_street', 'value'),
        Output('homevisit_client_barangay', 'value'),
        Output('homevisit_client_city', 'value'),
        Output('homevisit_client_region', 'value'),
    ],
    [
        Input('homevisit_clientdetails', 'n_clicks'),
        Input('url', 'search'),
    ],
)
def homevisit_clientmodal_initial_values(click, url_search):
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)
    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'homevisit_clientdetails' and click:
                sql = """
                    SELECT 
                        client_fn,
                        client_ln,
                        client_mi,
                        client_suffix, 
                        client_cn, 
                        client_email,
                        client_house_no,
                        client_street,
                        client_barangay,
                        client_city,
                        client_region
                    FROM 
                        patient
                    INNER JOIN client ON patient.client_id = client.client_id
                    WHERE patient_id = %s
                """
                values = [patient_id]
                col = ['client_fn', 'client_ln', 'client_mi', 'client_suffix', 'client_cn', 'client_email', 'client_house_no', 'client_street', 'client_barangay', 'client_city', 'client_region']
                        
                df = db.querydatafromdatabase(sql, values, col)
                        
                client_fn = df['client_fn'][0]
                client_ln = df['client_ln'][0]
                client_mi = df['client_mi'][0]
                client_suffix = df['client_suffix'][0]
                client_cn = df['client_cn'][0]
                client_email = df['client_email'][0]
                client_house_no = df['client_house_no'][0]
                client_street = df['client_street'][0]
                client_barangay = df['client_barangay'][0]
                client_city = df['client_city'][0]
                client_region = df['client_region'][0]

                return [client_fn, client_ln, client_mi, client_suffix, client_cn, client_email, client_house_no, client_street, client_barangay, client_city, client_region]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate



@app.callback( # Submit Button for client profile
        [
            Output('homevisit_clientprofile_alert', 'color'),
            Output('homevisit_clientprofile_alert', 'children'),
            Output('homevisit_clientprofile_alert', 'is_open'),
            Output('homevisit_client_close_successmodal', 'href')
        ],
        [
            Input('homevisit_client_submit', 'n_clicks'),
            Input('url', 'search'),
            Input('homevisit_client_fn', 'value'),
            Input('homevisit_client_ln', 'value'),
            Input('homevisit_client_mi', 'value'),
            Input('homevisit_client_suffix', 'value'),
            Input('homevisit_client_contact_no', 'value'),
            Input('homevisit_client_email', 'value'),
            Input('homevisit_client_house_no', 'value'),
            Input('homevisit_client_street', 'value'),
            Input('homevisit_client_barangay', 'value'),
            Input('homevisit_client_city', 'value'),
            Input('homevisit_client_region', 'value'),
        ],
)
def homevisit_client_save(submitbtn, url_search, fn, ln, mi, sf, cn, email, house_no, street, brgy, city, region):
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)
    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'homevisit_client_submit' and submitbtn: 
                alert_open = False
                alert_color = ''
                alert_text = ''

                if not fn:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = "Please enter client's first name"
                elif not ln:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = "Please enter client's last name"
                elif not cn:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = "Please enter client's contact number"
                elif not email:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = "Please enter client's email address"
                elif not street:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = "Please enter client's street address"
                elif not brgy:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = "Please enter client's barangay"
                elif not city:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = "Please enter the city of client's address"
                elif not region:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = "Please enter the region of client's address"
                else:
                    sql = '''
                        SELECT client.client_id
                        FROM patient
                        INNER JOIN client ON patient.client_id = client.client_id
                        WHERE patient_id = %s
                    '''
                    values = [patient_id]
                    col = ['client_id']
                    df = db.querydatafromdatabase(sql, values, col)
                    client_id = int(df['client_id'][0])

                    modified_date = datetime.now().strftime("%Y-%m-%d")
                    sql = '''
                        UPDATE client 
                        SET
                            client_ln = %s,
                            client_fn = %s,
                            client_mi = %s,
                            client_suffix = %s,
                            client_email = %s,
                            client_cn = %s,
                            client_house_no = %s,
                            client_street = %s,
                            client_barangay = %s,
                            client_city = %s,
                            client_region = %s,
                            client_modified_date = %s
                        WHERE client_id = %s
                    '''
                    values = [ln, fn, mi, sf, email, cn, house_no, street, brgy, city, region, modified_date, client_id]

                    db.modifydatabase(sql, values)

                href = f'/home_visit/purpose?mode=add&patient_id={patient_id}&refresh={time.time()}'
                return [alert_color, alert_text, alert_open, href]
            
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    
@app.callback( #opens and close form and success modal for creating patient profile
        [
            Output('homevisit_patient_modal', 'is_open'),
            Output('homevisit_patient_successmodal', 'is_open'),
        ],
        [
            Input('homevisit_patientdetails', 'n_clicks'),
            Input('homevisit_patient_submit','n_clicks'),
            Input('homevisit_patient_close_successmodal','n_clicks'),
        ],
        [
            State('homevisit_patient_modal', 'is_open'),
            State('homevisit_patient_successmodal', 'is_open'),
            State('homevisit_patient_species', 'value'),
            State('homevisit_patient_breed', 'value'),
            State('homevisit_patient_color', 'value'),
            State('homevisit_patient_sex', 'value'),
            State('homevisit_patient_bd', 'value'),
            State('homevisit_patient_idiosync', 'value'),
        ]
)
def homevisit_patient_modal(create, submit, close, form, success, species, breed, color, sex, bd, idiosync):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "homevisit_patientdetails" and create:
            return [not form, success]
        
        if eventid == "homevisit_patient_submit" and submit and all([species, color, breed, sex, bd, idiosync]):
            return [not form, not success]
        
        if eventid == "homevisit_patient_close_successmodal" and close:
            return [form, not success]
           
    return [form, success]



@app.callback( #modal initial values
    [
        Output('homevisit_patient_m', 'value'),
        Output('homevisit_patient_species', 'value'),
        Output('homevisit_patient_breed', 'value'),
        Output('homevisit_patient_color', 'value'),
        Output('homevisit_patient_sex', 'value'),
        Output('homevisit_patient_bd', 'value'),
        Output('homevisit_patient_idiosync', 'value'),
    ],
    [
        Input('url', 'search'),
        Input('homevisit_patientdetails', 'n_clicks'),
    ],
)
def homevisit_patientmodal_initial_values(url_search, click):
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'homevisit_patientdetails' and click:
                sql = """
                    SELECT 
                        patient_m,
                        patient_species,
                        patient_breed,
                        patient_color,
                        patient_sex,
                        patient_bd,
                        patient_idiosync
                    FROM 
                        patient
                    WHERE patient_id = %s
                """
                values = [patient_id]
                col = ['patient_m', 'patient_species', 'patient_breed', 'patient_color', 'patient_sex', 'patient_bd', 'patient_idiosync']
                    
                df = db.querydatafromdatabase(sql, values, col)
                    
                patient_m = df['patient_m'][0]
                patient_species = df['patient_species'][0]
                patient_breed = df['patient_breed'][0]
                patient_color = df['patient_color'][0]
                patient_sex = df['patient_sex'][0]
                patient_bd = df['patient_bd'][0]
                patient_idiosync = df['patient_idiosync'][0]

                return [patient_m, patient_species, patient_breed, patient_color, patient_sex, patient_bd, patient_idiosync]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    
@app.callback( # Submit Button for patient profile
        [
            Output('homevisit_patientprofile_alert', 'color'),
            Output('homevisit_patientprofile_alert', 'children'),
            Output('homevisit_patientprofile_alert', 'is_open'),
            Output('homevisit_patient_close_successmodal', 'href')
        ],
        [
            Input('homevisit_patient_submit', 'n_clicks'),
            Input('url', 'search'),
            Input('homevisit_patient_m', 'value'),
            Input('homevisit_patient_species', 'value'),
            Input('homevisit_patient_breed', 'value'),
            Input('homevisit_patient_color', 'value'),
            Input('homevisit_patient_sex', 'value'),
            Input('homevisit_patient_bd', 'value'),
            Input('homevisit_patient_idiosync', 'value'),
        ],
)
def editprofile_patient_save(submitbtn, url_search, name, species, breed, color, sex, bd, idiosync):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'homevisit_patient_submit' and submitbtn: 
            parsed = urlparse(url_search)
            query_patient_id = parse_qs(parsed.query)
            if 'patient_id' in query_patient_id:
                patient_id = query_patient_id['patient_id'][0]
        
                alert_open = False
                alert_color = ''
                alert_text = ''

                if not species:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the species of the patient'
                elif not breed:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the breed of the patient'
                elif not color:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please describe the color or any color marks on the patient'
                elif not sex:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the sex of the patient'
                elif not bd:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please enter the birth date of the patient'
                elif not idiosync:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please describe any behavior or characteristic of the patient'
                else:
                    modified_date = datetime.now().strftime("%Y-%m-%d")
                    sql = '''
                        UPDATE patient 
                        SET
                            patient_m = %s,
                            patient_species = %s,
                            patient_breed = %s,
                            patient_color = %s,
                            patient_sex = %s,
                            patient_bd = %s,
                            patient_idiosync = %s,
                            patient_modified_date = %s
                        WHERE patient_id = %s
                    '''
                    values = [name, species, breed, color, sex, bd, idiosync, modified_date, patient_id]

                    db.modifydatabase(sql, values)

                href = f'/home_visit/purpose?mode=add&patient_id={patient_id}&refresh={time.time()}'

                return [alert_color, alert_text, alert_open, href]
            
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback( #opens and close form and success modal for editing visit details
        [
            Output('homevisit_visitdetails_modal', 'is_open'),
            Output('homevisit_visitdetails_successmodal', 'is_open'),
        ],
        [
            Input('homevisit_visitdetails', 'n_clicks'),
            Input('homevisit_visitdetails_submit','n_clicks'),
            Input('homevisit_visitdetails_close_successmodal','n_clicks'),
        ],
        [
            State('homevisit_visitdetails_modal', 'is_open'),
            State('homevisit_visitdetails_successmodal', 'is_open'),
            State('homevisit_visitdetails_date', 'value'),
            State('homevisit_visitdetails_forvaccine', 'value'),
            State('homevisit_visitdetails_fordeworm', 'value'),
            State('homevisit_visitdetails_forproblem', 'value'),
        ]
)
def homevisit_visitdetails_modal(create, submit, close, form, success, date, forvaccine, fordeworm, forproblem):
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "homevisit_visitdetails" and create:
            return [not form, success]
        
        if eventid == "homevisit_visitdetails_submit" and submit and all([date, forvaccine, fordeworm, forproblem]):
            return [not form, not success]
        
        if eventid == "homevisit_visitdetails_close_successmodal" and close:
            return [form, not success]
           
    return [form, success]

@app.callback( #modal initial values
    [
        Output('homevisit_visitdetails_vetassigned', 'options'),
        Output('homevisit_visitdetails_vetassigned', 'value'),
        Output('homevisit_visitdetails_date', 'value'),
        Output('homevisit_visitdetails_forvaccine', 'value'),
        Output('homevisit_visitdetails_fordeworm', 'value'),
        Output('homevisit_visitdetails_forproblem', 'value'),
        Output('homevisit_visitdetails_problemname', 'options'),
        Output('homevisit_visitdetails_problemname', 'value'),
    ],
    [
        Input('url', 'search'),
        Input('homevisit_visitdetails', 'n_clicks'),
    ],
)
def homevisit_visitdetailsmodal_initial_values(url_search, click):
    ctx = dash.callback_context
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'homevisit_visitdetails' and click:
                sql = """
                    SELECT 
                        vet_id,
                        COALESCE(vet_ln, '') || ', ' || COALESCE (vet_fn, '') || ' ' || COALESCE (vet_mi, '') AS vet_name
                    FROM 
                        vet
                    WHERE 
                        NOT vet_delete_ind
                """
                values = []
                cols = ['vet_id', 'vet_name']
                result = db.querydatafromdatabase(sql, values, cols)
                options1 = [{'label': row['vet_name'], 'value': row['vet_id']} for _, row in result.iterrows()]
                
                sql = """
                    SELECT DISTINCT
                        problem.problem_id,
                        problem_chief_complaint
                    FROM 
                        problem
                    INNER JOIN visit ON problem.problem_id = visit.problem_id
                    INNER JOIN patient ON visit.patient_id = patient.patient_id
                    WHERE 
                        NOT problem_delete_ind AND patient.patient_id = %s
                """
                values = [patient_id]
                cols = ['problem_id', 'problem_complaint']
                result = db.querydatafromdatabase(sql, values, cols)
                options2 = [{'label': row['problem_complaint'], 'value': row['problem_id']} for _, row in result.iterrows()]
                
                sql = """
                    SELECT MAX(visit_id)
                    FROM visit
                    """
                values = []
                df = db.querydatafromdatabase(sql,values)
                visit_id = int(df.loc[0,0])

                sql = """
                    SELECT 
                        vet_id,
                        visit_date,
                        visit_for_vacc,
                        visit_for_deworm,
                        visit_for_problem,
                        problem_id
                    FROM 
                        visit
                    WHERE
                        visit_id = %s
                """
                values = [visit_id]
                col = ['vet_id', 'visit_date', 'visit_for_vacc', 'visit_for_deworm', 'visit_for_problem', 'problem_id']
                    
                df = db.querydatafromdatabase(sql, values, col)
                    
                vet_id = df['vet_id'][0]
                visit_date = df['visit_date'][0]
                visit_for_vacc = df['visit_for_vacc'][0]
                visit_for_deworm = df['visit_for_deworm'][0]
                visit_for_problem = df['visit_for_problem'][0]
                problem_id = df['problem_id'][0]

                return [options1, vet_id, visit_date, visit_for_vacc, visit_for_deworm, visit_for_problem, options2, problem_id]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    



@app.callback( # Submit Button for patient profile
        [
            Output('homevisit_visitdetails_alert', 'color'),
            Output('homevisit_visitdetails_alert', 'children'),
            Output('homevisit_visitdetails_alert', 'is_open'),
            Output('homevisit_visitdetails_close_successmodal', 'href')
        ],
        [
            Input('homevisit_visitdetails_submit', 'n_clicks'),
            Input('url', 'search'),
            Input('homevisit_visitdetails_vetassigned', 'value'),
            Input('homevisit_visitdetails_date', 'value'),
            Input('homevisit_visitdetails_forvaccine', 'value'),
            Input('homevisit_visitdetails_fordeworm', 'value'),
            Input('homevisit_visitdetails_forproblem', 'value'),
            Input('homevisit_visitdetails_problemname', 'value'),
        ],
)
def editprofile_visitdetails_save(submitbtn, url_search, vet, date, forvaccine, fordeworm, forproblem, problemname):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'homevisit_visitdetails_submit' and submitbtn: 
            parsed = urlparse(url_search)
            query_patient_id = parse_qs(parsed.query)
            
            if 'patient_id' in query_patient_id:
                patient_id = query_patient_id['patient_id'][0]

                sql = """
                    SELECT MAX(visit_id)
                    FROM visit
                    """
                values = []
                df = db.querydatafromdatabase(sql,values)
                visit_id = int(df.loc[0,0])
        
                alert_open = False
                alert_color = ''
                alert_text = ''

                if not vet:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the veterinarian assigned'
                elif not date:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the visit date'
                elif not forvaccine:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the purpose of visit'
                elif not fordeworm:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the purpose of visit'
                elif not forproblem:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please indicate the purpose of visit'
                else:
                    sql = '''
                        UPDATE visit
                        SET
                            vet_id = %s,
                            visit_date = %s,
                            visit_for_vacc = %s,
                            visit_for_deworm = %s,
                            visit_for_problem = %s,
                            problem_id = %s
                        WHERE visit_id = %s
                    '''
                    values = [vet, date, forvaccine, fordeworm, forproblem, problemname, visit_id]

                    db.modifydatabase(sql, values)

                href = f'/home_visit/purpose?mode=add&patient_id={patient_id}&refresh={time.time()}'

                return [alert_color, alert_text, alert_open, href]
            
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback( #problem table content
    Output('homevisit_problem-table', 'children'),
    Input('url', 'search'),
)
def homevisit_problem_table(url_search):
    parsed = urlparse(url_search)
    query_patient_id = parse_qs(parsed.query)

    if 'patient_id' in query_patient_id:
        patient_id = query_patient_id['patient_id'][0]
        sql = """
        SELECT DISTINCT
            problem_chief_complaint, problem_diagnosis, problem_prescription, problem_client_educ, problem_status_m, problem_date_created, problem_date_resolved, problem.problem_id, patient.patient_id
        FROM 
            problem
        INNER JOIN problem_status ON problem.problem_status_id = problem_status.problem_status_id
        INNER JOIN visit ON problem.problem_id = visit.problem_id
        INNER JOIN patient ON visit.patient_id = patient.patient_id
        WHERE patient.patient_id = %s AND problem_delete_ind = false
        """
        values = [patient_id]
        sql += "ORDER BY problem.problem_id DESC"
        col = ['Chief Complaint', 'Diagnosis', 'Prescription', 'Patient Instructions', 'Problem Status', 'Start Date', 'Resolved Date', 'Problem_ID', 'Patient_ID']
        df = db.querydatafromdatabase(sql, values, col)

        if df.shape:
            buttons = []
            for problem_id, patient_id_query in zip(df['Problem_ID'], df['Patient_ID']):
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'/editproblem?mode=add&problem_id={problem_id}&patient_id={patient_id_query}', size='sm', color='success'),
                        style = {'text-align':'center'}
                    )
                ]

            df['Action'] = buttons
            df = df[['Chief Complaint', 'Diagnosis', 'Prescription', 'Patient Instructions', 'Problem Status', 'Start Date', 'Resolved Date', 'Action']] 

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'text-align': 'center'})
            return [table]

    else:
        raise PreventUpdate



from dash import html,dash_table,dcc
import dash_bootstrap_components as dbc
from datetime import date
#All the buttons should open seperate Windows

today = date.today()
# dd/mm/YY day month year
dmy = today.strftime("%d/%m/%Y")

#Add in Address, Postal Code, City, Province
ClientModal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Add Client Information")),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(type="text", placeholder="Bob"),
                    dbc.Label("First Name"),
                ]),
            ]),
            dbc.Col([
                dbc.FormFloating([
                dbc.Input(type="text", placeholder="Smith"),
                dbc.Label("Last Name"),
                ]),
            ])  
        ]),
        dbc.Row([
            dbc.FormFloating([
                dbc.Input(type="email", placeholder="example@gmail.com"),
                dbc.Label("Email"),
            ])
        ]),
        dbc.Row([
            dbc.FormFloating([
                dbc.Input(type="number", placeholder="999-999-9999"),
                dbc.Label("Phone Number"),
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Date of Visit: "),
            ]),
            dbc.Col([
                dbc.FormFloating([
                    dcc.DatePickerSingle(
                        id='ClientDateVisit',
                        initial_visible_month=date.today(),
                        date=date.today(),
                        clearable=True,
                    ),
                ])
            ]),
            dbc.Col([
                dbc.Label("Date of Followup:")
            ]),
            dbc.Col([
                dbc.FormFloating([
                    dcc.DatePickerSingle(
                        id='ClientFollowup',
                        initial_visible_month=date.today(),
                        date=date.today(),
                        clearable=True,
                    ),
                ])
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Has a Hearing Aid:")
            ]),
            dbc.Col([
                dcc.Dropdown(['Yes',"No"],'No',id="HearingAidDropdown")
            ])
        ]),
        #Hearing Aid Container, Appears when Hearing aid = Yes
        #Maybe make Collapse instead of a Div
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Model:")
                ]),
                dbc.Col([
                    dcc.Dropdown(['One',"Two"],'One')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Purchased at Prosound:")
                ]),
                dbc.Col([
                    dcc.Dropdown(['Yes',"No"],'No',id='PurchaseDropdown')
                ]),  
            ]),
            #Displays only if customer purchases at Prosound
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Date Purchased:")
                    ]),
                    dbc.Col([
                        dcc.DatePickerSingle(
                                id='ClientHearingAidPurchase',
                                initial_visible_month=date.today(),
                                date=date.today(),
                                clearable=True,
                            ),
                    ])
                ])
            ],id="PurchaseDateContainer",style={'display':'None'}),
        ],
        id="HearingAidContainer",style={'display':'None'}),
        dbc.Row([
            dbc.Col([
                dbc.Label("Did Hearing Test:")
            ]),
            dbc.Col([
                dcc.Dropdown(['Yes',"No"],'No',id="HearingTestDropdown")
            ])
        ]),
        #Hearing Test Container, Appears when Hearing Test = Yes
        dbc.Row([
            dbc.Col([
                dbc.Label("Date Of Test:")
            ]),
            dbc.Col([
                dcc.DatePickerSingle(
                        id='ClientHearingTest',
                        initial_visible_month=date.today(),
                        date=date.today(),
                        clearable=True,
                    ),
            ])
        ],
        id="HearingTestContainer",style={'display':'None'}
        ),
        dbc.Row([
            dbc.Label('Notes')
        ]),
        dbc.Row([
            dcc.Textarea(id='NotesText'
            )
        ]),
        dbc.Row([
            dbc.Col([]),
            dbc.Col([]),
            dbc.Col([
                dbc.Button(["Confirm"])
            ])
        ])
    ])
],id='ClientModal',is_open=False,size="xl")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([dbc.Button(["Add New Client"],id="ClientButton",n_clicks=0)]),
        dbc.Col([dbc.Button(["Task List"])]),
        dbc.Col([
            dbc.Button([
                "View Followups",dbc.Badge("4",color="White", text_color="primary", className="ms-1"),
            ]),
        ]),
    ]),
    dbc.Row([ClientModal])
])


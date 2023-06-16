from dash import html,dash_table,dcc
import dash_bootstrap_components as dbc
from datetime import date
#All the buttons should open seperate Windows

today = date.today()
# dd/mm/YY day month year
dmy = today.strftime("%d/%m/%Y")

ClientModal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Add Client Information")),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(id="ClientFirstName",type="text", placeholder="Bob"),
                    dbc.Label("First Name"),
                ]),
            ]),
            dbc.Col([
                dbc.FormFloating([
                dbc.Input(id="ClientLastName",type="text", placeholder="Smith"),
                dbc.Label("Last Name"),
                ]),
            ])  
        ],style={'margin-bottom':'10px'}),
        dbc.Row([
            dbc.FormFloating([
                dbc.Input(id="ClientEmail",type="email", placeholder="example@gmail.com"),
                dbc.Label("Email"),
            ])
        ],style={'margin-bottom':'10px'}),
        dbc.Row([
            dbc.FormFloating([
                dbc.Input(id="ClientPhone",type="number", placeholder="999-999-9999"),
                dbc.Label("Phone Number"),
            ])
        ],style={'margin-bottom':'10px'}),
        dbc.Row([
            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(id="ClientAddress",placeholder="12 Sesame Drive"),
                    dbc.Label("Home Address"),
                ])
            ]),
            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(id="ClientPostalCode",placeholder="T1C-7Z5"),
                    dbc.Label("Postal Code"),
                ])
            ]),
            
        ],style={'margin-bottom':'10px'}),
        dbc.Row([
            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(id="ClientCity",placeholder="Toronto"),
                    dbc.Label("City"),
                ])
            ]),
            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(id="ClientProvince",placeholder="Ontario"),
                    dbc.Label("Province"),
                ])
            ]),
        ],style={'margin-bottom':'10px'}),
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
        ],style={'margin-bottom':'10px'}),
        dbc.Row([
            dbc.Col([
                dbc.Label("Has a Hearing Aid:")
            ]),
            dbc.Col([
                dcc.Dropdown(['Yes',"No"],'No',id="HearingAidDropdown")
            ])
        ],style={'margin-bottom':'10px'}),
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
        ],style={'margin-bottom':'10px'}),
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
    ]),
    dbc.ModalFooter([
        dbc.Button(["Confirm"],id="ClientConfirm",n_clicks=0,style={'margin-top':'10px'}),
        dbc.Toast(
            children=[],
            id="ClientConfirmToast",
            header="Client Added",
            icon="primary",
            duration=4000,
            is_open=False
        )
    ])
],id='ClientModal',is_open=False,size="xl")

FollowupModal = dbc.Modal([
    dbc.ModalHeader(),
    dbc.ModalBody(),
    dbc.ModalFooter(),
])

#
#Whole Layout
#

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


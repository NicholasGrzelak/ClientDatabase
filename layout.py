from dash import html,dash_table,dcc
import dash_bootstrap_components as dbc
from datetime import date
#All the buttons should open seperate Windows
#Popovers to provide tool tips

##
#MODALS
##

#Maybe if has hearing aid, then button to add new hearing aid to log peoples hearing aids
#Need Model, Date, Invoice, Heath Card?
#Still need to add clientidnumber and add to database
#Still need to add a Add hearing aid button
ClientModal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Add Client Information")),
    dbc.ModalBody([
        dbc.Row([
            dbc.FormFloating([
                dbc.Input(id="ClientNumber",type="number", placeholder="100"),
                dbc.Label("Client #"),
            ],style={'textAlign':'center','margin-bottom':'10px'}),
        ]),
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
            dbc.FormFloating([
                dbc.Input(id="ClientHealthCard", placeholder="9999-999-999-AA"),
                dbc.Label("Health Card"),
            ])
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
        # dbc.Row([
        #     dbc.Col([
        #         dbc.Label("Has a Hearing Aid:")
        #     ]),
        #     dbc.Col([
        #         dcc.Dropdown(['Yes',"No"],'No',id="HearingAidDropdown")
        #     ])
        # ],style={'margin-bottom':'10px'}),
        # #Hearing Aid Container, Appears when Hearing aid = Yes
        # #Maybe make Collapse instead of a Div
        # html.Div([
        #     dbc.Row([
        #         dbc.Col([
        #             dbc.Label("Model:")
        #         ]),
        #         dbc.Col([
        #             dcc.Dropdown(['One',"Two"],'One',id='ClientModel')
        #         ]),
        #     ]),
        #     dbc.Row([
        #         dbc.Col([
        #             dbc.Label("Purchased at Prosound:")
        #         ]),
        #         dbc.Col([
        #             dcc.Dropdown(['Yes',"No"],'No',id='ClientPurchaseDropdown')
        #         ]),  
        #     ]),
        #     #Displays only if customer purchases at Prosound
        #     html.Div([
        #         dbc.Row([
        #             dbc.Col([
        #                 dbc.Label("Date Purchased:")
        #             ]),
        #             dbc.Col([
        #                 dcc.DatePickerSingle(
        #                         id='ClientHearingAidPurchase',
        #                         initial_visible_month=date.today(),
        #                         date=date.today(),
        #                         clearable=True,
        #                     ),
        #             ])
        #         ])
        #     ],id="PurchaseDateContainer",style={'display':'None'}),
        # ],
        # id="HearingAidContainer",style={'display':'None'}),
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
        id="HearingTestContainer",style={'display':'None','margin-bottom':'10px'}
        ),
        dbc.Row([
            dbc.Col([]),
            dbc.Col([dbc.Button('Add Hearing Aid',id='ClientAddHearingAid',n_clicks=0)],style={'textAlign':'center'}),
            dbc.Col([]),
        ],style={'margin-bottom':'10px'}),
        dbc.Row([
            dbc.Label('Notes')
        ]),
        dbc.Row([
            dcc.Textarea(id='ClientNotesText')
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
],id='ClientModal',is_open=False,size="xl")\

#Aid Hearing Aid Modal
hearingaidmodal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle('Add Hearing Aid')),
    dbc.ModalBody([
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Client Number:")
                ]),
                dbc.Col([
                    dcc.Input(id='HearingAidClientIDNumber')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Invoice Number:")
                ]),
                dbc.Col([
                    dcc.Input(id='HearingAidInvoiceNumber')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Quantity:")
                ]),
                dbc.Col([
                    dcc.Input(id='ClientHearingAidQuantity')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Status:")
                ]),
                dbc.Col([
                    dcc.Dropdown(options=["Trying","Returned","Purchased"],id='ClientHearingAidStatus')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Manufacturer:")
                ]),
                dbc.Col([
                    dcc.Dropdown(options=['Bernafon',"Other"],placeholder='Bernafon',id='ClientHearingAidManufacturer')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Model:")
                ]),
                dbc.Col([
                    dcc.Dropdown(['One',"Two"],'One',id='ClientHearingAidModel')
                ]),
            ]),
             dbc.Row([
                dbc.Col([
                    dbc.Label("Type:")
                ]),
                dbc.Col([
                    dcc.Dropdown(['One',"Two"],'One',id='ClientHearingAidType')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Left Serial:")
                ]),
                dbc.Col([
                    dcc.Input(id='HearingAidLSerialNumber')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Right Serial:")
                ]),
                dbc.Col([
                    dcc.Input(id='HearingAidRSerialNumber')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Dispense Date:")
                ]),
                dbc.Col([
                    dcc.DatePickerSingle(
                        id='ClientHearingAidDispenseDate',
                        initial_visible_month=date.today(),
                        date=date.today(),
                        clearable=True,
                    ),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Invoice Paid:")
                ]),
                dbc.Col([
                    dcc.Dropdown(['Yes',"No"],'Yes',id='HearingAidPaidInvoice')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Payment Date:")
                ]),
                dbc.Col([
                    dcc.DatePickerSingle(
                        id='ClientHearingAidPurchase',
                        initial_visible_month=date.today(),
                        date=date.today(),
                        clearable=True,
                    ),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Payment Amount: ")
                ]),
                dbc.Col([
                    dcc.Input(id='HearingAidPaymentAmount')
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("MSRP: ")
                ]),
                dbc.Col([
                    dcc.Input(id='ClientHearingAidMSRP')
                ]),
            ]),
        ],
        id="HearingAidContainer"),
    ])
],id='hearingAidModal')


#Follow Up Modal
# Should have name, email, phonenumber
# On the right of each client should have option to follow up or couldnt get ahold of
FollowupModal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Client Follow Ups")),
    dbc.ModalBody([
        dbc.Container(id="FollowUpsContainer")
    ]),
    dbc.ModalFooter(),
],id='followUpModal',is_open=False,size="xl")

#

settingsModal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Settings")),
    dbc.ModalBody([
        dbc.Row([html.H5('Client Settings')]),
        dbc.Row([
            dbc.Col([dbc.Label('Routine Follow Up After:')]),
            dbc.Col([dcc.Dropdown(options=['3 months','6 months','12 months'],placeholder='6 months',id="FollowUpSettings")])
        ]),
        dbc.Row([
            dbc.Col([dbc.Label('Test Follow Up After: ')]),
            dbc.Col([dcc.Dropdown(options=['12 months'],placeholder='12 months',id="FollowUpSettingsTest")])
        ]),
        dbc.Row([
            dbc.Col([dbc.Label('Payment Follow Up After: ')]),
            dbc.Col([dcc.Dropdown(options=['30 days','45 days','60 days'],placeholder='30 days',id="FollowUpSettingsPayment")])
        ]),
        dbc.Row([
            dbc.Col([dbc.Label('Hearing Aid Follow Up After: ')]),
            dbc.Col([dcc.Dropdown(options=['14 days','28 days','30 days'],placeholder='14 days',id="FollowUpSettingsHearing")])
        ],style={'margin-bottom':'10px'}),
        dbc.Row([
            html.H5('Uploads')
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label(['Upload Client Datasheet'])
            ],style={'textAlign': 'center'}),
            dbc.Col([
                dbc.Label(['Upload Hearing Aid Datasheet'])
            ],style={'textAlign': 'center'})
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Upload(
                    id='ClientsUpload',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                ),
            dbc.Toast(
                children=[],
                id="ClientUploadConfirm",
                header="Clients Added",
                icon="primary",
                duration=4000,
                is_open=False
            )
            ]),
            dbc.Col([
                dcc.Upload(
                    id='DataUpload',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                ),
                dbc.Toast(
                    children=[],
                    id="DataUploadConfirm",
                    header="Hearing Aids Added",
                    icon="primary",
                    duration=4000,
                    is_open=False
                )
            ])
        ])
    ]),
    dbc.ModalFooter(),
],id='settingsModal',is_open=False,size="xl")

#TaskListModal
#Should be able to make and complete Tasks Dynamically
#Maybe dbc.Checklist
taskListModal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Tasks")),
    dbc.ModalBody([
        dbc.Row([html.H3('Tasks to be completed:')]),
        dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText(
                    dbc.Checkbox(id={"type": "task-checkbox", "index": "1"})
                ),
                dbc.Input(id={"type": "task", "index": "1"})
            ])
        ],id="tasksContainer"),
        dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText(
                    dbc.Checkbox(id={"type": "task-checkbox", "index": "2"})
                ),
                dbc.Input(id={"type": "task", "index": "2"})
            ])
        ],id="newTaskAdder",style={'margin-bottom':'10px'}),
        dbc.Row([html.H3('Completed Tasks:')]),
        dbc.Row([],id="completedTaskContainer"),
    ]),
    dbc.ModalFooter(),
],id='taskListModal',is_open=False,size="xl")

#LOGIN MODAL

loginModal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Login"),close_button=False),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Label('Username:')
            ],style={'textAlign':'center'},width=3,align='center'),
            dbc.Col([
                dbc.Input(id='usernameEnter')
            ],width=9),
        ],style={'margin-bottom':'10px'}),
        dbc.Row([  
            dbc.Col([
                dbc.Label('Password:')
            ],style={'textAlign':'center'},width=3,align='center'),
            dbc.Col([
                dbc.Input(id='passwordEnter')
            ],width=9),
        ],style={'margin-bottom':'10px'}),
        dbc.Row([
            dbc.Col([
                dbc.Button('Sign In',id='signInButton',n_clicks=0),
                dbc.Toast(
                    id='loginToast',
                    header='Login Failed',
                    duration=4000,
                    icon='danger',
                    is_open=False
                )
            ])
        ],style={'textAlign':'center'})
    ]),
    dbc.ModalFooter(),
],id='loginModal',is_open=True,backdrop='static')

#Task List Modal
#Should have check boxes for tasks that go into the top of bottom container once checkchecked. Then in bottom container tasks can be deleted.
#Maybe store in another database, see if a good way to make new task without clicking a add button, try to add at the bottom of current task list

#Need Filters Modal
#Should have check boxes for what should be filtered on client dropdown
#Should have option to input client names, phonenumber, email, or clientnumber

##
##Navbar
##

navitems = dbc.Row([
    dbc.Col([
        dbc.Button(['Sales'],id="salesButton",class_name="bg-transparent border-0")
    ]),
    #text-secondary
    dbc.Col([
        dbc.Button(['Settings'],id="settingsButton",n_clicks=0,class_name="bg-transparent border-0")
    ]),
],class_name="ms-auto flex-nowrap mt-3 mt-md-0",align="center")

##
#Whole Layout
##

layout = dbc.Container([
    dbc.Navbar([
        dbc.Container([
            dbc.Row([
                dbc.NavbarBrand('Hearing Management',class_name='ms-2')
            ],
            align="center",
            class_name="g-0"
            ),
            dbc.NavbarToggler(id="navbar-toggler",n_clicks=0),
            dbc.Collapse(navitems,id="navbar-collapse",is_open="false",navbar=True)
        ],fluid=True),
    ],style={'margin-bottom':'35px'},expand=True,dark=True,color='primary'),
    dbc.Row([
        dbc.Col([dbc.Button(["Add New Client"],id="ClientButton",n_clicks=0)],style={'textAlign':'center'}),
        dbc.Col([dbc.Button(["Task List (WIP)"],id="taskListButton")],style={'textAlign':'center'}),
        dbc.Col([
            dbc.Button(
                [
                    "View Followups",dbc.Badge("4",id="followUpBadge",color="secondary", text_color="primary",pill=True, className="ms-1")
                ],
                id="followUpButton")]
            ,style={'textAlign':'center'}),
    ],justify="end",class_name='g-0'),
    dbc.Row([ClientModal,FollowupModal,settingsModal,taskListModal,hearingaidmodal,loginModal,
                dcc.Store(id='memory-output')
            ],style={'margin-bottom':'20px'},),
    dbc.Row([
        dbc.Col([dbc.Button(["Filters (WIP)"],id="ClientSelectFilter")],md={"size":3,'offset':1},style={'textAlign':'right'}),
        dbc.Col([dcc.Dropdown(id="ClientSelectDropdown",options=['A',"B"])],md={"size":4}),
    ],style={'margin-bottom':'20px'}),
    #Add in container Purchased Hearing Aid Button
    #Add in Container Inputs so that customer information can be changed
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("ID"),
                    dbc.Input(id='changeID')
                ],class_name='mb-3')
            ],width=2),
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("First Name"),
                    dbc.Input(id='changeFirstName',value=None)
                ],class_name='mb-3') 
            ],width=4),
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("Last Name"),
                    dbc.Input(id='changeLastName',value=None)
                ],class_name='mb-3') 
            ],width=4),
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("Status"),
                    dcc.Dropdown(options=["Open","Close"],placeholder="Open",id='changeStatus',style={'flex':'1 1 auto','align-self':'center'})
                ],class_name='mb-3') 
            ],width=2),
        ]),
        dbc.Row([
            dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("Email"),
                        dbc.Input(id='changeEmail')
                    ],class_name='mb-3')
                ]),
            dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("Phone Number"),
                        dbc.Input(id='changePhoneNumber')
                    ],class_name='mb-3')
                ]),
        ]),
        dbc.Row([
            dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("Address"),
                        dbc.Input(id='changeAddress')
                    ],class_name='mb-3')
            ],width=4),
            dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("Postal Code"),
                        dbc.Input(id='changePostalCode')
                    ],class_name='mb-3')
            ],width=3),
            dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("City"),
                        dbc.Input(id='changeCity')
                    ],class_name='mb-3')
            ],width=3),
            dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("Province"),
                        dbc.Input(id='changeProvince')
                    ],class_name='mb-3')
            ],width=2),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("Health Card"),
                    dbc.Input(id='changeHealthCard')
                ],class_name='mb-3')
            ],width=5),
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("Visit:"),
                    dcc.DatePickerSingle(
                        id='changeVisitDate',
                        initial_visible_month=date.today(),
                        date=date.today(),
                        disabled=True,
                        clearable=True,
                    ),
                ],class_name='mb-3')
            ]),
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("Followed Up:"),
                    dcc.DatePickerSingle(
                        id='changeFollowDate',
                        initial_visible_month=date.today(),
                        date=date.today(),
                        disabled=True,
                        clearable=True,
                    ),
                ],class_name='mb-3')
            ]),
        ]),
        dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText("Notes"),
                dbc.Textarea(id='changeNotes')
            ],class_name='mb-3')
        ]),
        dbc.Row([
            dbc.Container([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("Invoice #"),
                                dbc.Input(id='changeInvoiceNumber')
                            ],class_name='mb-3')
                        ]),
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("Hearing Aid Status"),
                                dcc.Dropdown(options=["Trying","Returned","Purchased"],id='changeAidStatus',style={'flex':'1 1 auto','align-self':'center'})
                            ],class_name='mb-3')
                        ]),
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("Dispensed Date:"),
                                dcc.DatePickerSingle(
                                    id='changeDispenseDate',
                                    initial_visible_month=date.today(),
                                    date=date.today(),
                                    disabled=False,
                                    clearable=True,
                                ),
                            ])
                        ],class_name='mb-3')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("Quantity"),
                                dcc.Dropdown(options=["1","2"],id='changeQuan',style={'flex':'1 1 auto','align-self':'center'})
                            ],class_name='mb-3')
                        ],width=3),
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("Manufacturer"),
                                dcc.Dropdown(id='changeHearingAidMake',options=['Bernafon','Other'],style={'flex':'1 1 auto','align-self':'center'})
                            ],class_name='mb-3')
                        ],width=3),
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("Model"),
                                dcc.Dropdown(id='changeHearingAidModel',style={'flex':'1 1 auto','align-self':'center'})
                            ],class_name='mb-3')
                        ],width=3),
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("Type"),
                                dcc.Dropdown(id='changeHearingAidType',style={'flex':'1 1 auto','align-self':'center'})
                            ],class_name='mb-3')
                        ],width=3),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("Left Serial Number"),
                                dbc.Input(id='changeHearingAidLSerial')
                            ],class_name='mb-3')
                        ],width={'size':4}),
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("Right Serial Number"),
                                dbc.Input(id='changeHearingAidRSerial')
                            ],class_name='mb-3')
                        ],width={'size':4}),
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("Paid"),
                                dcc.Dropdown(options=["Yes","No"],id='changePaid',style={'flex':'1 1 auto','align-self':'center'})
                            ],class_name='mb-3')
                        ],width=4)
                    ]),
                ],id="changeHearingAidPurchaseDiv"),
                dbc.Row([                
                    dbc.Col([
                        dbc.InputGroup([
                            dbc.InputGroupText("Payment Date"),
                            dcc.DatePickerSingle(
                                id='changePaymentDate',
                                initial_visible_month=date.today(),
                                date=date.today(),
                                clearable=True,
                            ),
                        ],class_name='mb-3')
                    ]),
                    dbc.Col([
                        dbc.InputGroup([
                            dbc.InputGroupText("Invoice $"),
                            dbc.Input(id='changeInvoiceAmount')
                        ],class_name='mb-3')
                    ]),
                    dbc.Col([
                        dbc.InputGroup([
                            dbc.InputGroupText("MSRP"),
                            dbc.Input(id='changeMSRP')
                        ],class_name='mb-3')
                    ])
                ],id='changePaymentDiv')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(options=["Hearing Test","Hearing Aid Dispensing","Hearing Aid Purchase","Ear Cleaning"],id="changeAppointmentType",multi=True)
            ]),
            dbc.Col([
                dbc.Button("Update",id='changeClientInfo',n_clicks=0),
                dbc.Toast(
                    children=[],
                    id="ClientUpdateToast",
                    header="Client Updated",
                    icon="primary",
                    duration=4000,
                    is_open=False
                )
            ]) #only activates if something has been updated
        ],style={'margin-bottom':'10px'})
    ],id="ClientContainer",class_name="border rounded-pill")
],fluid=True,style={'padding':'0'})


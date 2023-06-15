from dash import html,dash_table,dcc
import dash_bootstrap_components as dbc
#All the buttons should open seperate Windows
layout = dbc.Container([
    dbc.Row([
        html.H1(id='total-balance',children=['test']),
        dbc.Button(["Add New Client"]),
        dbc.Button(["View Followups",dbc.Badge("4",color="White", text_color="primary", className="ms-1"),
    ]),
        dbc.Button(["Task List"])
    ]),
])
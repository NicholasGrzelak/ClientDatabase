from hashlib import new
from tkinter import Y
from weakref import ref
from dash import Output,Input,MATCH,State,ctx,dcc,ALL
import dash_bootstrap_components as dbc
import pandas as pd
from App import app
from datetime import date
from functions import *
import plotly.graph_objects as go
import sqlite3

today = date.today()
# dd/mm/YY day month year
dmy = today.strftime("%d/%m/%Y")

#Modal Toggles

app.callback(
    Output("ClientModal", "is_open"),
    Input("ClientButton", "n_clicks"),
    State("ClientModal", "is_open"),
)(toggle_modal)

app.callback(
    Output("followUpModal", "is_open"),
    Input("followUpButton", "n_clicks"),
    State("followUpModal", "is_open"),
)(toggle_modal)

app.callback(
    Output("settingsModal", "is_open"),
    Input("settingsButton", "n_clicks"),
    State("settingsModal", "is_open"),
)(toggle_modal)

app.callback(
    Output("taskListModal", "is_open"),
    Input("taskListButton", "n_clicks"),
    State("taskListModal", "is_open"),
)(toggle_modal)

#Hiding Sections

app.callback(
    Output("HearingTestContainer", "style"),
    Input("HearingTestDropdown", "value")
)(unhide)

app.callback(
    Output("HearingAidContainer", "style"),
    Input("HearingAidDropdown", "value")
)(unhide)

app.callback(
    Output("PurchaseDateContainer", "style"),
    Input("ClientPurchaseDropdown", "value")
)(unhide)

#Button should be desiabled until items are filled

#Populates Clientdatabase with all information
#Expand Outputs to ensure form clears when pressed
#Add client id number
#Filter output none to other sections of database
#Should check if information is already in database, and display toast that client already exists

@app.callback(
    Output("ClientConfirmToast", "is_open"),
    Output("ClientFirstName","value"),
    Output("ClientLastName","value"),
    Output("ClientEmail","value"),
    Output("ClientPhone","value"),
    Output("ClientAddress","value"),
    Output("ClientPostalCode","value"),
    Output("ClientCity","value"),
    Output("ClientProvince","value"),

    State("ClientFirstName","value"),
    State("ClientLastName","value"),
    State("ClientEmail","value"),
    State("ClientPhone","value"),
    State("ClientAddress","value"),
    State("ClientPostalCode","value"),
    State("ClientCity","value"),
    State("ClientProvince","value"),
    State("ClientHealthCard","value"),
    State("ClientDateVisit","date"),
    State("ClientFollowup","date"),
    State("HearingAidDropdown","value"),
    State("ClientModel","value"),
    State("ClientPurchaseDropdown","value"),
    State("ClientHearingAidPurchase","date"),
    State("HearingTestDropdown","value"),
    State("ClientHearingTest","date"),
    State("ClientNotesText","value"),

    Input("ClientConfirm", "n_clicks")
)
#Problem with SQL is uniqueness needs a key
def ConfirmClient(firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes,clicks):
    #print(firstname,lastname,email,phone,address,postal,city,province)
    #print(clicks)
    if firstname == None and lastname == None:
        print('No data to input')
        return False,None,None,None,None,None,None,None,None
    
    #information should be cleaned here
    #if hearing aid = No then model = None and date = None
    clientlist = [(firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes)]
    db_file = 'database.db'
    if checkfile('database.db'):
        print('Database exists')
        with sqlite3.connect(db_file) as conn:
            print('name: '+ firstname)
            print('lastname: ' +lastname)
            conn.executemany("insert into clients values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",clientlist)
    else:
        schema_file = 'schema.sql'
        with open(schema_file,'r') as rf:
            schema = rf.read()
        with sqlite3.connect(db_file) as conn:
            conn.executescript(schema)
            conn.executemany("insert into clients values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",clientlist)

        #firstname, lastname, email, homeaddress, postalcode, city, province, healthcard, datevisit, datefollowup, hearingaid, hearingaidmodel, hearingaidpurchaseprosound, hearingtest, datetest, notes
    return True,None,None,None,None,None,None,None,None

#Populates Dropdown with all client Information
@app.callback(
    Output("ClientSelectDropdown", "options"),
    Input("ClientSelectDropdown", "search_value")
    )
def GetClients(value):
    print(value)
    if value == None:
        return []
    matchinglist=[]
    db_file = 'database.db'
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                   select * from clients
                   """)
        for row in cursor.fetchall():
            firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes = row
            if firstname == None:
                pass
            else: 
                #value in firstname or lastname:
                matchinglist.append(firstname + ' ' + lastname)
    return matchinglist

#Input match 

@app.callback(
    Output({"type": "task", "index": '1'},"value"),
    Output("completedTaskContainer","children"),
    State("completedTaskContainer","children"),
    State({"type": "task", "index": "1"},"value"),
    Input({"type": "task-checkbox", "index": "1"},"value")
)

def completeTask(completedtasks,task,checkbox):
    if checkbox == True:
        inputMethod = ctx.triggered_id
        number = inputMethod["index"]
        completedtask = dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText(
                    dbc.Checkbox(id={"type": "completedtask-checkbox", "index": number},value=True,disabled=True)
                ),
                dbc.Input(id={"type": "completedtask", "index": number},value=task,disabled=True)
            ])
        ])
        completedtasks.append(completedtask)
        return None,completedtasks
    return None,completedtasks

#Display Customer Info

@app.callback(
    Output('changeFirstName',"value"),
    Input("ClientSelectDropdown","value")
)

def displaydata(client):
    print("client",client)
    if client == None:
        return None
    clientlist = client.split(" ")
    print("clientlist", clientlist)
    db_file = 'database.db'
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                   select * from clients
                   """)
        for row in cursor.fetchall():
            firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes = row
            if firstname == clientlist[0]:
                print(firstname)
                return firstname
            


""" app.callback(
    Output({'type':'stock-input','index':'CAD'},'valid'),
    Output({'type':'stock-input','index':'CAD'},'invalid'),
    Input({'type':'stock-input','index':'CAD'},'value')
)(checkvalid) """

#Adds to stocks to Table

""" @app.callback(
    Output({'type':'datatable','index':MATCH},'data'),
    Output({'type':'datatable','index':MATCH},'tooltip_data'),
    Input({'type':'stock-confirm','index':MATCH},'n_clicks'),
    Input({'type':'interval','index':MATCH},'n_intervals'),
    State({'type':'datatable','index':MATCH},'data'),
    State({'type':'datatable','index':MATCH},'tooltip_data'),
    State({'type':'stock-input','index':MATCH},'value'),
    State({'type':'amount-input','index':MATCH},'value'),
    State({'type':'price-input','index':MATCH},'value'),
    prevent_initial_call=True
)

def addToTable(clicks,intervals,data,tooltips,ticker,amount,price):
    inputMethod = ctx.triggered_id
     
        return data,tooltips """


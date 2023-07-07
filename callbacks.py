from hashlib import new
from tkinter import Y
from weakref import ref
from dash import Output,Input,MATCH,State,ctx,dcc,ALL
import dash_bootstrap_components as dbc
import pandas as pd
from App import app
from datetime import date,datetime
from functions import *
import plotly.graph_objects as go
import sqlite3
from dash.exceptions import PreventUpdate

#Modal Toggles

app.callback(
    Output("ClientModal", "is_open"),
    Input("ClientButton", "n_clicks"),
    State("ClientModal", "is_open"),
)(toggle_modal)

app.callback(
    Output("hearingAidModal", "is_open"),
    Input("ClientAddHearingAid", "n_clicks"),
    State("hearingAidModal", "is_open"),
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

# TEMPORARILY DISABLED
#change so that state of previous div changeHearingAidPurchaseDiv effects current
# app.callback(
#     Output("changePaymentDiv", "style"),
#     Input("changePaid", "value")
# )(unhide)

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

    State("ClientNumber","value"),
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
def ConfirmClient(clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes,clicks):
    #Filters out pay information
    if firstname == None and lastname == None:
        print('No data to input')
        return False,None,None,None,None,None,None,None,None
    
    #information should be cleaned here
    #if hearing aid = No then model = None and date = None

    #makes list of all data
    clientlist = [(clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes)]
    db_file = 'database.db'

    if createDatabase():
        with sqlite3.connect(db_file) as conn:
            conn.executemany("insert into clients values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",clientlist)
            return True,None,None,None,None,None,None,None,None

    #checks if database file exists
    """ if checkfile('database.db'):
        print('Database exists')
        with sqlite3.connect(db_file) as conn:
            #print('name: '+ firstname)
            #print('lastname: ' +lastname)
            conn.executemany("insert into clients values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",clientlist)
    else:  
        #creates database file using sql schema
        schema_file = 'ClientSchema.sql'
        with open(schema_file,'r') as rf:
            schema = rf.read()
        with sqlite3.connect(db_file) as conn:
            conn.executescript(schema)
            conn.executemany("insert into clients values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",clientlist) """

        #firstname, lastname, email, homeaddress, postalcode, city, province, healthcard, datevisit, datefollowup, hearingaid, hearingaidmodel, hearingaidpurchaseprosound, hearingtest, datetest, notes
    return False,None,None,None,None,None,None,None,None

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
            clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes = row
            if firstname == None:
                pass
            else: 
                #value in firstname or lastname:
                matchinglist.append(firstname + ' ' + lastname)
    return matchinglist

#Input match 
#Tasks completed
#Output Store, Input all, state all?
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
    Output('changeID','value'),
    Output('changeFirstName',"value"),
    Output('changeLastName',"value"),
    Output('changeEmail',"value"),
    Output('changePhoneNumber',"value"),
    Output('changeAddress',"value"),
    Output('changePostalCode',"value"),
    Output('changeCity',"value"),
    Output('changeProvince',"value"),
    Output('changeHealthCard',"value"),
    Output('changeNotes',"value"),
    Input("ClientSelectDropdown","value")
)

def displaydata(client):
    """Gets and displays a clients data"""
    if client == None:
        return None,None,None,None,None,None,None,None,None,None,None
    clientlist = client.split(" ")
    clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,clientnotes = getClient(clientlist[0],clientlist[1])
    return clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,clientnotes

    #print("clientlist", clientlist)
    # db_file = 'database.db'
    # with sqlite3.connect(db_file) as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("""
    #                select * from clients
    #                """)
    #     for row in cursor.fetchall():
    #         clientnum, firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes = row
    #         if firstname == clientlist[0]:
    #             #print(firstname)
    #             return clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,clientnotes
            
@app.callback(
    Output('ClientUpdateToast','is_open'),
    Input('changeClientInfo','n_clicks'),
    State('changeID','value'),
    State('changeFirstName',"value"),
    State('changeLastName',"value"),
    State('changeEmail',"value"),
    State('changePhoneNumber',"value"),
    State('changeAddress',"value"),
    State('changePostalCode',"value"),
    State('changeCity',"value"),
    State('changeProvince',"value"),
    State('changeHealthCard',"value"),
    State('changeNotes',"value"),
)

def updateDatabase(clicks,ID,first,last,emailad,phone,address,postal,cit,prov,health,notes):
    if ID == None:
        return False
    else:
        ID = str(ID)
    db_file = 'database.db'
    if checkfile(db_file):
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            #Gets current info, not sure why we would do this
            #cursor.execute(" SELECT * FROM clients WHERE clientid = " + ID)
            #clientnum, oldfirst,oldname,oldemail,oldphone,oldaddress,oldpostal,oldcity,oldprovince,oldhealth,olddov,oldfollowup,oldhasHearingAid,oldhearingAidModel,oldProsoundPurchase,oldProsoundpurchasedate,oldhasHearingTestdate,oldHearingtestdate,oldnotes = cursor.fetchall()[0]
            #print('old notes', oldnotes)
            #print('new notes', notes)

            updatedata = (first,last,emailad,phone,address,postal,cit,prov,health,notes)
            cursor.execute("UPDATE clients SET firstname = ? ,lastname = ?,email = ?,phonenumber = ?,homeaddress = ?,postalcode = ?,city = ?,province = ?,healthcard = ?,notes =? WHERE clientid = " +ID,updatedata)
    
            #  datevisit, datefollowup, hearingaid, hearingaidmodel, hearingaidpurchaseprosound, hearingaidpurchasedate, hearingtest, datetest,
    return True

@app.callback(
    Output('ClientNumber',"value"),
    Input("ClientButton","n_clicks")
)

def getClientNum(clicks):
    #Make Database here
    db_file = 'database.db'
    if checkfile(db_file):
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    select * from clients
                    """)
            for row in cursor.fetchall():
                clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes = row
        return clientnum+1
    else:  
        #creates database file using sql schema
        schema_file = 'ClientSchema.sql'
        with open(schema_file,'r') as rf:
            schema = rf.read()
        with sqlite3.connect(db_file) as conn:
            conn.executescript(schema)
        return 100

@app.callback(
    Output('FollowUpsContainer',"children"),
    Input("followUpButton","n_clicks"),
    Input('FollowUpSettings','value')
)

def populateFollowUps(clicks,setting):
    #Makes a date to compare to, if ccompare date = actual follow up
    #or if compare date is smaller than actual follow up
    #print(setting)
    today = date.today()

    outputlist = []

    clientlist = getAllClients()
    for client in clientlist:
        clientnum, tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes = client
        date_object = datetime.strptime(followupdate, '%Y-%m-%d').date()
        comparedate = generateDate(date_object,setting)
        #print('last followed up:',date_object)
        #print('date when follow up should happen:', date_object+relativedelta(months=+3))
        #print('date when follow up is calculated:', comparedate)
        if comparedate <= today:
            newrow = dbc.Row([
                dbc.Col([dbc.Label(tablefirstname)],width=1),
                dbc.Col([dbc.Label(tablelastname)],width=1),
                dbc.Col([dbc.Label(email)],width=4),
                dbc.Col([dbc.Label(phone)],width=4),
                dbc.Col([
                    dbc.Button(id={'type':'followButton','index':clientnum},n_clicks=0,children=["Followed Up"])
                ],width=2),
            ],id={'type':'followClientRow','index':clientnum},style={'margin-bottom':'10px'})
            outputlist.append(newrow)
    return outputlist

@app.callback(
    Output({'type':'followClientRow','index':MATCH},"style"),
    Input({'type':'followButton','index':MATCH},"n_clicks"),
    prevent_initial_call=True
)

def clientFollowUp(clicks):
    trigger = ctx.triggered_id
    clinum = trigger['index']
    updated = updateClientbyNum(clinum)
    if updated:
        return {'display':'None'}
    else:
        return {'display':'flex'}
    
#Displays how many follow ups
@app.callback(
    Output('followUpBadge',"children"),
    Input({'type':'followButton','index':ALL},"children")
)

def clientFollowUp(children):
    #print(children,len(children))
    return str(len(children))
    
#TEMPORARILY DISABLED, add back ,style={'display':'None'}
#Display Hearing Aid Purchase     
# @app.callback(
#     Output('changeHearingAidPurchaseDiv',"style"),
#     Input("changeAppointmentType","value"))

# def UnhideHearingAidPurchase(appointmentlist):
#     #print(appointmentlist)
#     if appointmentlist == [] or appointmentlist == None:
#         #print("empty list")
#         return {'display':'None'}
#     for typeappt in appointmentlist:
#         #print(typeappt)
#         if typeappt == "Hearing Aid Purchase":
#             #print("yes")
#             return {'display':'flex'}
#     return {'display':'None'}

#
#
#Notes
#
#
#1. Should make an initalizer to make the database, Client and Payment tables
#2. Should add functionality to update information
#2.5 Should add filter functionality to allow multiple things to be searched
#3. Buttons should be dyamic and only be accessed when information is avaliable














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


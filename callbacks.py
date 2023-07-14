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

""" app.callback(
    Output("HearingAidContainer", "style"),
    Input("HearingAidDropdown", "value")
)(unhide) """

""" app.callback(
    Output("PurchaseDateContainer", "style"),
    Input("ClientPurchaseDropdown", "value")
)(unhide) """

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
    #Wiping Client Modal
    Output("ClientFirstName","value"),
    Output("ClientLastName","value"),
    Output("ClientEmail","value"),
    Output("ClientPhone","value"),
    Output("ClientAddress","value"),
    Output("ClientPostalCode","value"),
    Output("ClientCity","value"),
    Output("ClientProvince","value"),
    Output("ClientHealthCard","value"),
    Output("ClientDateVisit","date"),
    Output("ClientFollowup","date"),
    Output("HearingTestDropdown","value"),
    Output("ClientHearingTest","date"),
    Output("ClientNotesText","value"),
    #Wiping Hearing Aid Modal
    Output('HearingAidInvoiceNumber',"value"),
    Output("ClientHearingAidManufacturer","value"),
    Output('ClientHearingAidModel',"value"),
    Output('ClientHearingAidType',"value"),
    Output('HearingAidLSerialNumber',"value"),
    Output('HearingAidRSerialNumber',"value"),
    Output('HearingAidPaidInvoice',"value"),
    Output("ClientHearingAidPurchase","date"),
    Output('HearingAidPaymentAmount',"value"),
    #Getting Client Info
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
    State("HearingTestDropdown","value"),
    State("ClientHearingTest","date"),
    State("ClientNotesText","value"),
    #Getting Hearing Aid Modal
    State('HearingAidInvoiceNumber',"value"),
    State("ClientHearingAidManufacturer","value"),
    State('ClientHearingAidModel',"value"),
    State('ClientHearingAidType',"value"),
    State('HearingAidLSerialNumber',"value"),
    State('HearingAidRSerialNumber',"value"),
    State('HearingAidPaidInvoice',"value"),
    State("ClientHearingAidPurchase","date"),
    State('HearingAidPaymentAmount',"value"),
    #Button Press Input
    Input("ClientConfirm", "n_clicks")
)
def ConfirmClient(clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,hearingAidInvoice,hearingAidManufacture,hearingAidModel,hearingAidType,LSerial,RSerial,hearinghaspaid,Prosoundpurchasedate,hearingpaidamount,clicks):
    #Filters out pay information
    today = date.today()
    if firstname == None and lastname == None:
        #print('No data to input')
        return False,None,None,None,None,None,None,None,None,None,today,today,None,today,None,None,None,None,None,None,None,None,today,None
    
    #information should be cleaned here
    #if hearing aid = No then model = None and date = None

    #makes list of all data
    clientlist = [(clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,True)]
    hearingaidlist= [(hearingAidInvoice,clientnum,hearingAidManufacture,hearingAidModel,hearingAidType,LSerial,RSerial,hearinghaspaid,Prosoundpurchasedate,hearingpaidamount)]
    #hearingAidModel,Prosoundpurchasedate,
    db_file = 'database.db'

    if createDatabase():
        with sqlite3.connect(db_file) as conn:
            conn.executemany("insert into clients values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",clientlist)
            conn.executemany("insert into sales values (?,?,?,?,?,?,?,?,?,?)",hearingaidlist)
            return True,None,None,None,None,None,None,None,None,None,today,today,None,today,None,None,None,None,None,None,None,None,today,None

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
    return False,None,None,None,None,None,None,None,None,None,today,today,None,today,None,None,None,None,None,None,None,None,today,None

#Populates Dropdown with all client Information
@app.callback(
    Output("ClientSelectDropdown", "options"),
    Input("ClientSelectDropdown", "search_value")
    )
def GetClients(value):
    #print(value)
    if value == None:
        return []
    matchinglist=[]
    allclients = getAllClients()
    for row in allclients:
        clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status = row
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

#Display Customer Info in section

@app.callback(
    #Top Information
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
    Output('changeVisitDate',"date"),
    Output('changeFollowDate',"date"),
    Output('changeNotes',"value"),
    #Bottom information
    Output('changeHearingAidMake','value'),
    Output('changeHearingAidModel',"value"),
    Output('changeHearingAidType',"value"),
    Output('changeHearingAidLSerial',"value"),
    Output('changeHearingAidRSerial',"value"),
    Output('changePaid',"value"),
    Output('changeInvoiceNumber',"value"),
    Output('changeInvoiceAmount',"value"),
    Output('changePaymentDate',"date"),
    Input("ClientSelectDropdown","value")
)

def displaydata(client):
    """Gets and displays a clients data"""
    today = date.today()
    if client == None:
        return None,None,None,None,None,None,None,None,None,None,today,today,None,None,None,None,None,None,None,None,None,today
    clientlist = client.split(" ")
    clientnum, firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status = getClient(clientlist[0],clientlist[1])
    saleslist = getSalesByClient(clientnum)
    if saleslist == []:
        return clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,dateofvisit,followupdate,clientnotes,None,None,None,None,None,None,None,None,today
    else:
        print(saleslist)
        Invoice,clientnumber,Make,Model,Type,Lserial,Rserial,dispensdate,Paid,Date,Amount,status = saleslist[0]
        #No Type
        return clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,clientnotes,Make,Model,Type,Lserial,Rserial,Paid,Invoice,Amount,Date

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
    if createDatabase():
        allclients = getAllClients()
        #print('allclients: ',allclients)
        if allclients == []:
            return 100
        else:
            for row in allclients:
                clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status = row
                #hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,
            return clientnum+1
    """ else:  
        #creates database file using sql schema
        schema_file = 'ClientSchema.sql'
        with open(schema_file,'r') as rf:
            schema = rf.read()
        with sqlite3.connect(db_file) as conn:
            conn.executescript(schema)
        return 100 """

@app.callback(
        Output('HearingAidClientIDNumber','value'),
        Input('ClientNumber',"value"),
)
def updateClientNumberHearingAid(num):
    return num

@app.callback(
    Output('FollowUpsContainer',"children"),
    Input("followUpButton","n_clicks"),
    Input('FollowUpSettings','value'),
    Input('FollowUpSettingsPayment','value'),
    Input('FollowUpSettingsHearing','value'),
    Input('FollowUpSettingsTest','value'),
    
)

def populateFollowUps(clicks,routsetting,paysetting,hearsetting,testsetting):
    #Makes a date to compare to, if ccompare date = actual follow up
    #or if compare date is smaller than actual follow up
    #print(setting)
    today = date.today()

    settingsfollowup = []
    paymentfollowup = []
    hearingaidfollowup=[]
    testfollowup = []

    try:
        clientlist = getAllClients()
        if clientlist == []:
            return []
        for client in clientlist:
            clientnum, tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status = client

            #Prevent Closed clients from being followed up
            if status == 'closed':
                pass

            saleslist = getSalesByClient(clientnum)
            if saleslist == []:
                payDate = date(2099,12,30)
                Paid = True
                Make = None
                Model = None
            else:
                for sale in saleslist:
                    Invoice,clientnumber,Make,Model,Type,Lserial,Rserial,dispensedate,Paid,payDate,Amount,aidstat = sale
                    if Invoice is not None and Paid == "Yes" and Amount is not None:
                        pass
                    else:
                        Invoice,clientnumber,Make,Model,Type,Lserial,Rserial,Paid,payDate,Amount = sale

            #,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate
            date_object = datetime.strptime(followupdate, '%Y-%m-%d').date()
            testobject = datetime.strptime(Hearingtestdate, '%Y-%m-%d').date()
            payobject = datetime.strptime(payDate, '%Y-%m-%d').date()
            
            routcomparedate = generateDate(date_object,routsetting)
            testcomparedate = generateDate(testobject,testsetting)
            paycomparedate = generateDate(payobject,paysetting)
            hearcomparedate = generateDate(date_object,hearsetting)

            #print('last followed up:',date_object)
            #print('date when follow up should happen:', date_object+relativedelta(months=+3))
            #print('date when follow up is calculated:', comparedate)
            if routcomparedate <= today:
                newrow = dbc.Row([
                    dbc.Col([dbc.Label(tablefirstname)],width=1),
                    dbc.Col([dbc.Label(tablelastname)],width=1),
                    dbc.Col([dbc.Label(email)],width=3),
                    dbc.Col([dbc.Label(phone)],width=3),
                    dbc.Col([dbc.Badge("Routine Follow Up",id={'type':'followUpBadge','index':clientnum},color="primary", text_color="white",pill=True, className="ms-1")],width=2),
                    dbc.Col([
                        dbc.Button(id={'type':'followButton','index':clientnum},n_clicks=0,children=["Followed Up"])
                    ],width=2),
                ],id={'type':'followClientRow','index':clientnum},style={'margin-bottom':'10px'})
                settingsfollowup.append(newrow)
            elif paycomparedate <= today and Paid == 'No':
                newrow = dbc.Row([
                    dbc.Col([dbc.Label(tablefirstname)],width=1),
                    dbc.Col([dbc.Label(tablelastname)],width=1),
                    dbc.Col([dbc.Label(email)],width=3),
                    dbc.Col([dbc.Label(phone)],width=3),
                    dbc.Col([dbc.Badge("Payment Follow",id={'type':'followUpBadgePay','index':clientnum},color="danger", text_color="primary",pill=True, className="ms-1")],width=2),
                    dbc.Col([
                        dbc.Button(id={'type':'followButton','index':clientnum},n_clicks=0,children=["Followed Up"])
                    ],width=2),
                ],id={'type':'followClientRow','index':clientnum},style={'margin-bottom':'10px'})
                paymentfollowup.append(newrow)
            elif hearcomparedate <= today and Paid == 'No':
                newrow = dbc.Row([
                    dbc.Col([dbc.Label(tablefirstname)],width=1),
                    dbc.Col([dbc.Label(tablelastname)],width=1),
                    dbc.Col([dbc.Label(email)],width=3),
                    dbc.Col([dbc.Label(phone)],width=3),
                    dbc.Col([dbc.Badge("Hearing Aid Follow",id={'type':'followUpBadgeHear','index':clientnum},color="blue", text_color="white",pill=True, className="ms-1")],width=2),
                    dbc.Col([
                        dbc.Button(id={'type':'followButton','index':clientnum},n_clicks=0,children=["Followed Up"])
                    ],width=2),
                ],id={'type':'followClientRow','index':clientnum},style={'margin-bottom':'10px'})
                hearingaidfollowup.append(newrow)
            elif testcomparedate <= today:
                print('compare date: ', testcomparedate)
                print('today: ', today)
                newrow = dbc.Row([
                    dbc.Col([dbc.Label(tablefirstname)],width=1),
                    dbc.Col([dbc.Label(tablelastname)],width=1),
                    dbc.Col([dbc.Label(email)],width=3),
                    dbc.Col([dbc.Label(phone)],width=3),
                    dbc.Col([dbc.Badge("Hearing Test Follow",id={'type':'followUpBadgeTest','index':clientnum},color="green", text_color="primary",pill=True, className="ms-1")],width=2),
                    dbc.Col([
                        dbc.Button(id={'type':'followButton','index':clientnum},n_clicks=0,children=["Followed Up"])
                    ],width=2),
                ],id={'type':'followClientRow','index':clientnum},style={'margin-bottom':'10px'})
                testfollowup.append(newrow)
            else:
                pass
            outputlist = paymentfollowup+hearingaidfollowup+testfollowup+settingsfollowup
        return outputlist
    except Exception as EGC:
        print('Populate FollowUps Error: ' + EGC)
        return None

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

@app.callback(
    Output('ClientUploadConfirm',"is_open"),
    Input('ClientsUpload',"contents")
)

def uploadclients(contents):
    if contents is None:
        return False
    dataframe = readExcel(contents)
    print('worked')
    print(dataframe)
    return True

#UPLOAD PRICING INFORMATION TO THE DATABASE

@app.callback(
    Output('DataUploadConfirm',"is_open"),
    Input('DataUpload',"contents")
)
    
def dataUpload(contents):
    if contents is None:
        return False
    else:
        dataframe = readExcel(contents)
        cnx = sqlite3.connect('database.db')
        dataframe.to_sql(name='MSRP',con=cnx,if_exists="append",index=False)
        return True
    
#FIND HEARING AID TYPE FROM DATABASE
@app.callback(
    Output("changeHearingAidType", "options"),
    Input("changeHearingAidModel", "value")
    )

def findType(Model):
    if Model == None:
        return []
    db_file = 'database.db'
    Outputlist=[]
    if createDatabase():
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM MSRP")
            listmodel = cursor.fetchall()
            for hearingaid in listmodel:
                man,make,typ,price = hearingaid
                if Model == make:
                    if make not in Outputlist:
                        Outputlist.append(typ)
            return Outputlist

#FIND HEARING AID MODEL FROM DATABASE
@app.callback(
    Output("changeHearingAidModel", "options"),
    Input("changeHearingAidMake", "value")
    )

def findMake(manuf):
    if manuf == None:
        return []
    db_file = 'database.db'
    Outputlist=[]
    if createDatabase():
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM MSRP")
            listmodel = cursor.fetchall()
            for hearingaid in listmodel:
                man,make,typ,price = hearingaid
                if manuf == man:
                    if make not in Outputlist:
                        Outputlist.append(make)
            return Outputlist


            #Gets current info, not sure why we would do this
            #cursor.execute(" SELECT * FROM clients WHERE clientid = " + ID)

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
#4. Add in a way to port prices and clients from excel
#5. Add in multiple followup options and pills to display tags for each one
#6. Add in closed client status
#7. Add in cost part to calulate profit, must be done by time
#8. Add in Client import feature
#9. Add in how new hearing aid data can be added














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


from dash import Output,Input,MATCH,State,ctx,dcc,ALL
import dash_bootstrap_components as dbc
import pandas as pd
from App import app
from datetime import date,datetime
from functions import *
import plotly.graph_objects as go
import sqlite3
import hashlib
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

#Unhiding Client Full View Section

@app.callback(
    Output("ClientContainer",'style'),
    Input("ClientSelectDropdown",'value')
)
def unhideUpdateClient(value):
    if value == None:
        return {'display':'None'}
    else:
        return {'display':'block'}

#Displays payment Section in Full View

app.callback(
    Output('changePaymentDiv', "style"),
    Input('changePaid', "value")
)(unhide)

#Displays Hearing Aid Section in Full View

@app.callback(
    Output("changeHearingAidPurchaseDiv", "style"),
    Input("changeAppointmentType", "value")
)
def DisplayHearingAidFullView(value):
    if value == [] or value == None:
        return {'display':'None'}
    if "Hearing Aid Dispensing" in value or "Hearing Aid Purchase" in value:
        return {'display':'block'}
    else:
        return {'display':'None'}

#Login Callback
@app.callback(
    Output("loginModal", "is_open"),
    Output("loginToast", "is_open"),
    Output("memory-output","data"),
    Input("signInButton", "n_clicks"),
    State('usernameEnter','value'),
    State('passwordEnter','value'),
)
def Login(clicks,username,password):
    if username == None or password == None:
        return True,False,None
        
    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM userdata WHERE username=? AND password = ?",(hashInput(username),hashInput(password)))

    line = cur.fetchall()

    #State('passwordEnter','value'),
    #State("memory-output","data"),

    if line:
        #print(line)
        id, us, pw, databasefile, keyfile = line[0]
        
        databasefile = decrypt('Data/configs/main.pkl',hashInput('UekiJW^209*$3D4'),databasefile)
        keyfile = decrypt('Data/configs/main.pkl',hashInput('UekiJW^209*$3D4'),keyfile)

        #print(databasefile,keyfile)
        print('Login Successful')
        return False,False,[databasefile,keyfile]
    else:
        return True,True,None

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
    Output('ClientHearingAidQuantity',"value"),
    Output('ClientHearingAidStatus',"value"),
    Output("ClientHearingAidDispenseDate","date"),
    Output('ClientHearingAidMSRP',"value"),
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
    State('ClientHearingAidQuantity',"value"),
    State('ClientHearingAidStatus',"value"),
    State("ClientHearingAidDispenseDate","date"),
    State('ClientHearingAidMSRP',"value"),
    #SECURITY FEATURES
    State('passwordEnter','value'),
    State("memory-output","data"),
    #Button Press Input
    Input("ClientConfirm", "n_clicks")
)
def ConfirmClient(clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,hearingAidInvoice,hearingAidManufacture,hearingAidModel,hearingAidType,LSerial,RSerial,hearinghaspaid,Prosoundpurchasedate,hearingpaidamount,quan,aidstatus,dispensedate,msrp,password,memory,clicks):
    #Filters out pay information
    today = date.today()
    if firstname == None and lastname == None:
        return False,None,None,None,None,None,None,None,None,None,today,today,None,today,None,None,None,None,None,None,None,None,today,None,None,None,today,None
    
    #print(memory)

    #information should be cleaned here
    #if hearing aid = No then model = None and date = None

    db_file = memory[1]
    keyfile = memory[0]

    #makes list of all data and encrypts
    clientlist = [(clientnum,firstname,lastname,encrypt(keyfile,password,email),encrypt(keyfile,password,phone),encrypt(keyfile,password,address),encrypt(keyfile,password,postal),encrypt(keyfile,password,city),encrypt(keyfile,password,province),encrypt(keyfile,password,healthcard),encrypt(keyfile,password,dateofvisit),encrypt(keyfile,password,followupdate),encrypt(keyfile,password,hasHearingTestdate),encrypt(keyfile,password,Hearingtestdate),encrypt(keyfile,password,clientnotes),encrypt(keyfile,password,'Open'))]    
    if hearingAidInvoice != None:
        hearingaidlist= [(hearingAidInvoice,clientnum,encrypt(keyfile,password,hearingAidManufacture),encrypt(keyfile,password,hearingAidModel),encrypt(keyfile,password,hearingAidType),encrypt(keyfile,password,LSerial),encrypt(keyfile,password,RSerial),encrypt(keyfile,password,dispensedate),encrypt(keyfile,password,hearinghaspaid),encrypt(keyfile,password,Prosoundpurchasedate),encrypt(keyfile,password,hearingpaidamount),encrypt(keyfile,password,aidstatus),encrypt(keyfile,password,quan),encrypt(keyfile,password,msrp))]
    else:
        hearingaidlist = [()]
    #Encrypts Data

    

    #clientlist = encryptTuple(keyfile,hashInput(password),clientlist)
    #hearingaidlist = encryptTuple(keyfile,hashInput(password),hearingaidlist)
    

    if createDatabase(db_file):
        with sqlite3.connect(db_file) as conn:
            conn.executemany("insert into clients values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",clientlist)
            if hearingAidInvoice != None:
                conn.executemany("insert into sales values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",hearingaidlist)
            return True,None,None,None,None,None,None,None,None,None,today,today,None,today,None,None,None,None,None,None,None,None,today,None,None,None,today,None

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
    return False,None,None,None,None,None,None,None,None,None,today,today,None,today,None,None,None,None,None,None,None,None,today,None,None,None,today,None

#Populates Dropdown with all client Information
@app.callback(
    Output("ClientSelectDropdown", "options"),
    Input("ClientSelectDropdown", "search_value"),
    State("memory-output","data")
    )

def GetClients(value,memory):
    #print(value)

    if value == None:
        return []
    
    dbfile = memory[1]

    matchinglist=[]
    allclients = getAllClients(dbfile)
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

#Display Customer Info in Full View

@app.callback(
    #Top Information
    Output('changeID','value'),
    Output('changeFirstName',"value"),
    Output('changeLastName',"value"),
    Output('changeStatus','value'),
    Output('changeEmail',"value"),
    Output('changePhoneNumber',"value"),
    Output('changeAddress',"value"),
    Output('changePostalCode',"value"),
    Output('changeCity',"value"),
    Output('changeProvince',"value"),
    Output('changeHealthCard',"value"),
    Output('changeVisitDate',"date"),
    Output('changeFollowDate',"date"),
    #Should add test date
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
    Output('changeAidStatus',"value"),
    Output('changeDispenseDate',"date"),
    Output('changeQuan',"value"),
    Output('changeMSRP',"value",allow_duplicate=True),
    Input("ClientSelectDropdown","value"),
    #SECURITY FEATURES
    State('passwordEnter','value'),
    State("memory-output","data"),
    prevent_initial_call=True
)

def displaydata(client,password,memory):
    """Gets and displays a clients data"""
    today = date.today()
    if client == None:
        return None,None,None,None,None,None,None,None,None,None,None,today,today,None,None,None,None,None,None,None,None,None,today,None,today,None,None
    clientlist = client.split(" ")

    keyfile = memory[0]
    db = memory[1]

    clientnum, firstname,lastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status = getClient(clientlist[0],clientlist[1],db,keyfile,password)
    saleslist = getSalesByClient(clientnum,db)

    #Decrypting Customer Data
    email = decrypt(keyfile,password,email)
    phone = decrypt(keyfile,password,phone)
    address = decrypt(keyfile,password,address)
    postal = decrypt(keyfile,password,postal)
    city = decrypt(keyfile,password,city)
    province = decrypt(keyfile,password,province)
    healthcard = decrypt(keyfile,password,healthcard)
    dateofvisit = decrypt(keyfile,password,dateofvisit)
    followupdate = decrypt(keyfile,password,followupdate)
    clientnotes = decrypt(keyfile,password,clientnotes)
    status = decrypt(keyfile,password,status)

    """ email = decrypt(keyfile,password,email)
    email = decrypt(keyfile,password,email)
    email = decrypt(keyfile,password,email)
    """

    #CHECKS IF THERE IS ANYTHING IN SALES LIST
    if saleslist == []:
        return clientnum,firstname,lastname,status,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,clientnotes,None,None,None,None,None,None,None,None,today,None,today,None,None
    else:
        #DECIDES WHICH SALE IS DIPLAYED
        #Sets inital Values
        Invoice,clientnumber,Make,Model,Typea,Lserial,Rserial,dispensdate,Paid,Date,Amount,aidstatus,quan,msrp = saleslist[0]
        aidstatus = decrypt(keyfile,password,aidstatus)
        for sale in saleslist:
            #Gets values of each Sale
            newInvoice,newclientnumber,newMake,newModel,newTypea,newLserial,newRserial,newdispensdate,newPaid,newDate,newAmount,newaidstatus,newquan,newmsrp = sale
            newaidstatus = decrypt(keyfile,password,newaidstatus)
            #If a new Sale value = Trying then sets it to main values
            if newaidstatus == "Trying":
                Invoice,clientnumber,Make,Model,Typea,Lserial,Rserial,dispensdate,Paid,Date,Amount,aidstatus,quan,msrp = newInvoice,newclientnumber,newMake,newModel,newTypea,newLserial,newRserial,newdispensdate,newPaid,newDate,newAmount,newaidstatus,newquan,newmsrp 
            else:
                pass
        #checks that if nothing was set to old values then replaces old sale with Nothing
        if aidstatus == "Returned" or aidstatus == "Purchased":
            Invoice,clientnumber,Make,Model,Typea,Lserial,Rserial,dispensdate,Paid,Date,Amount,aidstatus,quan,msrp = None,None,None,None,None,None,None,today,None,today,None,None,None,None
        else:
            Make = decrypt(keyfile,password,Make)
            Model = decrypt(keyfile,password,Model)
            Typea = decrypt(keyfile,password,Typea)
            Lserial = decrypt(keyfile,password,Lserial)
            Rserial = decrypt(keyfile,password,Rserial)
            Paid = decrypt(keyfile,password,Paid)
            dispensdate = decrypt(keyfile,password,dispensdate)
            Date = decrypt(keyfile,password,Date)
            Amount = decrypt(keyfile,password,Amount)
            #aidstatus = decrypt(keyfile,password,aidstatus)
            #`b'gAAAAABkzAlC-XXvWkk0exuorxN6CS_0hUaPOWYV_AyQDArHqNOPUmU1obEeGE5QTAXr5L_MLvER9bRTyzzoGvVHIxzqp6u0_w=='`


            quan = decrypt(keyfile,password,quan)
            msrp = decrypt(keyfile,password,msrp)

        return clientnum,firstname,lastname,status,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,clientnotes,Make,Model,Typea,Lserial,Rserial,Paid,Invoice,Amount,Date,aidstatus,dispensdate,quan,msrp

#Update Database for client in full view  
@app.callback(
    Output('ClientUpdateToast','is_open'),
    Input('changeClientInfo','n_clicks'),
    State('changeID','value'),
    State('changeFirstName',"value"),
    State('changeLastName',"value"),
    State('changeStatus',"value"),
    State('changeEmail',"value"),
    State('changePhoneNumber',"value"),
    State('changeAddress',"value"),
    State('changePostalCode',"value"),
    State('changeCity',"value"),
    State('changeProvince',"value"),
    State('changeHealthCard',"value"),
    State('changeNotes',"value"),
    #Bottom Part
    State('changeInvoiceNumber',"value"),
    State('changeAidStatus',"value"),
    State('changeDispenseDate','date'),
    State('changeQuan','value'),
    State('changeHearingAidMake','value'),
    State('changeHearingAidModel','value'),
    State('changeHearingAidType','value'),
    State('changeHearingAidLSerial','value'),
    State('changeHearingAidRSerial','value'),
    State('changePaid','value'),
    State('changePaymentDate','date'),
    State('changeInvoiceAmount','value'),
    State('changeMSRP','value'),
    State("changeAppointmentType",'value'),
    #SECURITY FEATURES
    State('passwordEnter','value'),
    State("memory-output","data")
)

def updateDatabase(clicks,ID,first,last,status,emailad,phone,address,postal,cit,prov,health,notes,invoicenum,aidstatus,dispensedate,quan,manu,model,typea,lserial,rserial,paidbol,paydate,payamount,msrp,appt,password,memory):
    if ID == None:
        return False
    else:
        ID = str(ID)
    if invoicenum != None:
        invoicenum = str(invoicenum)

    db_file = memory[1]
    keyfile = memory[0]
    if createDatabase(db_file):
        
        
        testlist=["Hearing Test","Hearing Aid Dispensing","Hearing Aid Purchase","Ear Cleaning"]
        #appt can be a list
        

        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            #Gets current info
            cursor.execute(" SELECT * FROM clients WHERE clientid = " + ID)
            clientnum, oldfirst,oldlast,oldemail,oldphone,oldaddress,oldpostal,oldcity,oldprovince,oldhealth,visitdate,followup,testbool,testdate,oldnotes,oldstatus = cursor.fetchall()[0]
            
            print(appt)
            if "Hearing Test" in appt:
                testbool=True
                testdate=date.today()
                visitdate=date.today()
                followup=date.today()
            if "Ear Cleaning" in appt:
                visitdate=date.today()
                followup=date.today()
            if "Hearing Aid Purchase" in appt or "Hearing Aid Dispensing" in appt:
                followup=date.today()
                
                #Has to check if invoice is there
                cursor.execute(" SELECT * FROM sales WHERE invoicenumber = " +invoicenum)
                recieved = cursor.fetchall()
                if recieved == []:
                    salesdata= [(int(invoicenum),int(ID),encrypt(keyfile,password,manu),encrypt(keyfile,password,model),encrypt(keyfile,password,typea),encrypt(keyfile,password,lserial),encrypt(keyfile,password,rserial),encrypt(keyfile,password,dispensedate),encrypt(keyfile,password,paidbol),encrypt(keyfile,password,paydate),encrypt(keyfile,password,payamount),encrypt(keyfile,password,aidstatus),encrypt(keyfile,password,quan),encrypt(keyfile,password,msrp))]
                    conn.executemany("insert into sales values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",salesdata)
                else:
                    salesdata= [ID,encrypt(keyfile,password,manu),encrypt(keyfile,password,model),encrypt(keyfile,password,typea),encrypt(keyfile,password,lserial),encrypt(keyfile,password,rserial),encrypt(keyfile,password,dispensedate),encrypt(keyfile,password,paidbol),encrypt(keyfile,password,paydate),encrypt(keyfile,password,payamount),encrypt(keyfile,password,aidstatus),encrypt(keyfile,password,quan),encrypt(keyfile,password,msrp)]
                    cursor.execute("UPDATE sales SET clientnumber= ?,manufacturer = ?,model = ?,type = ?,Lserialnum = ?,Rserialnum = ?,dispensedate = ?,invoicepaid = ?,paymentdate = ?,paymentamount = ?,status = ?,quantity = ?,msrp =? WHERE invoicenumber = " +invoicenum,salesdata)


            updatedata=[first,last,encrypt(keyfile,password,emailad),encrypt(keyfile,password,phone),encrypt(keyfile,password,address),encrypt(keyfile,password,postal),encrypt(keyfile,password,cit),encrypt(keyfile,password,prov),encrypt(keyfile,password,health),encrypt(keyfile,password,visitdate),encrypt(keyfile,password,followup),encrypt(keyfile,password,testbool),encrypt(keyfile,password,testdate),encrypt(keyfile,password,notes),encrypt(keyfile,password,status)]
            cursor.execute("UPDATE clients SET firstname = ? ,lastname = ?,email = ?,phonenumber = ?,homeaddress = ?,postalcode = ?,city = ?,province = ?,healthcard = ?,datevisit = ?,datefollowup = ?,hearingtest = ?,datetest = ?,notes =?,status=? WHERE clientid = " +ID,updatedata)

            #updatedata = (first,last,emailad,phone,address,postal,cit,prov,health,notes,status)
            #cursor.execute("UPDATE clients SET firstname = ? ,lastname = ?,email = ?,phonenumber = ?,homeaddress = ?,postalcode = ?,city = ?,province = ?,healthcard = ?,notes =?,status=? WHERE clientid = " +ID,updatedata)
    
            #  datevisit, datefollowup, hearingaid, hearingaidmodel, hearingaidpurchaseprosound, hearingaidpurchasedate, hearingtest, datetest,

    return True

#FINDS CLIENT NUMBER AND POPULATES NEW CLIENT

@app.callback(
    Output('ClientNumber',"value"),
    Input("ClientButton","n_clicks"),
    Input("memory-output","data")
)
def clientNumberMask(clicks,memory):
    if memory == None:
        return None
    #print(memory)
    return getClientNum(clicks,memory[1])

#ADD CLIENT NUMBER TO HEARING AID

@app.callback(
        Output('HearingAidClientIDNumber','value'),
        Input('ClientNumber',"value"),
)
def updateClientNumberHearingAid(num):
    return num

#Populates Entire Follow up Modal

@app.callback(
    Output('FollowUpsContainer',"children"),
    Input("followUpButton","n_clicks"),
    Input('FollowUpSettings','value'),
    Input('FollowUpSettingsPayment','value'),
    Input('FollowUpSettingsHearing','value'),
    Input('FollowUpSettingsTest','value'),
    State("memory-output","data"),
    State('passwordEnter','value')
)

def populateFollowUps(clicks,routsetting,paysetting,hearsetting,testsetting,memory,password):
    #Makes a date to compare to, if ccompare date = actual follow up
    #or if compare date is smaller than actual follow up
    #print(setting)
    today = date.today()

    settingsfollowup = []
    paymentfollowup = []
    hearingaidfollowup=[]
    testfollowup = []

    if memory == None:
        return []

    dbfile = memory[1]
    keyfile = memory[0]

    try:
        clientlist = getAllClients(dbfile)
        if clientlist == []:
            return []
        for client in clientlist:
            clientnum, tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status = client

            status = decrypt(keyfile,password,status)

            #Prevent Closed clients from being followed up
            if status == 'closed':
                pass

            saleslist = getSalesByClient(clientnum,dbfile)
            if saleslist == []:
                payDate = date(2099,12,30)
                Paid = True
                Make = None
                Model = None
            else:
                for sale in saleslist:
                    Invoice,clientnumber,Make,Model,Type,Lserial,Rserial,dispensedate,Paid,payDate,Amount,aidstat,quan,msrp = sale

                    Paid = decrypt(keyfile,password,Paid)
                    Amount = decrypt(keyfile,password,Amount)
                    
                    if Invoice is not None and Paid == "Yes" and Amount is not None:
                        pass
                    else:
                        Invoice,clientnumber,Make,Model,Type,Lserial,Rserial,dispensedate,Paid,payDate,Amount,aidstat,quan,msrp = sale
                        Paid = decrypt(keyfile,password,Paid)
                        Amount = decrypt(keyfile,password,Amount)

            followupdate = decrypt(keyfile,password,followupdate)
            Hearingtestdate = decrypt(keyfile,password,Hearingtestdate)
            try:
                dispensedate = decrypt(keyfile,password,dispensedate)
            except:
                #For some reason the dispense date is not encrypted here
                dispensedate = dispensedate

            #,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate
            date_object = datetime.strptime(followupdate, '%Y-%m-%d').date()
            testobject = datetime.strptime(Hearingtestdate, '%Y-%m-%d').date()
            payobject = datetime.strptime(dispensedate, '%Y-%m-%d').date()
            
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
                    dbc.Col([dbc.Label(decrypt(keyfile,password,email))],width=3),
                    dbc.Col([dbc.Label(decrypt(keyfile,password,phone))],width=3),
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
                    dbc.Col([dbc.Label(decrypt(keyfile,password,email))],width=3),
                    dbc.Col([dbc.Label(decrypt(keyfile,password,phone))],width=3),
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
                    dbc.Col([dbc.Label(decrypt(keyfile,password,email))],width=3),
                    dbc.Col([dbc.Label(decrypt(keyfile,password,phone))],width=3),
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
                    dbc.Col([dbc.Label(decrypt(keyfile,password,email))],width=3),
                    dbc.Col([dbc.Label(decrypt(keyfile,password,phone))],width=3),
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

#Hides Clients that have been followed up with

@app.callback(
    Output({'type':'followClientRow','index':MATCH},"style"),
    Input({'type':'followButton','index':MATCH},"n_clicks"),
    State("memory-output","data"),
    State('passwordEnter','value'),
    prevent_initial_call=True
)

def clientFollowUp(clicks,memory,password):
    db = memory[1]
    key = memory[0]

    trigger = ctx.triggered_id
    clinum = trigger['index']

    updated = updateClientbyNum(clinum,db,key,password)
    if updated:
        return {'display':'None'}
    else:
        return {'display':'flex'}
    
#Displays how many follow ups on outside badge
@app.callback(
    Output('followUpBadge',"children"),
    Input({'type':'followButton','index':ALL},"children")
)

def clientFollowUp(children):
    #print(children,len(children))
    return str(len(children))

#UPLOADS CLIENTS IN BATCH LIST (WIP)
#NEEDS ENCRYPTION

@app.callback(
    Output('ClientUploadConfirm',"is_open"),
    Input('ClientsUpload',"contents"),
    State("memory-output","data"),
    State('passwordEnter','value'),
)

def uploadclients(contents,memory,password):
    if contents is None:
        return False
    dataframe = readExcel(contents)

    db = memory[1]
    key = memory[0]

    #Splits Dataframe
    salesdata = dataframe.iloc[:,15:]
    clientdata = dataframe.iloc[:,:15]

    #Creates Client Dataframe
    clientnumber = getClientNum(3,db)

    clientnumberlist = []
    clientnumberlist.append(clientnumber)
    newnumber = clientnumber
    for index in range(len(clientdata)-1):
        newnumber = newnumber+1
        clientnumberlist.append(newnumber)

    clientdata['datevisit'] = clientdata['datevisit'].dt.strftime("%Y-%m-%d")
    clientdata['datefollowup'] = clientdata['datefollowup'].dt.strftime("%Y-%m-%d")
    clientdata['datetest'] = clientdata['datetest'].dt.strftime("%Y-%m-%d")

    #Creates Sales Dataframe
    salesdata.insert(0,'clientnumber',clientnumberlist,True)

    #Drops non invoice sales data
    salesdata.dropna(subset=['invoicenumber'],inplace=True)
    salesdata = salesdata.astype({'invoicenumber':'int'})
    salesdata.rename(columns={'status.1':'status'},inplace=True)
    salesdata['dispensedate'] = salesdata['dispensedate'].dt.strftime("%Y-%m-%d")
    salesdata['paymentdate'] = salesdata['paymentdate'].dt.strftime("%Y-%m-%d")

    #Encrypts dfs
    #sales need to encrypt everything except first two, invoice and client number
    #print('1')
    encSalesDf = salesdata.iloc[:,1:]
    invoicedata = salesdata['invoicenumber']
    clientnumdata = salesdata['clientnumber']
    salesdata = encryptDf(key,password,encSalesDf)
    #print('2')
    salesdata.insert(0,'clientnumber',clientnumdata,True)
    salesdata.insert(0,'invoicenumber',invoicedata,True)

    #clients encrypt everything except first three, client id, firt and last
    #print('3')
    encClientData = clientdata.iloc[:,2:]
    firstname = clientdata['firstname']
    lastname = clientdata['lastname']
    clientdata = encryptDf(key,password,encClientData)
    clientdata.insert(0,'lastname',lastname,True)
    clientdata.insert(0,'firstname',firstname,True)
    clientdata.insert(0,'clientid',clientnumberlist,True)

    #`b'gAAAAABk06cjZpa6ddEa4BOPf-5YqO8lFQeJ6UD6hRs9xKdTAJjsLU2RllfGZEHJjBKuVCbuHNf2uPG4iW9HG1WscbwNSoeAIA=='

    #print('salesdata')
    #print(salesdata)
    #print('clientdata')
    #print(clientdata)

    #Writes to Dataframe
    cnx = sqlite3.connect(db)
    salesdata.to_sql(name='sales',con=cnx,if_exists="append",index=False)
    clientdata.to_sql(name='clients',con=cnx,if_exists="append",index=False)

    return True

#UPLOAD PRICING INFORMATION TO THE DATABASE

@app.callback(
    Output('DataUploadConfirm',"is_open"),
    Input('DataUpload',"contents"),
    State("memory-output","data")
)
    
def dataUpload(contents,memory):
    if contents is None:
        return False
    else:
        db = memory[1]
        today = date.today()
        dataframe = readExcel(contents)
        cnx = sqlite3.connect(db)
        dataframe['dateadded'] = today
        dataframe.to_sql(name='MSRP',con=cnx,if_exists="append",index=False)
        return True
    
#FIND HEARING AID TYPE FROM DATABASE OUTPUT TO FULL VIEW
@app.callback(
    Output("changeHearingAidType", "options"),
    Input("changeHearingAidModel", "value")
)(findType)

#FIND HEARING AID MODEL FROM DATABASE OUTPUT TO FULL VIEW
@app.callback(
    Output("changeHearingAidModel", "options"),
    Input("changeHearingAidMake", "value")
)(findMake)

#FIND HEARING AID TYPE FROM DATABASE OUTPUT TO ADD CLIENT VIEW
@app.callback(
    Output('ClientHearingAidType', "options"),
    Input('ClientHearingAidModel', "value")
)(findType)
   
#FIND HEARING AID MODEL FROM DATABASE OUTPUT TO ADD CLIENT VIEW
@app.callback(
    Output('ClientHearingAidModel', "options"),
    Input('ClientHearingAidManufacturer', "value")
)(findMake)

#Gets MSRP when full view Client
@app.callback(
    Output("changeMSRP", "value"),
    Input('changeQuan', "value"),
    State('changeHearingAidType','value'),
    State('changeHearingAidModel','value'),
    #SECURITY FEATURES
    State('passwordEnter','value'),
    State("memory-output","data"),
    )

def getMSRP(quan,typea,model,password,memory):
    if typea == None or quan == None or model == None:
        return None
    else:
        quan = int(quan)
        hearingaidlist = []
        db_file = memory[1]
        if createDatabase(db_file):
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM MSRP")
                listmodel = cursor.fetchall()
                for hearingaid in listmodel:
                    man,make,typ,price,date = hearingaid
                    if make == model:
                        if typ == typea:
                            hearingaidlist.append(hearingaid)
                #Only 1 matching Hearing Aid
                if len(hearingaidlist) == 1:
                    man,make,typ,price,date = hearingaidlist[0]
                    return price*quan
                #Multiple Matching hearing aids, different dates
                else:
                    olman,olmake,oltyp,olprice,oldate = hearingaidlist[0]
                    for newhearingaid in hearingaidlist:
                        man,make,typ,price,date = newhearingaid
                        if date > oldate:
                            olman,olmake,oltyp,olprice,oldate = newhearingaid
                    return olprice*quan
                            
#ONLY TURNS ON UPDATE BUTTON ONCE APPOINTMENT HAS BEEN SELECTED

@app.callback(
    Output('changeClientInfo','disabled'),
    Input('changeAppointmentType','value')
)

def dropActivate(value):
    if value == None or value == []:
        return True
    else:
        return False


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


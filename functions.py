import os
import sqlite3
from datetime import date
from dateutil.relativedelta import relativedelta
import base64
import io
import pandas as pd

def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

def unhide(value):
    if value == "Yes":
        return {'display':'flex'}
    else:
        return {'display':'None'}
    
def checkfile(filename):
    return os.path.exists(filename)

def createDatabase():
    db_file = 'database.db'
    if checkfile('database.db'):
        return True
    else:
        schema_file = 'ClientSchema.sql'
        payment_file = 'PaymentSchema.sql'
        data_file = 'DataSchema.sql'
        with open(schema_file,'r') as rf:
            schemacli = rf.read()
        with open(payment_file,'r') as rfp:
            schemapay = rfp.read()
        with open(data_file,'r') as rfp:
            schemadata = rfp.read()
        with sqlite3.connect(db_file) as conn:
            conn.executescript(schemacli)
            conn.executescript(schemapay)
            conn.executescript(schemadata)
        return True
    
def getClient(firstname,lastname):
    """Gets client data using first and last name"""
    db_file = 'database.db'
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE firstname = ? AND lastname= ?",(firstname,lastname))
        for row in cursor.fetchall():
            clientnum, tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status = row
            if firstname == tablefirstname:
                #print(firstname)
                return clientnum,tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status
    #error clause here

def getAllClients():
    db_file = 'database.db'
    Clientlist = []
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        Clientlist = cursor.fetchall()
        return Clientlist
    
def getClientByNum(num):
    """Gets clients by client number"""
    db_file = 'database.db'
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE clientid",num)
        for row in cursor.fetchall():
            clientnum, tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status = row
            return clientnum,tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,clientnotes,status
        
def updateClientbyNum(ID):
    if ID == None:
        return False
    else:
        ID = str(ID)
    today = date.today()
    dmy = today.strftime("%Y-%m-%d")
    followupdate = (dmy,)
    db_file = 'database.db'
    if createDatabase():
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE clients SET datefollowup = ? WHERE clientid = " +ID,followupdate)
    
            #  datevisit, datefollowup, hearingaid, hearingaidmodel, hearingaidpurchaseprosound, hearingaidpurchasedate, hearingtest, datetest,
    return True

def generateDate(dof,datesetting):
    """Takes in Date setting to generate a new date"""
    #today = date.today()
    if datesetting == "6 months":
        newdate = dof + relativedelta(months=+6)
        return newdate
    elif datesetting == '3 months':
        newdate = dof + relativedelta(months=+3)
        return newdate
    elif datesetting == '12 months':
        newdate = dof + relativedelta(months=+12)
        return newdate
    elif datesetting == '14 days':
        newdate = dof + relativedelta(days=+14)
        return newdate
    elif datesetting == '28 days':
        newdate = dof + relativedelta(days=+28)
        return newdate
    elif datesetting == '30 days':
        newdate = dof + relativedelta(days=+30)
        return newdate
    elif datesetting == '45 days':
        newdate = dof + relativedelta(days=+45)
        return newdate
    elif datesetting == '60 days':
        newdate = dof + relativedelta(days=+60)
        return newdate
    else:
        return dof
    
def getSalesByClient(clientnumber):
    """Query the database to find all sales matching a client"""
    db_file = 'database.db'
    clientnumber = str(clientnumber)
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales WHERE clientnumber = " +clientnumber)
        salesList = cursor.fetchall()
    return salesList

def readExcel(file):
    content_type, content_string = file.split(',')

    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))
    
    return df
        
def findType(Model):
    #Add for adding new client, edit for editing current one
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
                man,make,typ,price,date = hearingaid
                if Model == make:
                    if typ not in Outputlist:
                        Outputlist.append(typ)
            return Outputlist
        
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
                man,make,typ,price,date = hearingaid
                if manuf == man:
                    if make not in Outputlist:
                        Outputlist.append(make)
            return Outputlist
""" today = date(2023,7,10)
compd = generateDate(today,'12 months')
print('gendate: ', compd)
print('today: ', today)

if compd <= today:
    print('sucess')
else:
    print('no follow') """
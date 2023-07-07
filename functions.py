import os
import sqlite3
from datetime import date
from dateutil.relativedelta import relativedelta

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
        with open(schema_file,'r') as rf:
            schemacli = rf.read()
        with open(payment_file,'r') as rfp:
            schemapay = rfp.read()
        with sqlite3.connect(db_file) as conn:
            conn.executescript(schemacli)
            conn.executescript(schemapay)
        return True
    
def getClient(firstname,lastname):
    """Gets client data using first and last name"""
    db_file = 'database.db'
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE firstname = ? AND lastname= ?",(firstname,lastname))
        for row in cursor.fetchall():
            clientnum, tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes = row
            if firstname == tablefirstname:
                #print(firstname)
                return clientnum,firstname,lastname,email,phone,address,postal,city,province,healthcard,clientnotes
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
            clientnum, tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingAid,hearingAidModel,ProsoundPurchase,Prosoundpurchasedate,hasHearingTestdate,Hearingtestdate,clientnotes = row
            return clientnum,tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,clientnotes
        
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
    if datesetting == '3 months':
        newdate = dof + relativedelta(months=+3)
        return newdate
    if datesetting == '12 months':
        newdate = dof + relativedelta(months=+12)
        return newdate
    else:
        return dof
    
""" compd = generateDate('3 months')
today = date(2024,7,5)
print('gendate: ', compd)
print('today: ', today)

if compd <= today:
    print('sucess')
else:
    print('no follow') """
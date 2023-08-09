import os
import sqlite3
from datetime import date
from dateutil.relativedelta import relativedelta
import base64
import io
import pandas as pd
import hashlib
import pickle
import pyAesCrypt
from cryptography.fernet import Fernet

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

def createDatabase(dbfile):
    if checkfile(dbfile):
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
        with sqlite3.connect(dbfile) as conn:
            conn.executescript(schemacli)
            conn.executescript(schemapay)
            conn.executescript(schemadata)
        return True

#
"""GETTING CLIENT DATA FUNCTIONS PAST THIS POINT"""
#

def getClient(firstname,lastname,db_file,keyfile,password):
    """Gets client data using first and last name"""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE firstname = ? AND lastname= ?",(firstname,lastname))
        for row in cursor.fetchall():
            clientnum, tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status = row
            if firstname == tablefirstname:
                #print(firstname)
                return clientnum,tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status
    #error clause here

def getAllClients(db_file):
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
        cursor.execute("SELECT * FROM clients WHERE clientid = ?",num)
        for row in cursor.fetchall():
            clientnum, tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,dateofvisit,followupdate,hasHearingTestdate,Hearingtestdate,clientnotes,status = row
            return clientnum,tablefirstname,tablelastname,email,phone,address,postal,city,province,healthcard,clientnotes,status
        
def updateClientbyNum(ID,db_file,keyfile,password):
    if ID == None:
        return False
    else:
        ID = str(ID)
    today = date.today()
    dmy = today.strftime("%Y-%m-%d")
    followupdate = (encrypt(keyfile,password,dmy))
    if createDatabase(db_file):
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
    
def getSalesByClient(clientnumber,db_file):
    """Query the database to find all sales matching a client"""
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
    if createDatabase(db_file):
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
    if createDatabase(db_file):
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
        
def getClientNum(clicks,db_file):
    #Make Database here
    if createDatabase(db_file):
        allclients = getAllClients(db_file)
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
    
#
""" THIS IS ALL FOR ENCRYPTION AND SECURITY FROM THIS POINT DOWN"""
#

def hashInput(input):
    output = hashlib.sha256(input.encode()).hexdigest()
    return output

def readKey(filename,password):
    f = pickle.load(open(filename,'rb'))

    fdec = io.BytesIO()
    fCiph = io.BytesIO(f)

    # decrypt stream
    pyAesCrypt.decryptStream(fCiph, fdec, password)
    return fdec.getvalue()

def decrypt(keyname,password,data):
    #print(data)
    key = readKey(keyname,password)
    f = Fernet(key)
    output = f.decrypt(data).decode()
    return output

def decryptList(keyname,password,listdata):
    outputlist = []
    for item in listdata:
        decrypteditem = decrypt(keyname,password,item)
        outputlist.append(decrypteditem)
    return outputlist

def encrypt(keyname,password,data):
    data = str(data)
    key = readKey(keyname,password)
    f = Fernet(key)
    output = f.encrypt(data.encode())
    return output

def encryptList(keyname,password,listdata):
    outputlist = []
    for item in listdata:
        encrypteditem = encrypt(keyname,password,item)
        outputlist.append(encrypteditem)
    return outputlist

def encryptTuple(keyname,password,listdata):
    data = list(listdata[0])
    output = tuple(encryptList(keyname,password,data))
    return [output]

def encryptDf(keyname,password,df):
    encryptdict = {}

    for column in df:
        columnlist = df[column].tolist()
        columnlist = encryptList(keyname,password,columnlist)
        #print(columnlist)
        encryptdict[column] = columnlist

    encdf = pd.DataFrame.from_dict(encryptdict)

    return encdf
from hashlib import new
from tkinter import Y
from weakref import ref
from dash import Output,Input,MATCH,State,ctx,dcc,ALL
import pandas as pd
from App import app
from datetime import date
from functions import *
import plotly.graph_objects as go


today = date.today()
# dd/mm/YY day month year
dmy = today.strftime("%d/%m/%Y")

app.callback(
    Output("ClientModal", "is_open"),
    Input("ClientButton", "n_clicks"),
    State("ClientModal", "is_open"),
)(toggle_modal)

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
    Input("PurchaseDropdown", "value")
)(unhide)

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
    Input("ClientConfirm", "n_clicks")
)
def ConfirmClient(clicks,firstname,lastname,email,phone,address,postal,city,province):
    print(firstname,lastname,email,phone,address,postal,city,province)
    return True,None,None,None,None,None,None,None,None
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


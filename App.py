from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(__name__,external_stylesheets=[dbc.themes.LUX])

#Use google cloud to ensure everything is stored in the cloud
#Entire Client Dashboard, can add, remove and manage clients, following up with them when needed
#Can store invoices along with purchase historys along with amounts
#Can search by hearing aids looking at total units sold and amount
#Visualize Sales
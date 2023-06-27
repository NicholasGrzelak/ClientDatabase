import os

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
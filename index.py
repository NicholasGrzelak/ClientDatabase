#-----------------------------------------------------------------------------
# Client Database App
# Copyright (c) 2023, Nicholas Grzelak
#-----------------------------------------------------------------------------

from App import app
from layout import layout
from callbacks import *

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)


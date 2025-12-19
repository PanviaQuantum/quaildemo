##################################################################################################################
# state.py
# Render state probability plots from teleport json QPS
# Copyright Panvia Future Technologies Inc. 2018-2024
# Roger Selly
# Python functional API for PanviaQuantumWebStore server
#############################################################
import json
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Bokeh libs
import bokeh.colors
import bokeh.palettes
import bokeh.transform
from bokeh.palettes import Category20
from bokeh.io import output_file, output_notebook
from bokeh.io import export_png
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
from bokeh.models.layouts import Tabs, TabPanel

# Pass input JSON file containing trace response
# Write HTML files with plots of state vector probabilities
# - 5 files 41 qubits + 4 * 10 qubits
#  output filename = input filename,~a,~b,~c,~d.html
def state( y ):
    subplots = 4
    nq=3   # number of qubits per multiverse
    svdim = 1 << nq   # state vector dim = 2^nq

    n = len(y)    # get total number of worlds = items
    n1 = y[0][0]['panvia']['response']['total']    # get total trace items
    if n1 != n:
        print('error in worlds vs items:' + str(n) + ' != ' + str(n1) )
        input()
        return

    div = int(n/subplots)                      # div = size of subplot
    remaining = n - ( subplots * div )         # 
    splits = subplots
    if remaining > 0:
       splits += 1

    key  = [None]*n
    subkeyraw = [ [None]*div ] * subplots
    subkey = np.array(subkeyraw)

    raw = [[0.0]*svdim]*n    # allocate column of state vector probabilities for each item
    data = np.array(raw)

    subraw = [ [[0.0]*svdim]*div ] * subplots
    subdata = np.array(subraw)

    coldim = svdim + 1     # add 1 for the column title in list[0]
    cols = [0]*svdim
    subcolsraw = [ [None]*svdim] * subplots
    subcols = np.array(subcolsraw)

    for w in y:     # loop over worlds
       for x in w:    # loop over trace items in world
         item = int(x['panvia']['response']['item'])
         plotindex = n - 1 - item   # reverse order for plot
         subplot = int( item / div )  
         subplotitem = item % div
         subplotindex = div - 1 - subplotitem
         p = float(x['panvia']['list'][0]['probability'])
         k = x['panvia']['list'][0]['tag']['key']
         s = x['panvia']['list'][0]['state']
         t = s.split()
         sv = int(t[1],2)
         # print( str(item) + ' p: ' + str(p) + ' sv: ' + str(sv) + ' s: ' + s + k )
         data[plotindex,sv] = p
         if key[plotindex] == None:
            # print(str(item) + k )
            key[plotindex] = k     # add column header = tag key for state vectors
         if subplot < subplots:
            subdata[subplot,subplotindex,sv] = p
            if subkey[subplot,subplotindex] == None:
               # print(str(item) + k )
               subkey[subplot,subplotindex] = k     # add column header = tag key for state vectors
            if subcols[subplot,sv] == None:
               # print(s)
               subcols[subplot,sv] = s

         if cols[sv] == 0:
            cols[sv] = s


         #pprint(cols)
         #pprint(key)
         #pprint(data)

      # Create a dataframe from data array
    df = pd.DataFrame(data, index=key, columns=cols)
    df.columns.name='state'
    df.index.name='circuit'
    pprint(df)
    source=ColumnDataSource(df)
    # output_file( plotfile )   # for html
    p=figure(y_range=key, height=650, title='state probabilities', toolbar_location=None, tools='hover', tooltips='$name @circuit: @$name',x_axis_location='above')
    p.hbar_stack(cols, y='circuit', height=0.9, color=Category20[8], source=source, legend_label=cols)
    p.add_layout(p.legend[0],'right')
    show(p)    # for html
    # print( plotfile )
    # export_png(p, filename=plotfile )

    # Create subplots of ten multiverses each
    for i in range(subplots):
        df = pd.DataFrame(subdata[i], index=subkey[i], columns=cols)
        df.columns.name='state'
        df.index.name='circuit'
         # pprint(df)

        source=ColumnDataSource(df)
        # output_file( subplotfiles[i] )  # for html
        p=figure(y_range=subkey[i], height=250, title='state probabilities', toolbar_location=None, tools='hover', tooltips='$name @circuit: @$name',x_axis_location='above')
        p.hbar_stack(cols, y='circuit', height=0.9, color=Category20[8], source=source, legend_label=cols)
        p.add_layout(p.legend[0],'right')
        show(p)    # for html
        # export_png(p, filename=subplotfiles[i] )

##########   end of state.py   ##############

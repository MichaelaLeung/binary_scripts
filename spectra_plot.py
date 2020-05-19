#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:22:21 2020

@author: mwl
"""
import csv 
import matplotlib.pyplot as plt
import smart 
import numpy as np 
import pandas as pd 

def spectra_plot(): 
    data = []
    data2 = []
    csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/twostars3_out_bndflux1.csv'
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(list(row))
    fig,ax = plt.subplots(1,1, figsize = (10,10))
#    print(data)
    f_wn = []
    wn = data[1]
    wn = list(wn)
    for v in wn[:-1]: 
        print(v)
        out = float(v)
        f_wn.append(out)
    i = 0
    data = data[2:]
    for row in data: 
     #   print(row)
        temp = []
        row = row[:-1]
        for num in row:
      #      print(num)
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(f_wn, temp)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_row'+str(i) + '.png')
#    wn = data[1]
#    wn = np.array(wn[:-1])
#    print(wn[:-1])
#    wn_float = []
#    for i in wn: 
#        print(i, float(i))
#        wn_float.append(float(i)/10000)
#    data = data[1:]
#    df = pd.DataFrame(data)
#    print(df)
#    csv_path2 = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/twostars3_out_bndflux2.csv'
#    with open(csv_path2) as csvfile:
#        readCSV = csv.reader(csvfile, delimiter=',')
#        for row in readCSV:
#            data2.append(np.array(row))
#    data2 = data2[1:]
#    df2 = pd.DataFrame(data2)
#    wl_df = pd.DataFrame(wn_float)
#    g_avg = df.mean(axis = 0)
#    m_avg = df2.mean(axis = 0)
#    g_avg.append(wl_df)
#    m_avg.append(wl_df)
#    print(g_avg)
  
    
#        fig,ax = plt.subplots(1,1, figsize = (10,10))
#        ax.plot(wn, row)
  #  ax.plot(wn_float, m_avg, label = "M")
  #  ax.legend()
 #   g_avg.plot()
 #   m_avg.plot()
 #   fig.savefig('/gscratch/vsm/mwjl/projects/binary/plots/spec_out.png')
        
    
if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="specplt",
                               subname="submit.csh",
                               workdir = "",
                               nodes = 1,
                               mem = "500G",
                               walltime = "72:00:00",
                               ntasks = 28,
                               account = "vsm",
                               submit = True,
                               rm_after_submit = True)
    elif platform.node().startswith("n"):
        # On a mox compute node: ready to run
        spectra_plot()

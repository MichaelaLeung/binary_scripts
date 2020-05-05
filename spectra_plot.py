#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:22:21 2020

@author: mwl
"""
import csv 
import matplotlib.pyplot as plt

def spectra_plot(): 
    data = []
    csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/'
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row)
    data = data[1:]
    fig,ax = plt.subplots(figsize = (10,10))
    for row in data:
        x = range(len(row))
        ax.plot(x,row)
    fig.savefig('/gscratch/vsm/mwjl/projects/binary/plots/spec_out.png')
        
    
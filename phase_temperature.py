#!/usr/bin/python

import numpy as np
import matplotlib; matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from astropy.io import fits
import smart
import sys, os
import datetime
matplotlib.rcParams['text.usetex'] = False
import random
import math 
import csv

def phase_temp()
    data = []
    with open("/gscratch/vsm/mwjl/projects/binary/twostarsGG/twostars3_out_general.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row[3:5])
    data = data[1:]
    star1 = []
    star2 = []
    for line in data: 
        temp = line[0]
        temp = temp.strip(" ")
        star1.append(float(temp))
        temp2 = line[1]
        temp2 = temp2.strip(" ")
        star2.append(float(temp2))

    t_star = [] # converting timescale to days
    t_star_temp = range(len(star1))
    for i in t_star_temp: 
        temp3 = float(i)
        temp3 = temp3 *0.01 
        t_star.append(temp3)

    infile = "/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info.dat"
    t_final = []
    block_length = 128
    skip_lines = 7
    i = 0

    while i < 86400: 
        temp = np.genfromtxt(infile, skip_header = (1 + (block_length + skip_lines)*(i-1)), max_rows = block_length)
        T = temp[-1:,1]
        t_final.append(float(T))
        i = i+1
        
    matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
    matplotlib.rcParams['font.size'] = 15.0
    matplotlib.rc('text', usetex=False)
    plt.switch_backend('agg')

    ax.plot(range(len(t_final)), t_final)
    ax.set_xlabel("Time stamp")
    ax.set_ylabel("Temperature")
    fig.savefig("/gscratch/vsm/mwjl/projects/binary/plots/phase_temp.png", bbox_inches = "tight")


#!/usr/bin/python

import numpy as np
import matplotlib; matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from astropy.io import fits
import sys, os
import datetime
matplotlib.rcParams['text.usetex'] = False
import random
import math 
import csv
import smart 
print('imports')

def phase_temp(pair):
    print('pt start') 
    data = []
    with open("/gscratch/vsm/mwjl/projects/binary/twostars" + str(pair)+ "/twostars3_out_general.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row[3:5])
        print("csv")
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
    print("arrays")

    t_star = [] # converting timescale to days
    t_star_temp = range(len(star1))
    for i in t_star_temp: 
        temp3 = float(i)
        temp3 = temp3 *0.01 
        t_star.append(temp3)
    print("time conversion")

    infile = "/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info.dat"
    t_final = []
    block_length = 128
    skip_lines = 7

    i = 0

    while i < len(star2): 
        temp = np.genfromtxt(infile, skip_header = (1 + (block_length + skip_lines)*(i-1)), max_rows = block_length)
        T = temp[-1:,1]
        t_final.append(float(T))
        print(T,i)
        i = i+10
        
    matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
    matplotlib.rcParams['font.size'] = 15.0
    matplotlib.rc('text', usetex=False)
    plt.switch_backend('agg')
    fig, ax = plt.subplots(figsize = (10,10))
    ax.plot(range(len(t_final)), t_final)
    ax.set_xlabel("Time stamp")
    ax.set_ylabel("Surface Temperature")
    fig.savefig("/gscratch/vsm/mwjl/projects/binary/plots/phase_temp" + str(pair)+ ".png", bbox_inches = "tight")


if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="phase_T",
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
        phase_temp('GM')
    else:
        phase_temp()

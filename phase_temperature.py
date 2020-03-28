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
    o3_final = []
    co2_final = []
    o2_final = []
    h2o_final = []
    ch4_final = []
    n2o_final = []
    ch3cl_final = []
    block_length = 128
    skip_lines = 7

    i = 0

    while i < 100000: 
        temp = np.genfromtxt(infile, skip_header = (1 + (block_length + skip_lines)*(i-1)), max_rows = block_length)
        T = temp[-1:,1]
        O3 = temp[-1,2]
        CO2 = temp[-1,3]
        O2 = temp[-1:,4]
        H2O = temp[-1,5]
        CH4 = temp[-1,6]
        N2O = temp[-1,7]
        CH3Cl = temp[-1,8]
        t_final.append(float(T))
        o3_final.append(float(O3))
        co2_final.append(float(CO2))
        o2_final.append(float(O2))
        h2o_final.append(float(H2O))
        ch4_final.append(float(CH4))
        n2o_final.append(float(N2O))
        ch3cl_final.append(float(CH3Cl))
        print(i)
        i = i+100
        
    matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
    matplotlib.rcParams['font.size'] = 15.0
    matplotlib.rc('text', usetex=False)
    plt.switch_backend('agg')
    fig, ax = plt.subplots(8,1,figsize = (15,32))
    ax[0].plot(range(len(t_final)), t_final, label = "Temp")
    ax[1].plot(range(len(o3_final)), o3_final, label = "O3")
    ax[2].plot(range(len(co2_final)), co2_final, label = "CO2")
    ax[3].plot(range(len(o2_final)), o2_final, label = "O2")
    ax[4].plot(range(len(h2o_final)), h2o_final, label = "H2O")
    ax[5].plot(range(len(ch4_final)), ch4_final, label = "CH4")
    ax[6].plot(range(len(n2o_final)), n2o_final, label = "N2O")
    ax[7].plot(range(len(ch3cl_final)), ch3cl_final, label = "CH3Cl")
    ax[0].set_xlabel("Time stamp")
    ax[0].set_ylabel("Temperature (K)")

    i = 1
    while i <= 7:
        ax[i].set_xlabel("Time stamp")
        ax[i].set_ylabel("Gas abundance")
        ax[i].legend()
        i = i+1
    fig.savefig("/gscratch/vsm/mwjl/projects/binary/plots/phase_temp_both" + str(pair)+ ".png", bbox_inches = "tight")

def phase_temp_conly(pair):
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
    o3_final = []
    co2_final = []
    o2_final = []
    h2o_final = []
    ch4_final = []
    block_length = 128
    skip_lines = 7

    i = 0

    while i < 100000: 
        temp = np.genfromtxt(infile, skip_header = (1 + (block_length + skip_lines)*(i-1)), max_rows = block_length)
        T = temp[-1:,1]
        O3 = temp[-1,2]
        CO2 = temp[-1,3]
        O2 = temp[-1:,4]
        H2O = temp[-1,5]
        CH4 = temp[-1,6]
        N2O = temp[-1,7]
        CH3Cl = temp[-1,8]
        t_final.append(float(T))
        o3_final.append(float(O3))
        co2_final.append(float(CO2))
        o2_final.append(float(O2))
        h2o_final.append(float(H2O))
        ch4_final.append(float(CH4))
        print(i)
        i = i+100
        
    matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
    matplotlib.rcParams['font.size'] = 15.0
    matplotlib.rc('text', usetex=False)
    plt.switch_backend('agg')
    fig, ax = plt.subplots(6,1,figsize = (15,32))
    ax[0].plot(range(len(t_final)), t_final, label = "Temp")
    ax[1].plot(range(len(o3_final)), o3_final, label = "O3")
    ax[2].plot(range(len(co2_final)), co2_final, label = "CO2")
    ax[3].plot(range(len(o2_final)), o2_final, label = "O2")
    ax[4].plot(range(len(h2o_final)), h2o_final, label = "H2O")
    ax[5].plot(range(len(ch4_final)), ch4_final, label = "CH4")
    ax[0].set_xlabel("Time stamp")
    ax[0].set_ylabel("Temperature (K)")

    i = 1
    while i <= 5:
        ax[i].set_xlabel("Time stamp")
        ax[i].set_ylabel("Gas abundance")
        ax[i].legend()
        i = i+1
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
        phase_temp('GG')
    else:
        phase_temp()

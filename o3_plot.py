import numpy as np
import matplotlib; matplotlib.use('agg')
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from matplotlib.collections import LineCollection
from astropy.io import fits
import smart
import sys, os
import datetime
matplotlib.rcParams['text.usetex'] = False
import random
import math
import csv

def plot_o3(infile, pair):
    file = np.genfromtxt(infile, skip_header = 1)
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
        i = 0
        while i < 864:
            star1.append(float(temp))
            i = i+1 # original units are 1/100 of a day, 864 seconds -> should now be in seconds 
        temp2 = line[1]
        temp2 = temp2.strip(" ")
        j = 0
        while j < 864: 
            star2.append(float(temp2))
            j = j+1
    
    time = []
    o3 = []
    for line2 in file: 
        time.append(float(line2[0]))  # original units are in seconds 
        o3.append(line2[1])
        
    fig, ax = plt.subplots(figsize = (10,6))
    plt.plot(time,o3)
    plt.plot(range(len(star1)), star1)
    plt.plot(range(len(star2)), star2)
   # ax.set_yscale('log')
    ax.set_ylabel('O3 column depth (cm$^{-2}$)')
    ax.set_xlabel('Time (seconds)')
    #fig.savefig(str(pair)+"o3plot.png", bbox_inches = 'tight')

    fig.savefig("/gscratch/vsm/mwjl/projects/binary/plots/" + str(pair)+"o3plot.png", bbox_inches = 'tight')

if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="o3_plot",
                               subname="submit.csh",
                               workdir = "",
                               nodes = 1,
                               mem = "500G",
                               walltime = "10:00:00",
                               ntasks = 28,
                               account = "vsm",
                               submit = True,
                               rm_after_submit = True)
    elif platform.node().startswith("n"):
        # On a mox compute node: ready to run
        plot_o3('/gscratch/vsm/mwjl/projects/binary/multiflare/io/o3coldepth.dat', 'GG')
    else:
         plot_o3('o3coldepth.dat', 'GG')

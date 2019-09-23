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
    infile = "o3coldepth.dat"
    file = np.genfromtxt(infile, skip_header = 1)
    data = []
    with open("twostars3_out_general.csv") as csvfile:
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
        temp1 = line[1]
        temp1 = temp1.strip(" ")
        star2.append(float(temp1))
    
    t_star_final = []
    t_star = range(len(star1))
    for i in t_star: 
        t_star_final.append(i*1/100)
    
    time = []
    o3 = []
    for line2 in file: 
        time.append(float(line2[1])/84600)  # original units are in seconds 
        o3.append(float(line2[3]))

    fig, ax = plt.subplots(2,1, figsize = (20,12))

    ax[0].set_xlim(0,400)
    ax[1].set_xlim(0,400)

    ax[0].plot(time,o3)

    ax[1].plot(t_star_final, star1)
    ax[1].plot(t_star_final, star2)

    ax[0].set_ylabel('O3 column depth (cm$^{-2}$)')
    ax[0].set_xlabel('Time (days)')

    ax[1].set_xlabel('Time (days)')

    fig.savefig("/gscratch/vsm/mwjl/projects/binary/" + str(pair)+"o3plot.png", bbox_inches = 'tight')

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

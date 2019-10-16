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

def plot_mixingratios(infile, i, pair):
    #setting up constants
    block_length = 128
    skip_lines = 7
    i = int(i)
    #getting molecule names from input file
    with open(infile) as f:
        first_line = f.readline()
    mol_names = []
    first_line = first_line.strip('\n') 
    first_line = first_line.split(" ")
    for j in first_line: 
        if j != '':
            mol_names.append(j)
    mol_names = mol_names[2:]
    #finding the correct block in the long output file
    temp = np.genfromtxt(infile, skip_header = (1 + (block_length + skip_lines)*(i-1)), max_rows = block_length)
    #separating out the gases, P and T
    gases = temp[:,2:]
    P = temp[:,0]
    T = temp[:,1]
    T2 = []
    for b in T:
        temp2 = float(b)
        T2.append(temp2)
    #plotting
    matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
    matplotlib.rcParams['font.size'] = 15.0
    matplotlib.rc('text', usetex=False)
    plt.switch_backend('agg')

    fig, ax = plt.subplots(figsize=(9,9))
    ax.invert_yaxis()
    ax.plot(0,0,color="black", label="Temp.", ls="--")
    for k in range(len(mol_names)):
        ax.plot(gases[:,k], P, label=mol_names[k])
    ax.set_xlabel("Volume Mixing Ratio")
    ax.set_ylabel("Pressure [Pa]")
    ax.set_xlim(10**(-15),1)
    ax.set_ylim(0, 10**5)   
    ax.loglog()
    ax.legend()

    axT = ax.twiny()
    axT.set_xlabel("Temperature [K]")
    axT.set_axisbelow(True)
#    axT.set_xlim(200,300)    
    axT.plot(T2, P, color="black", label="Temperature", ls="--")
    fig_name = "/gscratch/vsm/mwjl/projects/binary/plots/" + str(i) + str(pair) + ".png"
    fig.savefig(fig_name, bbox_inches = "tight")
    return(fig_name)

def run_plots(values, pair):
    inputs = []
    for i in values:
        temp = plot_mixingratios("/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info.dat",i, pair)
        inputs.append(temp)
    gif_path = pair
    plt.figure(figsize=(10,10))
    with imageio.get_writer(gif_path, mode='I') as writer:
        for i in range(len(inputs)):
            writer.append_data(imageio.imread(inputs[i].format(i=i)))


if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="PT_plot",
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
        run_plots([10000,20000,30000,40000,50000,60000,70000,80000,90000,100000], "GG")
    else:
        plot_mixingratios('GG_output_pt.txt', 5)



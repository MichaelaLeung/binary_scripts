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
import imageio

def plot_mixingratios(infile, i, pair):
    #setting up constants
    block_length = 128
    skip_lines = 7
    i = int(i)
    #getting molecule names from input file
#    with open(infile) as f:
#        first_line = f.readline()
#    mol_names = []
#    first_line = first_line.strip('\n') 
#    first_line = first_line.split(" ")
#    for j in first_line: 
#        if j != '':
#            mol_names.append(j)
#    mol_names = mol_names[2:]
    #finding the correct block in the long output file
    temp = np.genfromtxt(infile, skip_header = (7 + (block_length + skip_lines)*(i)), max_rows = block_length)
#    print(temp)
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
    ax.plot(0,0,color="black", label="Temp.", ls="--")
    mol_names = temp[7,2:]
    print(mol_names)
    mol_names = np.split(mol_names,7)
    print(len(mol_names))
    mol_names_str = "O3", "CO2", "O2", "H2O", "CH4", "N2O", "CH3Cl"
    for k in range(len(mol_names)):
        print(gases[:,k], i)
        ax.plot(gases[:,k], P, label=mol_names_str[k])
    ax.set_xlabel("Volume Mixing Ratio")
    ax.set_ylabel("Pressure [Pa]")
    ax.set_xlim(10**(-15),1)
    ax.set_ylim(10**5,30)   
    ax.loglog()
    ax.legend()

    axT = ax.twiny()
    axT.set_xlabel("Temperature [K]")
    axT.set_axisbelow(True)
    axT.set_xlim(180,320)    
    axT.plot(T2, P, color="black", label="Temperature", ls="--")
    fig_name = "/gscratch/vsm/mwjl/projects/binary/plots/" + str(i) + str(pair) + ".png"
    fig.savefig(fig_name, bbox_inches = "tight")
    return(fig_name)

def run_plots(values, pair):
    for i in values:
        plot_mixingratios("/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info_4114GG.dat",i, pair)
        print(i)
#        plot_mixingratios("/gscratch/vsm/mwjl/projects/binary/spectra_info.dat", i, pair) 
       #temp = "/gscratch/vsm/mwjl/projects/binary/plots/"+str(i)+str(pair)+".png"
        #inputs.append(temp)
    gif_path = "/gscratch/vsm/mwjl/projects/binary/plots/" + str(pair) + ".gif"
    nums = values
    inputs = []
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/plots/"+str(i)+str(pair)+".png"
        inputs.append(name)
    plt.figure(figsize=(4,4))

    with imageio.get_writer(gif_path, mode='I') as writer:
        for i in range(len(inputs)):
            writer.append_data(imageio.imread(inputs[i].format(i=i)))


def gif_only(values, pair): 
    gif_path = str(pair) + ".gif"
    nums = values
    inputs = []
    for i in nums:
        name = "/gscratch/vsm/mwjl/projects/binary/plots/"+str(i)+str(pair)+".png"
        inputs.append(name)
    plt.figure(figsize=(4,4))

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
        num = range(1,100000,1000)
        run_plots(num, "GG")
#        gif_only(num, "GG")    
#run_plots(num, "GM")
#        run_plots(num, "GG")
    else:
        plot_mixingratios('GG_output_pt.txt', 5)



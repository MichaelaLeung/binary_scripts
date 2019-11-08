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
import subprocess
from shutil import copyfile
import platform


def run_smart_surface(infile, i, pair):
    place = '/gscratch/vsm/mwjl/projects/binary/scripts/smart/'
    sim = smart.interface.Smart(tag = "earth")
    sim.set_run_in_place(place)

    #setting up constants
    block_length = 128
    skip_lines = 7
    i = int(i)
    #getting molecule names from input file
    with open(infile) as f:
        first_line = f.readline()
    mol_names_full = []
    first_line2 = first_line.strip('\n') 
    first_line2 = first_line2.split(" ")
    for j in first_line2: 
        if j != '':
            mol_names_full.append(j)
    mol_names = mol_names_full[2:]
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
    np.savetxt("temp.pt",temp, header = first_line,comments = "")
        
    label = "Earth-like"
    sim.smartin.alb_file = "/gscratch/vsm/mwjl/projects/high_res/inputs/composite1_txt.txt"
    
    sim.smartin.out_dir = '/gscratch/vsm/mwjl/projects/binary/scripts/smart_output'
    sim.lblin.out_dir = '/gscratch/vsm/mwjl/projects/binary/scripts/smart_output'
    sim.smartin.abs_dir = '/gscratch/vsm/mwjl/projects/binary/scripts/smart_output'

    sim.set_executables_automatically()

    sim.lblin.par_file = '/gscratch/vsm/alinc/fixed_input/HITRAN2016.par' #/gscratch/vsm/alinc/fixed_input/
    sim.lblin.hitran_tag = 'hitran2016'
    sim.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'

    sim.load_atmosphere_from_pt("temp.pt", addn2 = True, scaleP = 1.0)

    lamin = 0.1
    lamax = 0.4

    res = 2
    sim.smartin.FWHM = res
    sim.smartin.sample_res = res


    sim.smartin.minwn = 1e4/lamax
    sim.smartin.maxwn = 1e4/lamin 

    sim.lblin.minwn = 1e4/lamax
    sim.lblin.maxwn = 1e4/lamin

    sim.lblin.par_index = 7
    sim.smartin.out_level = 2
    sim.gen_lblscripts()
    sim.run_lblabc()
    sim.write_smart(write_file = True)
    sim.run_smart()

    infile = '/gscratch/vsm/mwjl/projects/binary/scripts/smart_output/from_binary_25000_100000cm_sur.rad'
    # Convert each line to vector, compose array of vectors
    arrays = np.array([np.array(list(map(float, line.split()))) for line in open(infile)])

    # Flatten and reshape into rectangle grid
    arr = np.hstack(arrays).reshape((14, -1), order='F')

    # Parse columns
    lam   = arr[0,:]
    wno   = arr[1,:]
    solar = arr[2,:]
    dir_flux  = arr[3,:]
    diff_flux  = arr[4,:]

    total_flux = dir_flux + diff_flux

    fig, ax = plt.subplots(figsize = (20,12))
    ax.plot(lam, total_flux, label = "Earth-like atmosphere")
    ax.set_ylabel("Reflectance")
    ax.set_xlabel("Wavelength ($\mu$ m)")
    ax.legend()
    fig.savefig("/gscratch/vsm/mwjl/projects/binary/plots/smart_" + str(pair) + str(i) +".png")

def run_smart_toa(lamin = 0.1, lamax = 0.4, res = 0.01):
    place = '/gscratch/vsm/mwjl/projects/binary/scripts/smart/'
    sim = smart.interface.Smart(tag = "earth")
    sim.set_run_in_place(place)
        
    label = "Earth-like"
    sim.smartin.alb_file = "/gscratch/vsm/mwjl/projects/high_res/inputs/composite1_txt.txt"
    
    sim.smartin.out_dir = '/gscratch/vsm/mwjl/projects/binary/scripts/smart_output'
    sim.lblin.out_dir = '/gscratch/vsm/mwjl/projects/binary/scripts/smart_output'
    sim.smartin.abs_dir = '/gscratch/vsm/mwjl/projects/binary/scripts/smart_output'

    sim.set_executables_automatically()

    sim.lblin.par_file = '/gscratch/vsm/alinc/fixed_input/HITRAN2016.par' #/gscratch/vsm/alinc/fixed_input/
    sim.lblin.hitran_tag = 'hitran2016'
    sim.lblin.fundamntl_file = '/gscratch/vsm/alinc/fixed_input/fundamntl2016.dat'
    sim.lblin.lblabc_exe = '/gscratch/vsm/alinc/exec/lblabc_2016'

    sim.load_atmosphere_from_pt("temp.pt", addn2 = True, scaleP = 1.0)

    res = 2
    sim.smartin.FWHM = res
    sim.smartin.sample_res = res


    sim.smartin.minwn = 1e4/lamax
    sim.smartin.maxwn = 1e4/lamin 

    sim.lblin.minwn = 1e4/lamax
    sim.lblin.maxwn = 1e4/lamin

    sim.lblin.par_index = 7
    sim.smartin.out_level = 2
    sim.gen_lblscripts()
    sim.run_lblabc()
    sim.write_smart(write_file = True)
    sim.run_smart()
    sim.open_outputs()
    wl = sim.output.rad.lam
    flux = sim.output.rad.pflux
    sflux = sim.output.rad.sflux
    flux = flux/sflux

    return(wl, flux)


if __name__ == '__main__':

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="SMRT_BI",
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
        run_smart("/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info.dat", 10, "GG")
    else:
        run_smart("spectra_info.dat", 10)


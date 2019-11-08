import numpy as np
import matplotlib; matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from astropy.io import fits
import smart
import sys, os
import datetime
import random
import math
import csv

def spec_out(pair):
    G_spectra_file = '/gscratch/vsm/mwjl/packages/photochem_smart/fixed_input/specs/Kurucz1cm-1_susim_atlas2.dat'
    G = np.genfromtxt(G_spectra_file, skip_header = 11, skip_footer = 100)
    G = G[1:]
    G_wn = G[:,0]
    K_spectra_file = '/gscratch/vsm/mwjl/packages/photochem_smart/fixed_input/specs/ADLeo.dat'
    K = np.genfromtxt(K_spectra_file, skip_header = 1)
    K = K[1:]
    K_wn = K[:,0]
    M_spectra_file = '/gscratch/vsm/mwjl/packages/photochem_smart/fixed_input/specs/proxima_cen.dat'
    M = np.genfromtxt(M_spectra_file, skip_header = 400)
    M = M[1:]
    M_wn = M[:,0]
    if pair == "GG":
        weights_file = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/GGTweights.csv'
        out_name = "/gscratch/vsm/mwjl/projects/binary/plots/outGG.txt"
        solar_flux1 = G[:,1]
        solar_flux2 = G[:,1]
    elif pair == "GK":
        weights_file = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/GKTweights.csv'
        out_name = "/gscratch/vsm/mwjl/projects/binary/plots/outGK.txt"
        solar_flux1 = G[:,1]
        solar_flux2 = K[:,1]
    elif pair == "GK":
        weights_file = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/GMTweights.csv'
        out_name = "/gscratch/vsm/mwjl/projects/binary/plots/outGM.txt"
        solar_flux1 = G[:,1]
        solar_flux2 = M[:,1]
    weights = []
    with open(weights_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            weights.append(row)
        weights = np.asarray(weights)
        time = weights[:,0]
        stell_1 = weights[:,1]
        stell_2 = weights[:,2]
        i = 0
        stell_1_out = []
        stell_2_out = []
        stell_out = []
        while i < min(len(solar_flux1),len(solar_flux2),len(stell_1)):
           stell_1_out.append(float(solar_flux1[i]) * float(stell_1[i]))
           stell_2_out.append(float(solar_flux2[i]) * float(stell_2[i]))
           stell_out.append((float(stell_1_out[i]) + float(stell_2_out[i]))/2)
           i = i+1
        wn = np.zeros(len(solar_flux1))
        stell_out = np.zeros(len(solar_flux1))
        output = np.zeros((len(solar_flux1),2), dtype = 'float')
        output[:,0] = wn
        output[:,1] = stell_out
        np.savetxt(out_name, output)

def smart_spectral(pair,i):
        
    infile = '/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info.dat'
    res = 0.01
    lamin = 0.10
    lamax = 0.40

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
    
    sim = smart.interface.Smart(tag = "prox")
    sim.set_run_in_place()

   # infile7 = "/gscratch/vsm/mwjl/projects/high_res/inputs/profile_Earth_proxb_.pt_filtered"
    sim.smartin.alb_file = "/gscratch/vsm/mwjl/projects/high_res/inputs/composite1_txt.txt"
    sim.set_planet_proxima_b()
    sim.load_atmosphere_from_pt("temp.pt", addn2 = True)
    if pair == "GG":
        sim.smartin.spec = "/gscratch/vsm/mwjl/projects/binary/plots/outGG.txt"
    elif pair == "GM":
        sim.smartin.spec = "/gscratch/vsm/mwjl/projects/binary/plots/outGM.txt"
    elif pair == "GK":
        sim.smartin.spec = "/gscratch/vsm/mwjl/projects/binary/plots/outGK.txt"
    o2 = sim.atmosphere.gases[3]
    o2.cia_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/o4_calc.cia'
    label = "Earth-Like"
    sim.set_planet_proxima_b()
    sim.set_star_proxima()


    sim.set_executables_automatically()
    sim.smartin.sza = 57

    sim.smartin.FWHM = res
    sim.smartin.sample_res = res

    sim.smartin.minwn = 1e4/lamax
    sim.smartin.maxwn = 1e4/lamin 

    sim.lblin.minwn = 1e4/lamax
    sim.lblin.maxwn = 1e4/lamin 

    sim.radstar = 0.1542

    sim.gen_lblscripts()
    sim.run_lblabc()
    sim.write_smart(write_file = True)
    sim.run_smart()
    
    sim.open_outputs()
    wl = sim.output.rad.lam
    sflux = sim.output.rad.sflux
    flux = sim.output.rad.pflux
    flux = flux/sflux
    fig, ax = plt.subplots(figsize = (10,10))
    plt.plot(wl, flux)
    name = "/gscratch/vsm/mwjl/projects/binary/plots/smart_"+str(pair)+str(i)+".png"

    fig.savefig(name, bbox_inches = "tight")

        
def smart_spectral_integ(pair,band,i, res):

    if band == 'a':
        lamin = 0.315
        lamax = 0.40
    elif band == 'b':
        lamin = 0.28
        lamax = 0.315
    elif band == 'c':
        lamin = 0.10
        lamax = 0.28
        
    infile = '/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info.dat'

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
    
    sim = smart.interface.Smart(tag = "prox")
    sim.set_run_in_place()

   # infile7 = "/gscratch/vsm/mwjl/projects/high_res/inputs/profile_Earth_proxb_.pt_filtered"
    sim.smartin.alb_file = "/gscratch/vsm/mwjl/projects/high_res/inputs/composite1_txt.txt"
    sim.set_planet_proxima_b()
    sim.load_atmosphere_from_pt("temp.pt", addn2 = True)
    if pair == "GG":
        sim.smartin.spec = "/gscratch/vsm/mwjl/projects/binary/plots/outGG.txt"
    elif pair == "GM":
        sim.smartin.spec = "/gscratch/vsm/mwjl/projects/binary/plots/outGM.txt"
    elif pair == "GK":
        sim.smartin.spec = "/gscratch/vsm/mwjl/projects/binary/plots/outGK.txt"
    o2 = sim.atmosphere.gases[3]
    o2.cia_file = '/gscratch/vsm/mwjl/projects/high_res/inputs/o4_calc.cia'
    label = "Earth-Like"
    sim.set_planet_proxima_b()
    sim.set_star_proxima()


    sim.set_executables_automatically()
    sim.smartin.sza = 57

    sim.smartin.FWHM = res
    sim.smartin.sample_res = res

    sim.smartin.minwn = 1e4/lamax
    sim.smartin.maxwn = 1e4/lamin 

    sim.lblin.minwn = 1e4/lamax
    sim.lblin.maxwn = 1e4/lamin 

    sim.radstar = 0.1542

    sim.gen_lblscripts()
    sim.run_lblabc()
    sim.write_smart(write_file = True)
    sim.run_smart()
    
    sim.open_outputs()
    wl = sim.output.rad.lam
    sflux = sim.output.rad.sflux
    flux = sim.output.rad.pflux
    flux = flux/sflux
    fig, ax = plt.subplots(figsize = (10,10))
    plt.plot(wl, flux)
    name = "/gscratch/vsm/mwjl/projects/binary/plots/smart_"+str(band)+str(pair)+str(i)+".png"

    fig.savefig(name, bbox_inches = "tight")


if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="nor_plt",
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
        smart_spectral('GG', 1000, 0.01)
    else:
        smart_spectral(0.75,0.76, 'GG')


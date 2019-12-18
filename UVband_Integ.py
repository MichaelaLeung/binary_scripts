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

from spectral_weights import smart_spectral_integ

def integrate(pair, band, h):
    print("integrate")
    f = open("/gscratch/vsm/mwjl/projects/binary/scripts/integrations.txt", "a")
    wl, flux = smart_spectral_integ(pair, band, h, 0.1)
    wl_low, flux_low = smart_spectral_integ(pair, band, h, 10)

    long_flux = []
    for i in flux_low:
        j = 0
        while j < 101: 
            long_flux.append(i)
            j = j+1
    print(len(long_flux), len(flux))
    mixed = []
    i = 0
    while i < len(flux):
        temp = (flux[i] + long_flux[i]) / 2
        mixed.append(temp)
        i = i+1


    i = 0
    flattened = []
    while i < len(long_flux)- 25: 
        avg = np.mean(flux[i:i+25])
        j = 0
        while j < 25:
            flattened.append(avg)
            j = j+1
        i = i+25
        

    out = []
    i = 0
    while i < len(mixed[:-25]): 
        diff = abs(mixed[i] - flattened[i])
        out.append(diff)
        i = i+1

    import scipy.integrate as integrate
    adds = integrate.trapz(out, wl[:-25])
    print(adds)    
    name = str(abs(adds)), str(h), str(pair), str(band)
    f = open("/gscratch/vsm/mwjl/projects/binary/scripts/integrations.txt", "a")
    f.write(str(name) + "\n")
 #   return(pair, band, i)

def integrate_norm(pair, band, h):
    if band == 'a':
        lamin = 0.315
        lamax = 0.40
    elif band == 'b':
        lamin = 0.28
        lamax = 0.315
    elif band == 'c':
        lamin = 0.10
        lamax = 0.28
        
    f = open("/gscratch/vsm/mwjl/projects/binary/scripts/integrations.txt", "a")
    wl, flux = run_smart_toa(lamin, lamax, 0.01)
    wl_low, flux_low = run_smart_toa(lamin,lamax, 1)
    
    bi_wl, bi_flux = smart_spectral_integ(pair, band, h, 0.01)
    bi_wl_low, bi_flux_low = smart_spectral_integ(pair, band, h, 1)

    long_flux = []
    for i in flux_low:
        j = 0
        while j < 100: 
            long_flux.append(i)
            j = j+1

    mixed = []
    i = 0
    while i < len(flux):
        temp = (flux[i] + long_flux[i]) / 2
        mixed.append(temp)
        i = i+1


    i = 0
    flattened = []
    while i < len(long_flux)- 25: 
        avg = np.mean(flux[i:i+25])
        j = 0
        while j < 25:
            flattened.append(avg)
            j = j+1
        i = i+25
        

    out = []
    i = 0
    while i < len(mixed[:-25]): 
        diff = abs(mixed[i] - flattened[i])
        out.append(diff)
        i = i+1

    import scipy.integrate as integrate
    adds = integrate.trapz(out, wl[:-25])
    print(adds)    
    name = str(abs(adds)), str(i), str(pair)
    f = open("/gscratch/vsm/mwjl/projects/binary/scripts/integrations_norm.txt", "a")
    f.write(str(name) + "\n")
    
def output(pair,i):
    print("output")
    for i in values:
        integrate(pair, 'a', i)
        integrate(pair, 'b', i)
        integrate(pair, 'c', i)

def run_all():
    num = range(0,45000,1000)
    output("GG", num)
    output("GM", num)
if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="UV_integ",
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
        print("script submitted")
        run_all()
    else:
        output(6)


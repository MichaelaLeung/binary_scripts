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
print("imports")

def integrate(pair, band, h):
    print("integrate")
    f = open("/gscratch/vsm/mwjl/projects/binary/scripts/integrations.txt", "a")
    wl, flux = smart_spectral_integ(pair, band, h, 0.01)
    wl_low, flux_low = smart_spectral_integ(pair, band, h, 1)

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
    f = open("/gscratch/vsm/mwjl/projects/binary/scripts/integrations.txt", "a")
    f.write(str(name) + "\n")
 #   return(pair, band, i)

def output(pair,i):
    print("output")
    integrate(pair, 'a', i)
    integrate(pair, 'b', i)
    integrate(pair, 'c', i)

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
        output(5)
    else:
        output(6)

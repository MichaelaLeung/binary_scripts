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
from run_smart import run_smart_toa
from spectral_weights import smart_spectral 

def normalize(pair,i):
    wl, flux = run_smart_toa()
    bi_wl, bi_flux = smart_spectral(pair,i)
    norm_flux = bi_flux/flux
    fig, ax = plt.subplots(figsize = (10,10))
    plt.plot(wl, flux)
    name = "/gscratch/vsm/mwjl/projects/binary/plots/norm"+str(pair)+str(i)+".png"
    fig.savefig(name, bbox_inches = "tight")

if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="normalize",
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
        normalize('GG', 1000)
    else:
        normalize('GG', 1000)


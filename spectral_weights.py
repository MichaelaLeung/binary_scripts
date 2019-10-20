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

def spectral_weights(pair):
    if pair == 'GG':
        infile = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/GGTweights.csv'
        G_star = '/gscratch/vsm/mwjl/packages/photochem_smart/fixed_input/specs/Sun.dat'
        stell = '/gscratch/vsm/mwjl/packages/photochem_smart/fixed_input/specs/Sun.dat'
        weights = np.genfromtxt(infile)
        weight = weights[1]
 
        G = np.genfromtxt(G_star)
        print(np.shape(G), np.shape(weights)) 
        G = G[1]
        print(weight, G)
        G_out = weight * G
        wl = G[0]
        return(wl, G_out,G_out)
    if pair == 'GK':
        infile = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/GKTweights.csv'
        G_star = '/gscratch/vsm/mwjl/packages/photochem_smart/fixed_input/specs/Sun.dat'
        K_star = '/gscratch/vsm/mwjl/packages/photochem_smart/fixed_input/specs/Sun.dat'
        weights = np.genfromtxt(infile)
        weight = weights[1]
        G = np.genfromtxt(G_star)
        G = G[1]
        G_out = weight * G
        wl = G[0]
        K = np.genfromtxt(K_star)
        K = K[1]
        K_out = weight * K
        wl = G[0]
        return(wl, G_out,K_out)
    if pair == 'GM':
        infile = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/GKT_weights.csv'
        G_star = '/gscratch/vsm/mwjl/packages/photochem_smart/fixed_input/specs/Sun.dat'
        stell = '/gscratch/vsm/mwjl/packages/photochem_smart/fixed_input/specs/ADLeo.dat'
        weights = np.genfromtxt(infile)
        weight = weights[1]
        G = np.genfromtxt(G_star)
        G = G[1]
        G_out = weight * G
        wl = G[0]
        M = np.genfromtxt(M_star)
        M = M[1]
        M_out = weight * M
        wl = G[0]
        return(wl, G_out,M_out)

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
        spectral_weights('GG')
    else:
        spectral_weights('GG')

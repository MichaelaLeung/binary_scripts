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


from mixing_ratio_plot import plot_mixingratios
from csv_convert import csv_convert
from run_smart import run_smart
from o3_plot import plot_o3
from mixing_ratio_plot import run_plots

def run_twostars(pair):
    if pair == "GG":
        os.chdir("/gscratch/vsm/mwjl/projects/binary/twostarsGG/")
        subprocess.call(["make"])
        subprocess.call(["./twostars3"])
    elif pair == "GK":
        os.chdir("/gscratch/vsm/mwjl/projects/binary/twostarsGG/")
        subprocess.call(["make"])
        subprocess.call(["./twostars3"])
    elif pair == "GM":
        os.chdir("/gscratch/vsm/mwjl/projects/binary/twostarsGM/")
        subprocess.call(["make"])
        subprocess.call(["./twostars3"]) 

def run_csv_conversion(pair):
    csv_convert(pair)

def run_multiflare(pair):
    os.chdir("/gscratch/vsm/mwjl/projects/binary/multiflare")
    if pair == "GG":
        subprocess.call(["./recover"], shell = True)
        copyfile("input_ggbin", "input")
        subprocess.call(["./circumbinary"], shell = True)
    elif pair == "GK":
        subprocess.call(["./recover"], shell = True)
        copyfile("input_gkbin", "input")
        subprocess.call(["./circumbinary"], shell = True)
    elif pair == "GM":
        subprocess.call(["./recover"], shell = True)
        copyfile("input_gmbin", "input")
        subprocess.call(["./circumbinary"], shell = True)      
        

def run_plots(values, pair):        
    run_plots(values,pair)
    plot_o3("/gscratch/vsm/mwjl/projects/binary/multiflare/io/o3coldepth.dat", pair)

        
def run_smart_multi(values):
    for i in values:
        run_smart("/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info.dat", i)

def run_all(pair, values):
    run_twostars(pair)
    run_csv_conversion(pair)
    run_multiflare(pair)
    run_plots(values, pair)

def run_all_smart(pair,values):
    run_twostars(pair)
    run_csv_conversion(pair)
    run_multiflare(pair)
    run_plots(values)
    run_smart_multi(values)


if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="run_binary",
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
        run_all("GK", [1,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000])
    else:
        run_all("GG", 5)

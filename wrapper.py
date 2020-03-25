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
import imageio

from mixing_ratio_plot import plot_mixingratios
from csv_convert import csv_convert
from run_smart import run_smart_toa
from o3_plot import plot_o3
from mixing_ratio_plot import run_plots
from spectral_weights import smart_spectral
from UVband_Integ import output
from mixing_ratio_plot import run_plots
from norm import normalize
from phase_temperature import phase_temp

def run_twostars(pair):
    if pair == "GG":
        os.chdir("/gscratch/vsm/mwjl/projects/binary/twostarsGG/")
        subprocess.call(["make"])
        subprocess.call(["./twostars3"])
    elif pair == "GK":
        os.chdir("/gscratch/vsm/mwjl/projects/binary/twostarsGK/")
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
        subprocess.call(["make"])
        subprocess.call(["./recover"], shell = True)
        copyfile("input_ggbin", "input")
        subprocess.call(["./circumbinary"], shell = True)
    elif pair == "GK":
        subprocess.call(["make"])
        subprocess.call(["./recover"], shell = True)
        copyfile("input_gkbin", "input")
        subprocess.call(["./circumbinary"], shell = True)
    elif pair == "GM":
        subprocess.call(["make"])
        subprocess.call(["./recover"], shell = True)
        copyfile("input_gmbin", "input")
        subprocess.call(["./circumbinary"], shell = True)      
        

def run_plots_multi(values, pair):        
    run_plots(values,pair)
    plot_o3("/gscratch/vsm/mwjl/projects/binary/multiflare/io/o3coldepth.dat", pair)

def plot_test(values, pair): 
    run_plots(values, pair)

def test_plot():
    run_plots([100,200,300,400,500], "GG")        

def run_smart_multi(values,pair):
    for i in values:
        smart_spectral(pair,i)
    inputs = []
    for i in values:
        name = "/gscratch/vsm/mwjl/projects/binary/plots/smart_"+str(pair)+str(i)+".png"
        inputs.append(name)
    plt.figure(figsize=(4,4))
    gif_path = str(pair) + "_smart.gif"
    with imageio.get_writer(gif_path, mode='I') as writer:
        for i in range(len(inputs)):
            writer.append_data(imageio.imread(inputs[i].format(i=i)))    

def integration_multi(values, pair): 
    for i in values:
        output(pair, i)

def normalize_multi(pair,values):
    for i in values:
        normalize(pair,i)
    
 
def run_all(pair,values):
    sys.setrecursionlimit(15000)
    run_twostars(pair)
    print('************************************************* twostars complete *************************************************') 
    run_csv_conversion(pair)
    print('*************************************************** csv conversion complete *****************************************') 
    run_multiflare(pair)
    run_plots_multi(values, pair)
    print('******************************************************* run plots complete *******************************************') 
    run_smart_multi(values,pair)
    print('******************************************************* run smart complete ********************************************') 
    integration_multi(values, pair)
    print('********************************************************run integration complete ************************************')
    normalize_multi(values, pair)
    print('********************************************************normalization complete ***********************************')

def prelim_run():
    sys.setrecursionlimit(15000)
    pair_list = "GM", "GG"
    values = range(0,45000,100)
    for pair in pair_list:
        run_twostars(pair)
        run_csv_conversion(pair)
        run_multiflare(pair)
        run_plots_multi(values, pair)
        phase_temp(pair)

if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="prelim_run",
                               subname="submit.csh",
                               workdir = "",
                               nodes = 1,
                               mem = "500G",
                               walltime = "72:00:00",
                               ntasks = 28,
                               account = "vsm",
                               submit = True,
                               rm_after_submit = True)
    elif platform.node().startswith("n"):
        # On a mox compute node: ready to run
        prelim_run()
#        run_multiflare('GG')
        num = range(1,20000,100)
        run_plots_multi(num, "GM")
#        run_all_smart("GM", num)
    else:
        run_all("GG", 5)

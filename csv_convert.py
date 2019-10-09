import numpy as np
import matplotlib;matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from astropy.io import fits
import sys, os
import datetime
matplotlib.rcParams['text.usetex'] = False
import random
import math 
import csv
import smart

def csv_convert(pair):
    if pair == "GG":
        infile = "/gscratch/vsm/mwjl/projects/binary/multiflare/data/GGTweights_temp.csv"
        outfile = "/gscratch/vsm/mwjl/projects/binary/multiflare/data/GGTweights.csv"
    elif pair == "GK":
        infile = "/gscratch/vsm/mwjl/projects/binary/multiflare/data/GKTweights_temp.csv"
        outfile = "/gscratch/vsm/mwjl/projects/binary/multiflare/data/GKTweights.csv"
    elif pair == "GM":
        infile = "/gscratch/vsm/mwjl/projects/binary/multiflare/data/GMTweights_temp.csv"
        outfile = "/gscratch/vsm/mwjl/projects/binary/multiflare/data/GMTweights.csv"
    time_added = []
    data = []
    with open(infile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row)
    data = data[1:]
    i = 1
    for line in data:
        line.insert(0,i*864)
        time_added.append(line)
        i = i+1
    with open(infile) as f:
        first_line = f.readline()
    with open(outfile, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(time_added)

if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="CSV_convert",
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
        csv_convert("GG")
        csv_convert("GK")
        csv_convert("GM")
    else:
        csv_convert("GG")

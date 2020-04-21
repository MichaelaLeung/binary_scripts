#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:06:25 2020

@author: mwl
"""
import smart
from master_plot import run_plots
from tsi_math import tsi_math

def looper():
    # output_list is the tag for spectra_info files in order from smallest to largest sma 
    output_list = '41616GG', '4170GG', '41719GG', '42019GG' 
    for i in output_list: 
        run_plots(i)
        tsi_math(i)
        
if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="co_test",
                               subname="submit.csh",
                               workdir = "",
                               nodes = 1,
                               mem = "500G",
                               walltime = "24:00:00",
                               ntasks = 28,
                               account = "vsm",
                               submit = True,
                               rm_after_submit = True)
    elif platform.node().startswith("n"):
        # On a mox compute node: ready to run
        looper()
#    else:
        # Presumably, on a regular computer: ready to run
        looper()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:17:34 2020

@author: mwl
"""
import numpy as np
import smart 

def tsi_math():
    temp = np.genfromtxt('/gscratch/vsm/mwjl/projects/binary/multiflare/clima/io/solint.pdat')
    out = np.mean(temp)
    f = open('avgs.txt', 'a')
    f.write('TSI:', out)
    f.close()
    
if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="tsi-py",
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
        tsi_math()
    else:
        tsi_math()
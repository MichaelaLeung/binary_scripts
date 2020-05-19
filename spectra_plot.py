#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:22:21 2020

@author: mwl
"""
import csv 
import matplotlib.pyplot as plt
import smart 
import imageio
import numpy as np

def spectra_plot(): 
    data = []
    csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/twostars3_out_bndflux1.csv'
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(list(row))
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    f_wn = []
    wn = data[1]
    wn = list(wn)
    for v in wn[:-1]: 
        print(v)
        out = float(v)
        f_wn.append(out)
    g_star_path = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/g2v_photo.pdat'
    g_star = np.genfromtxt(g_star_path)
    g_flux = g_star[1]
    i = 0
    data = data[2:]
    for row in data: 
        temp = []
        row = row[:-1]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        out = f_wn - g_flux
        ax.plot(f_wn, out)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowG'+str(i) + '.png')
    m_star_path = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/adleo_photo.pdat'
    m_star = np.genfromtxt(m_star_path)
    m_flux = m_star[1]
    csv_path2 = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/twostars3_out_bndflux2.csv'
    with open(csv_path2) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
       data.append(list(row))
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    f_wn = []
    wn = data[1]
    wn = list(wn)
    for v in wn[:-1]: 
        print(v)
        out = float(v)
        f_wn.append(out)
    i = 0
    data = data[2:]
    for row in data: 
        temp = []
        row = row[:-1]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        out = temp - m_flux
        ax.plot(f_wn, out)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowM'+str(i) + '.png')

    nums = range(1,108)
    inputsM = []
    gif_pathM = '/gscratch/vsm/mwjl/projects/binary/plots/M_star.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowM"+str(i)+".png"
        inputsM.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_pathM, mode='I') as writer:
        for i in range(len(inputsM)):
            writer.append_data(imageio.imread(inputsM[i].format(i=i)))

    inputsG = []
    gif_pathG = '/gscratch/vsm/mwjl/projects/binary/plots/G_star.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowG"+str(i)+".png"
        inputsG.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_pathG, mode='I') as writer:
        for i in range(len(inputsG)):
            writer.append_data(imageio.imread(inputsG[i].format(i=i)))
        
    
if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="specplt",
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
        spectra_plot()

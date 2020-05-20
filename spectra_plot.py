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
    f_wl = []
    wn = data[1]
    wn = list(wn)
    for v in wn[:-1]: 
        print(v)
        out = 10000 / float(v)
        f_wl.append(out)
    i = 0
    data = data[2:]
    while i < 1000: 
        temp = []
        row = row[:-1]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(f_wl[:len(temp)], temp[:len(f_wl)])
        ax.set_xlim(0,5)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowG'+str(i) + '.png')
    csv_path2 = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/twostars3_out_bndflux2.csv'
    with open(csv_path2) as csvfile2:
        readCSV = csv.reader(csvfile2, delimiter=',')
        for row in readCSV:
            data.append(list(row))
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    f_wl = []
    wn = data[1]
    wn = list(wn)
    for v in wn[:-1]: 
        print(v)
        out = 10000 / float(v)
        f_wl.append(out)
    i = 0
    data = data[2:]
    while i < 1000: 
        temp = []
        row = row[:-1]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(f_wl[:len(temp)], temp[:len(f_wl)])
        ax.set_xlim(0,5)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowM'+str(i) + '.png')

    nums = range(1,108)
    inputsM = []
    gif_pathM = '/gscratch/vsm/mwjl/projects/binary/plots/M_star_diff.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowM"+str(i)+".png"
        inputsM.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_pathM, mode='I') as writer:
        for i in range(len(inputsM)):
            writer.append_data(imageio.imread(inputsM[i].format(i=i)))

    inputsG = []
    gif_pathG = '/gscratch/vsm/mwjl/projects/binary/plots/G_star_diff.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowG"+str(i)+".png"
        inputsG.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_pathG, mode='I') as writer:
        for i in range(len(inputsG)):
            writer.append_data(imageio.imread(inputsG[i].format(i=i)))
            
def spectra_plot_diff(): 
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
        out = 10000 / float(v)
        f_wn.append(out)
    g_star_path = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/g2v_photo.pdat'
    g_star = np.genfromtxt(g_star_path, skip_header = 1)
    g_flux = g_star[:,1]
    i = 0
    data = data[2:]
    while i < 1000: 
        temp = []
        row = row[:-1]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        out = temp[:len(g_flux)] - g_flux[:len(temp)]
        ax.plot(f_wn[:len(out)], out[:len(g_flux)])
        ax.set_xlim(0,5)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowG_diff'+str(i) + '.png')
    m_star_path = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/adleo_photo.pdat'
    m_star = np.genfromtxt(m_star_path, skip_header = 1)
    m_flux = m_star[:,1]
    csv_path2 = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/twostars3_out_bndflux2.csv'
    with open(csv_path2) as csvfile2:
        readCSV = csv.reader(csvfile2, delimiter=',')
        for row in readCSV:
            data.append(list(row))
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    f_wn = []
    wn = data[1]
    wn = list(wn)
    for v in wn[:-1]: 
        print(v)
        out = 10000 / float(v)
        f_wn.append(out)
    i = 0
    data = data[2:]
    while i < 1000: 
        temp = []
        row = row[:-1]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        out = temp[:len(m_flux)] - m_flux[:len(temp)]
        ax.plot(f_wn[:len(out)], out[:len(f_wn)])
        ax.set_xlim(0,5)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowM_diff'+str(i) + '.png')

    nums = range(1,108)
    inputsM = []
    gif_pathM = '/gscratch/vsm/mwjl/projects/binary/plots/M_star_diff.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowM_diff"+str(i)+".png"
        inputsM.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_pathM, mode='I') as writer:
        for i in range(len(inputsM)):
            writer.append_data(imageio.imread(inputsM[i].format(i=i)))

    inputsG = []
    gif_pathG = '/gscratch/vsm/mwjl/projects/binary/plots/G_star_diff.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowG_diff"+str(i)+".png"
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
        spectra_plot_diff()

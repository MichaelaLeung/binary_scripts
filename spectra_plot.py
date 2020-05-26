#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:22:21 2020

@author: mwl
"""
import csv 
import matplotlib; matplotlib.use('agg')
import matplotlib.pyplot as plt
import smart 
import imageio
import numpy as np

def spectra_plot(pair): 
    data = []
    csv_path = '/gscratch/vsm/mwjl/projects/binary/twostars'+str(pair)+'/twostars3_out_bndflux1.csv'
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            row = row[:-1]
            data.append(list(row))
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    f_wl = []
    wn = data[1]
    wn = list(wn)
    for v in wn[:-1]: 
        out = 10000 / float(v)
        f_wl.append(out)
    i = 0
    data = data[2:]
    while i < 20: 
        temp = []
        row = data[i]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(f_wl[:len(temp)], temp[:len(f_wl)])
        ax.set_xlim(1,5)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowP'+str(i) + '.png')
    csv_path2 = '/gscratch/vsm/mwjl/projects/binary/twostars'+str(pair)+'/twostars3_out_bndflux2.csv'
    with open(csv_path2) as csvfile2:
        readCSV = csv.reader(csvfile2, delimiter=',')
        for row in readCSV:
            row = row[:-1]
            data.append(list(row))
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    print(wn,f_wl)
    while i < 20: 
        temp = []
        row = data[i]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(f_wl[:len(temp)], temp[:len(f_wl)])
        ax.set_xlim(1,5)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowS'+str(i) + '.png')

    nums = range(1,20)
    inputs2 = []
    gif_path2 = '/gscratch/vsm/mwjl/projects/binary/plots/Sec_star.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowS"+str(i)+".png"
        inputs2.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_path2, mode='I') as writer:
        for i in range(len(inputs2)):
            writer.append_data(imageio.imread(inputs2[i].format(i=i)))

    inputs1 = []
    gif_path1 = '/gscratch/vsm/mwjl/projects/binary/plots/Pri_star.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowP"+str(i)+".png"
        inputs1.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_path1, mode='I') as writer:
        for i in range(len(inputs1)):
            writer.append_data(imageio.imread(inputs1[i].format(i=i)))
            
def spectra_plot_diff(pair): 
    data = []
    csv_path = '/gscratch/vsm/mwjl/projects/binary/twostars'+str(pair)+'/twostars3_out_bndflux1.csv'
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            row = row[:-1]
            data.append(list(row))
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    f_wn = []
    f_start = []
    wn = data[1]
    wn = list(wn)
    start = data[2]
    for v in wn[:-1]: 
        out = 10000 / float(v)
        f_wn.append(out)
    for v in start[:-1]: 
        f_start.append(float(v))
    i = 0
    data = data[2:]
    while i < 20: 
        row = data[i]
        temp = []
        out = []
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        zip_object = zip(f_start, temp) 
        for a,b in zip_object: 
           print((a-b)/a)
           out.append(a-b)
        ax.plot(f_wn, out)
        ax.set_xlim(1,5)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_row1_diff'+str(i) + '.png')
    csv_path2 = '/gscratch/vsm/mwjl/projects/binary/twostars'+str(pair)+'/twostars3_out_bndflux2.csv'
    with open(csv_path2) as csvfile2:
        readCSV = csv.reader(csvfile2, delimiter=',')
        for row in readCSV:
            row = row[:-1]
            data.append(list(row))
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    f_start_m = []
    start_m = data[2]
    for v in start_m[:-1]:
        f_start_m.append(float(v))
    i = 0
    data = data[2:]
    while i < 20:
        row = data[i] 
        temp = []
        out = []
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        zip_object = zip(f_start_m, temp) 
        for a,b	in zip_object: 
           out.append(a-b)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(f_wn, out)
        ax.set_xlim(1,5)
        i = i+1
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowS_diff'+str(i) + '.png')

    nums = range(1,20)
    inputs2 = []
    gif_path2 = '/gscratch/vsm/mwjl/projects/binary/plots/sec_star_diff.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowS_diff"+str(i)+".png"
        inputs2.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_path2, mode='I') as writer:
        for i in range(len(inputs2)):
            writer.append_data(imageio.imread(inputs2[i].format(i=i)))

    inputs1 = []
    gif_path1 = '/gscratch/vsm/mwjl/projects/binary/plots/pri_star_diff.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowP_diff"+str(i)+".png"
        inputs1.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_path1, mode='I') as writer:
        for i in range(len(inputs1)):
            writer.append_data(imageio.imread(inputs1[i].format(i=i)))
        
    
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
        spectra_plot('GM')
        spectra_plot_diff('GM')

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

def chooser(pair): 
    path = '/gscratch/vsm/mwjl/projects/binary/multiflare/data/'
    if pair == 'GG':
        pri_star = path + 'g2v_photo.pdat'	
        sec_star = path + 'g2v_photo.pdat'	
        pri_star_uv = path + 'faruv_g2v.pdat' 
        sec_star_uv = path + 'faruv_g2v.pdat'
    if pair == 'GK': 
        pri_star =  path + 'g2v_photo.pdat'	
        sec_star =  path + 'k2v_photo.pdat'	
        pri_star_uv = path + 'faruv_g2v.pdat' 
        sec_star_uv = path + 'faruv_k2v.pdat'
    if pair == 'GM': 
        pri_star =  path + 'g2v_photo.pdat'	
        sec_star = path + 'adleo_photo.pdat'
        pri_star_uv = path + 'faruv_g2v.pdat' 
        sec_star_uv = path + 'faruv_adleo.pdat' 
    if pair == 'MK':
        pri_star =  path + 'adleo_photo.pdat'
        sec_star = path + 'k2v_photo.pdat'	
        pri_star_uv = path + 'faruv_adleo.pdat' 
        sec_star_uv = path + 'faruv_k2v.pdat' 
    weights = []
    weights_path = path + str(pair) + 'Tweights.csv'
    with open(weights_path) as weightsfile:
        readWeights = csv.reader(weightsfile, delimiter=',')
        for row in readWeights:
            weights.append(list(row))
            
    pri_spec = np.genfromtxt(pri_star)
    pri_spec_uv = np.genfromtxt(pri_star_uv)
    pri_wl = pri_spec[:,2]
    pri_spec = pri_spec[:,1]
    pri_spec_uv = pri_spec_uv[:,1]
    pri_wl_uv = pri_spec[:,2]
    
    sec_spec = np.genfromtxt(sec_star)
    sec_spec_uv = np.genfromtxt(sec_star_uv)
    sec_wl = sec_spec[:,2]
    sec_spec = sec_spec[:,1]
    sec_spec_uv = sec_spec_uv[:,1]
    sec_wl_uv = sec_spec[:,2]
    
    pri_out = pri_spec_uv.append(pri_spec)
    sec_out = sec_spec_uv.append(sec_spec)
    
    pri_out = pri_out * weights[0]
    sec_out = sec_out * weights[1]
    
    pri_wl = pri_wl_uv.append(pri_wl)
    sec_wl = sec_wl_uv.append(sec_wl)
    
    return(pri_out, sec_out, pri_wl, sec_wl)
        

def spectra_plot(pair): 
    pri_spec, sec_spec, pri_wl, sec_wl = chooser(pair)
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    i = 0
    while i < 1000:
        print(i, 'pri') 
        temp = []
        row = pri_spec[i]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(pri_wl[:len(temp)], temp[:len(pri_wl)])
        ax.set_xlim(1,5)
        ax.set_ylim(0, 5 * 10 **11)
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowP'+str(i) + '.png')
        i = i + 10

    j = 0
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    while j < 1000: 
        temp = []
        print(j, 'sec')
        row = sec_spec[j]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(sec_wl[:len(temp)], temp[:len(sec_wl)])
        ax.set_xlim(1,5)
        ax.set_ylim(0, 5 * 10**10)
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowS'+str(j) + '.png')
        j  =j + 10

    nums = range(0,1000,10)
    inputs2 = []
    gif_path2 = '/gscratch/vsm/mwjl/projects/binary/plots/Sec_star.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowS"+str(i)+".png"

        inputs2.append(name)
    plt.figure(figsize=(4,4))
    print(inputs2)
    with imageio.get_writer(gif_path2, mode='I') as writer:
        for k in range(len(inputs2)):
            writer.append_data(imageio.imread(inputs2[k].format(i=k)))

    inputs1 = []
    gif_path1 = '/gscratch/vsm/mwjl/projects/binary/plots/Pri_star.gif'
    for m in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowP"+str(m)+".png"
        inputs1.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_path1, mode='I') as writer:
        for m in range(len(inputs1)):
            writer.append_data(imageio.imread(inputs1[m].format(i=i)))
            
def spectra_plot_diff(pair): 
    pri_spec, sec_spec, pri_wl, sec_wl = chooser(pair)
    
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    i = 0 
    start = pri_spec[0]
    while i < 1000: 
        row = pri_spec[i]
        temp = []
        out = []
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        zip_object = zip(start, temp) 
        for a,b in zip_object: 
           print((a-b))
           out.append(a/b)
        ax.plot(pri_wl, out)
        ax.set_xlim(1,5)
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowP_diff'+str(i) + '.png')
        i = i + 10 

    data = []
    i = 0
    start_sec = sec_spec[0]
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    while i < 1000:
        row = sec_spec[i] 
        temp = []
        out = []
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        zip_object = zip(start_sec, temp) 
        for a,b	in zip_object: 
           out.append(a/b)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(sec_wl, out)
        ax.set_xlim(1,5)
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowS_diff'+str(i) + '.png')
        i = i + 10
    nums = range(0,1000,10)
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
        spectra_plot('GG')
        spectra_plot_diff('GG')

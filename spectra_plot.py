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
            weights.append(list(row[:-1]))
    weights = weights[1:]
    weights = np.asarray(weights, dtype = 'float64')
    print(np.shape(weights))            
    pri_spec = np.genfromtxt(pri_star, skip_header = 1, delimiter = (5,14,9,8))
    pri_spec_uv = np.genfromtxt(pri_star_uv, skip_header = 2, max_rows = 10, delimiter = (6,10))
    print(np.shape(pri_spec_uv))
    pri_wl = pri_spec[:,2]
    pri_spec = pri_spec[:,1]
    pri_wl_uv = pri_spec_uv[:,0]
    pri_spec_uv = pri_spec_uv[:,1]
    
    sec_spec = np.genfromtxt(sec_star, skip_header = 1, delimiter = (5,14,9,8))
    sec_spec_uv = np.genfromtxt(sec_star_uv, skip_header = 2, max_rows = 10, delimiter = (6,10))
    print(sec_spec_uv)
    sec_wl = sec_spec[:,2]
    sec_spec = sec_spec[:,1]
    sec_wl_uv = sec_spec_uv[:,0]
    sec_spec_uv = sec_spec_uv[:,1]
    
    pri_weights = weights[:,1]
    sec_weights = weights[:,2]
    pri_weights = np.transpose(pri_weights)
    sec_weights = np.transpose(sec_weights) 

    pri_spec = np.outer(pri_weights, pri_spec)
    sec_spec = np.outer(sec_weights, sec_spec)
    pri_spec_uv = np.outer(pri_weights, pri_spec_uv)
    sec_spec_uv = np.outer(sec_weights, sec_spec_uv)
    
    return(pri_wl, pri_spec, pri_wl_uv, pri_spec_uv, sec_wl, sec_spec, sec_wl_uv, sec_spec_uv)
        

def spectra_plot(pair): 
    pri_wl, pri_spec, pri_wl_uv, pri_spec_uv, sec_wl, sec_spec, sec_wl_uv, sec_spec_uv = chooser(pair)
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    i = 0
    while i < 1000:
        print(i, 'pri') 
        temp = []
        temp_uv = []
        row = pri_spec[i]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        row_uv = pri_spec_uv[i]
        for num in row_uv: 
            print(num)
            f_num_uv = float(num)
            temp_uv.append(f_num_uv)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(pri_wl[:len(temp)], temp[:len(pri_wl)])
        ax.plot(pri_wl_uv, temp_uv)
#        ax.set_xlim(1,5)
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
 #       ax.set_xlim(1,5)
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
    pri_wl, pri_spec, pri_wl_uv, pri_spec_uv, sec_wl, sec_spec, sec_wl_uv, sec_spec_uv = chooser(pair)
    
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
  #      ax.set_xlim(1,5)
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
 #       ax.set_xlim(1,5)
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

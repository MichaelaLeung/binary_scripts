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
    pri_delim = (5,14,9,8)
    if pair == 'GG':
        pri_star = path + 'g2v_photo.pdat'	
        sec_star = path + 'g2v_photo.pdat'	
        pri_star_uv = path + 'faruv_g2v.pdat' 
        sec_star_uv = path + 'faruv_g2v.pdat'
        sec_delim = (5,14,9,8)
    if pair == 'GK': 
        pri_star =  path + 'g2v_photo.pdat'	
        sec_star =  path + 'k2v_photo.pdat'	
        pri_star_uv = path + 'faruv_g2v.pdat' 
        sec_star_uv = path + 'faruv_k2v.pdat'
        sec_delim = (8,10,8,6)
    if pair == 'GM': 
        pri_star =  path + 'g2v_photo.pdat'	
        sec_star = path + 'adleo_photo.pdat'
        pri_star_uv = path + 'faruv_g2v.pdat' 
        sec_star_uv = path + 'faruv_adleo.pdat'
        sec_delim = (8,10,8,6) 
    if pair == 'MK':
        pri_star =  path + 'adleo_photo.pdat'
        sec_star = path + 'k2v_photo.pdat'	
        pri_star_uv = path + 'faruv_adleo.pdat' 
        sec_star_uv = path + 'faruv_k2v.pdat'
        sec_delim = (8,10,8,6)
        pri_delim = (8,10,8,6) 
    weights = []
    weights_path = path + str(pair) + 'Tweights.csv'
    with open(weights_path) as weightsfile:
        readWeights = csv.reader(weightsfile, delimiter=',')
        for row in readWeights:
            weights.append(list(row[:-1]))
    weights = weights[1:]
    weights = np.asarray(weights, dtype = 'float64')
#    print(np.shape(weights))            
    pri_spec = np.genfromtxt(pri_star, skip_header = 1, delimiter = pri_delim)
    pri_spec_uv = np.genfromtxt(pri_star_uv, skip_header = 2, max_rows = 10, delimiter = (6,10))
    pri_wl = pri_spec[:,2]
    pri_spec = pri_spec[:,1]
    pri_wl_uv = pri_spec_uv[:,0]
    pri_spec_uv = pri_spec_uv[:,1]
    
    sec_spec = np.genfromtxt(sec_star, skip_header = 1, delimiter = sec_delim)
    sec_spec_uv = np.genfromtxt(sec_star_uv, skip_header = 2, max_rows = 10, delimiter = (6,10))
    sec_wl = sec_spec[:,2]
    sec_spec = sec_spec[:,1]
    sec_wl_uv = sec_spec_uv[:,0]
    sec_spec_uv = sec_spec_uv[:,1]
    print(sec_spec_uv)    
    pri_weights = weights[:,1]
    sec_weights = weights[:,2]
    pri_weights = np.transpose(pri_weights)
    sec_weights = np.transpose(sec_weights) 

    pri_spec = np.outer(pri_weights, pri_spec)
    sec_spec = np.outer(sec_weights, sec_spec)
    pri_spec_uv = np.outer(pri_weights, pri_spec_uv)
    sec_spec_uv = np.outer(sec_weights, sec_spec_uv)

    pri_wl = 10000 / pri_wl 
    sec_wl = 10000/ sec_wl    
    pri_wl_uv = pri_wl_uv /10000 
    sec_wl_uv = sec_wl_uv/10000
    print(sec_spec_uv)
    return(pri_wl, pri_spec, pri_wl_uv, pri_spec_uv, sec_wl, sec_spec, sec_wl_uv, sec_spec_uv, pair)
        

def spectra_plot(pair): 
    g_max = 5*10**11
    m_max = 2*10**12
    pri_wl, pri_spec, pri_wl_uv, pri_spec_uv, sec_wl, sec_spec, sec_wl_uv, sec_spec_uv,pair = chooser(pair)
    i = 0
    while i < 1000:
        temp = []
        temp_uv = []
        row = pri_spec[i]
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        row_uv = pri_spec_uv[i]
        for num in row_uv: 
            f_num_uv = float(num)
            temp_uv.append(f_num_uv)
        fig,ax = plt.subplots(2,2, figsize = (20,20))
        if pair == 'MK':
            ymax = m_max
            uv_max = 10 ** 8
        else:
            ymax = g_max
            uv_max = 10 **6
        temp_sec = []
        temp_sec_uv = []
        row_sec = sec_spec[i]
        for num in row_sec:
            f_num = float(num)
            temp_sec.append(f_num)
        row_sec_uv = sec_spec_uv[i]
        for num in row_sec_uv: 
            f_num_uv = float(num)
            temp_sec_uv.append(f_num_uv)

        ax[1,1].plot(sec_wl[:len(temp)], temp_sec[:len(sec_wl)])
        ax[1,0].plot(sec_wl_uv, temp_sec_uv)
        ax[1,1].set_xlim(1,5)
        ax[1,0].set_xlim(0.1, 0.2)
        ax[1,1].set_ylim(0, ymax)
        ax[1,0].set_ylim(0,uv_max)
        
        ax[0,1].plot(pri_wl[:len(temp)], temp[:len(pri_wl)])
        ax[0,0].plot(pri_wl_uv, temp_uv)
        ax[0,1].set_xlim(1,5)
        ax[0,0].set_xlim(0.1, 0.2)
        ax[0,1].set_ylim(0, ymax)
        ax[0,0].set_ylim(0,uv_max)
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_row'+str(i) + str(pair)+'.png')
        i = i + 10
    nums = range(0,1000,10)
    inputs2 = []
    gif_path2 = '/gscratch/vsm/mwjl/projects/binary/plots/spectra_'+str(pair)+'.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_row"+str(i)+str(pair)+".png"
        inputs2.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_path2, mode='I') as writer:
        for k in range(len(inputs2)):
            writer.append_data(imageio.imread(inputs2[k].format(i=k)))

            
def spectra_plot_diff(pair): 
    pri_wl, pri_spec, pri_wl_uv, pri_spec_uv, sec_wl, sec_spec, sec_wl_uv, sec_spec_uv, pair  = chooser(pair)
    print('sec spec uv', sec_spec_uv)    
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    i = 0 
    start = pri_spec[0]
    start_uv = pri_spec_uv[0]
    while i < 1000: 
        row = pri_spec[i]
        row_uv = pri_spec_uv[i]
        temp = []
        temp_uv = []
        out = []
        out_uv = []
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        temp_uv = []
        for num_uv in row_uv:
            f_num_uv = float(num_uv)
            temp_uv.append(f_num_uv)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        zip_object = zip(start, temp) 
        for a,b in zip_object: 
#           print((a-b))
           out.append(a/b)
        zip_object_uv = zip(start_uv, temp_uv) 
        for a,b in zip_object_uv: 
  #         print((a/b))
           out_uv.append(a/b)
        ax.plot(pri_wl, out)
        ax.plot(pri_wl_uv, out_uv)
        ax.set_xlim(0.1,5)
        ax.set_ylim(0.8,1.2)
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowP_diff'+str(i) + str(pair)+'.png')
        i = i + 10 

    data = []
    i = 0
    start_sec = sec_spec[0]
    start_sec_uv = sec_spec_uv[0]
    fig,ax = plt.subplots(1,1, figsize = (10,10))
    while i < 1000:
        row = sec_spec[i] 
        row_uv = sec_spec_uv[i]
        temp = []
        temp_uv = []
        out = []
        out_uv = []
        for num in row:
            f_num = float(num)
            temp.append(f_num)
        for num in row_uv:
            f_num = float(num)
            temp_uv.append(f_num)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        zip_object = zip(start_sec, temp) 
        for a,b in zip_object: 
#           print((a-b))
           out.append(a/b)
#        print('************* temp uv *********', np.shape(temp_uv))
        zip_object_uv = zip(start_sec_uv, temp_uv) 
        for a,b in zip_object_uv: 
#           print('ab', a,b)
           out_uv.append(a/b)
        fig,ax = plt.subplots(1,1, figsize = (10,10))
        ax.plot(sec_wl, out)
        ax.plot(sec_wl_uv, out_uv)
        ax.set_xlim(0.1,5)
        ax.set_ylim(0.8,1.2)
        fig.savefig('/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowS_diff'+str(i) +str(pair)+ '.png')
        i = i + 10
    nums = range(0,1000,10)
    inputs2 = []
    gif_path2 = '/gscratch/vsm/mwjl/projects/binary/plots/sec_star_diff'+str(pair)+'.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowS_diff"+str(i)+str(pair)+".png"
        inputs2.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_path2, mode='I') as writer:
        for i in range(len(inputs2)):
            writer.append_data(imageio.imread(inputs2[i].format(i=i)))

    inputs1 = []
    gif_path1 = '/gscratch/vsm/mwjl/projects/binary/plots/pri_star_diff'+str(pair)+'.gif'
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/scripts/scratch/wn_rowP_diff"+str(i)+str(pair)+".png"
        inputs1.append(name)
    plt.figure(figsize=(4,4))
    with imageio.get_writer(gif_path1, mode='I') as writer:
        for i in range(len(inputs1)):
            writer.append_data(imageio.imread(inputs1[i].format(i=i)))
            
def light_curve(pair):
    pri_wl, pri_spec, pri_wl_uv, pri_spec_uv, sec_wl, sec_spec, sec_wl_uv, sec_spec_uv,pair = chooser(pair)
    total_flux = pri_spec + sec_spec 
    total_flux_uv = pri_spec_uv + sec_spec_uv 
    i = 5 
    flux_out = total_flux[:,i]
    flux_out_uv = total_flux_uv[:,i]
    fig,ax = plt.subplots(2,1, fig_size = (10,10))
    ax[0].plot(range(len(flux_out)),flux_out)
    ax[1].plot(range(len(flux_out_uv)), flux_out_uv)   
    fig.savefig('/gscratch/vsm/mwjl/projects/binary/lightcurve_'+ str(pair)+'.png')     
    
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
        spectra_plot('GK')
        spectra_plot('GG')
        spectra_plot('MK')
#        spectra_plot_diff('GM')
      #  chooser('GM')

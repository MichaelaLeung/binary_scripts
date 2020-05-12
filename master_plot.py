#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:15:48 2020

@author: mwl
"""

import numpy as np
import matplotlib; matplotlib.use('agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['text.usetex'] = False 
import csv
import imageio
import smart
from o3_plot import plot_o3
def phase_temp(inf, pair):
    data = []
    infile = '/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info_'+str(inf)+'.dat'
    with open("/gscratch/vsm/mwjl/projects/binary/twostars" + str(pair)+ "/twostars3_out_general.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row[3:5])
    data = data[1:]
    star1 = []
    star2 = []
    for line in data: 
        temp = line[0]
        temp = temp.strip(" ")
        star1.append(float(temp))
        temp2 = line[1]
        temp2 = temp2.strip(" ")
        star2.append(float(temp2))

    t_star = [] # converting timescale to days
    t_star_temp = range(len(star1))
    for i in t_star_temp: 
        temp3 = float(i)
        temp3 = temp3 *0.1 
        t_star.append(temp3)
    t_star = t_star[10000:]
    t_star = t_star
    t_final = []
    o3_final = []
    co2_final = []
    o2_final = []
    h2o_final = []
    ch4_final = []
    n2o_final = []
    ch3cl_final = []
    block_length = 128
    skip_lines = 7

    i = 7000

    while i < 9500: 
        temp = np.genfromtxt(infile, skip_header = (1 + (block_length + skip_lines)*(i-1)), max_rows = block_length)
#        print(1+(block_length+ skip_lines)*(i-1))
        T = temp[-1:,1]
        O3 = temp[-1,2]
        CO2 = temp[-1,3]
        O2 = temp[-1:,4]
        H2O = temp[-1,5]
        CH4 = temp[-1,6]
        N2O = temp[-1,7]
        CH3Cl = temp[-1,8]
        t_final.append(float(T))
        o3_final.append(float(O3)* 10**9)
        co2_final.append(float(CO2))
        o2_final.append(float(O2))
        h2o_final.append(float(H2O)* 10**6)
        ch4_final.append(float(CH4))
        n2o_final.append(float(N2O))
        ch3cl_final.append(float(CH3Cl))
        i = i+1
    time = np.array(range(len(t_final)))        
    print("gases created") 

    matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
    matplotlib.rcParams['font.size'] = 28.0
    matplotlib.rc('text', usetex=False)
    plt.switch_backend('agg')
    fig, ax = plt.subplots(3,1,figsize = (15,32))
    ax[0].plot(time, t_final, label = "Temp")
  #  ax[1].plot(time, o3_final, label = "O3")
   # ax[2].plot(range(len(co2_final)), co2_final, label = "CO2")
   # ax[3].plot(range(len(o2_final)), o2_final, label = "O2")
    ax[2].plot(time, h2o_final, label = "H2O")
 #   ax[3].plot(range(len(ch4_final)), ch4_final, label = "CH4")
   # ax[4].plot(range(len(n2o_final)), n2o_final, label = "N2O")
   # ax[5].plot(range(len(ch3cl_final)), ch3cl_final, label = "CH3Cl")
    ax[0].set_xlabel("Time [days]")
    ax[0].set_ylabel("Temperature (K)")

    file = np.genfromtxt("/gscratch/vsm/mwjl/projects/binary/multiflare/io/o3coldepth"+str(inf) + '.dat", skip_header = 8001)
    data = []
    if pair == "GG":
        csv_path = "/gscratch/vsm/mwjl/projects/binary/twostarsGG/twostars3_out_general.csv"
    elif pair == "GK":
        csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/twostars3_out_general.csv'
    elif pair == "GM":
        csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGK/twostars3_out_general.csv'        
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row[3:5])
    solint = np.genfromtxt('/gscratch/vsm/mwjl/projects/binary/multiflare/io/solint_' + str(inf)+'pdat', skip_header=1000)
    o3 = []
    for line2 in file: 
        o3.append(float(line2[3]))
    time2 = np.linspace(0,2500, len(o3))
    ax[1].plot(time2,o3)

    ax[1].set_ylabel('O3 column depth (cm$^{-2}$)')

    ax[1].set_xlabel('Time [days]')
    
    temp_avg = np.mean(t_final)
    f = open('avgs.txt', 'w')
    out = str(temp_avg) + '\n'
    f.write(str(out))
    f.close()


    ax[2].set_ylabel("Gas abundance (ppm)")
    i = 2
    while i <= 2:
        ax[i].set_xlabel("Time [days]")
        i = i+1
    fig.savefig("/gscratch/vsm/mwjl/projects/binary/plots/phase_temp_both" + str(pair)+ "_long.png", bbox_inches = "tight")

def phase_temp_conly(inf, pair):
    data = []
    infile = '/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info_'+str(inf)+'.dat'

    with open("/gscratch/vsm/mwjl/projects/binary/twostars" + str(pair)+ "/twostars3_out_general.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row[3:5])
    data = data[1:]
    star1 = []
    star2 = []
    for line in data: 
        temp = line[0]
        temp = temp.strip(" ")
        star1.append(float(temp))
        temp2 = line[1]
        temp2 = temp2.strip(" ")
        star2.append(float(temp2))

    t_star = [] # converting timescale to days
    t_star_temp = range(len(star1))
    for i in t_star_temp: 
        temp3 = float(i) * 0.1
        temp3 = temp3 
        t_star.append(temp3)
    t_star = t_star[1000:]
 #   print(t_star)
    t_final = []
    o3_final = []
    co2_final = []
    o2_final = []
    h2o_final = []
    ch4_final = []
    block_length = 52
    skip_lines = 1
    i = 1000

    while i < 3500:
        print(i)
        print(1 + (block_length + skip_lines)*(i-1))
        temp = np.genfromtxt(infile, skip_header = (1 + (block_length + skip_lines)*(i-1)), max_rows = block_length)
        T = temp[-1:,1]
        O3 = temp[-1,2]
        CO2 = temp[-1,3]
        O2 = temp[-1:,4]
        H2O = temp[-1,5]
        CH4 = temp[-1,6]
        t_final.append(float(T))
        o3_final.append(float(O3)*10**9)
        co2_final.append(float(CO2))
        o2_final.append(float(O2))
        h2o_final.append(float(H2O)*10**6)
        ch4_final.append(float(CH4))
        i = i+1
    time = np.asarray(range(len(t_final))) * 100 
    matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
    matplotlib.rcParams['font.size'] = 28.0
    matplotlib.rc('text', usetex=False)
    plt.switch_backend('agg')
    fig, ax = plt.subplots(3,1,figsize = (15,32))
    ax[0].plot(range(len(t_final)), t_final, label = "Temp")
#    ax[1].plot(range(len(o3_final)), o3_final, label = "O3")
  #  ax[2].plot(t_star, co2_final, label = "CO2")
  #  ax[3].plot(t_star, o2_final, label = "O2")
    ax[2].plot(range(len(h2o_final)), h2o_final, label = "H2O")
  #  ax[3].plot(t_star, ch4_final, label = "CH4")
    ax[0].set_xlabel("Time [days]")
    ax[0].set_ylabel("Temperature (K)")

    file = np.genfromtxt("/gscratch/vsm/mwjl/projects/binary/multiflare/io/o3coldepth" + str(inf) + ".dat", skip_header = 1)
    data = []
    if pair == "GG":
        csv_path = "/gscratch/vsm/mwjl/projects/binary/twostarsGG/twostars3_out_general.csv"
    elif pair == "GK":
        csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/twostars3_out_general.csv'
    elif pair == "GM":
        csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGK/twostars3_out_general.csv'
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row[3:5])
    data = data[1001:]
#    solint = np.genfromtxt('/gscratch/vsm/mwjl/projects/binary/multiflare/io/solint_43017GG.pdat', skip_header=1000)
    o3 = []
    for line2 in file:
  #	 time.append(float(line2[1])/84600)  # original units are in seconds
        o3.append(float(line2[3]))
    time2 = np.linspace(0,3500, len(o3))
    ax[1].plot(time2,o3)

    ax[1].set_ylabel('O3 column depth (cm$^{-2}$)')

    ax[1].set_xlabel('Time [days]')

   
    temp_avg = np.mean(t_final)
    temp_med = np.median(t_final)
    f = open('avgs.txt', 'w')
    out = str(temp_avg) + ", " + str(temp_med)+'\n'
    f.write(str(out))
    f.close()
   
   # ax[1].set_ylabel("Gas abundance (ppb)")
    ax[2].set_ylabel("Gas abundance (ppm)")
 
 #   ax[0].set_title("Temperature")
 #   ax[1].set_title("Ozone") 
 #   ax[2].set_title("Water") 

    i = 1
    while i <= 2:
        ax[i].set_xlabel("Time [days]")
  #      ax[i].set_ylabel("Gas abundance")
 #       ax[i].legend()
        i = i+1
    fig.savefig("/gscratch/vsm/mwjl/projects/binary/plots/phase_temp" + str(pair)+ ".png", bbox_inches = "tight")

def plot_mixingratios(infile, i, pair, coupled):
    #setting up constants
    block_length = 128
    skip_lines = 7
    i = int(i)
    if coupled == False: 
        skip_lines = 1
        block_length = 52
    print(i, skip_lines, block_length)
    print((skip_lines + (block_length + skip_lines)*(i)))
    temp = np.genfromtxt(infile, skip_header = (1 + (block_length + skip_lines)*(i-1)), max_rows = block_length)
    print((skip_lines + (block_length + skip_lines)*(i))) 
#    print(temp)
    #separating out the gases, P and T
    gases = temp[:,2:]
    #print(gases)
    P = temp[:,0]
    T = temp[:,1]
    T2 = []
    for b in T:
        temp2 = float(b)
        T2.append(temp2)
    #plotting
    matplotlib.rc('font',**{'family':'serif','serif':['Computer Modern']})
    matplotlib.rcParams['font.size'] = 15.0
    matplotlib.rc('text', usetex=False)
    plt.switch_backend('agg')

    fig, ax = plt.subplots(figsize=(9,9))
    ax.plot(0,0,color="black", label="Temp.", ls="--")
    if coupled == True: 
       mol_names_str = "O3", "CO2", "O2", "H2O", "CH4", "N2O", "CH3Cl"
    else: 
           mol_names_str = "O3", "CO2", "O2", "H2O", "CH4"
    for k in range(len(mol_names_str)):
        print(gases[:,k], P, mol_names_str[k])
        ax.plot(gases[:,k], P, label=mol_names_str[k])
    ax.set_xlabel("Volume Mixing Ratio")
    ax.set_ylabel("Pressure [Pa]")
#    ax.set_xlim(10**(-15),1)
#    ax.set_ylim(10**5,30)   
    ax.loglog()
    ax.legend()

    axT = ax.twiny()
    axT.set_xlabel("Temperature [K]")
    axT.set_axisbelow(True)
    axT.set_xlim(180,320)    
    axT.plot(T2, P, color="black", label="Temperature", ls="--")
    fig_name = "/gscratch/vsm/mwjl/projects/binary/plots/" + str(i) + str(pair) + str(coupled) + ".png"
    fig.savefig(fig_name, bbox_inches = "tight")
            
def plot_o3(infile, pair):
    file = np.genfromtxt(infile, skip_header = 1)
    data = []
    if pair == "GG":
        csv_path = "/gscratch/vsm/mwjl/projects/binary/twostarsGG/twostars3_out_general.csv"
    elif pair == "GK":
        csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/twostars3_out_general.csv'
    elif pair == "GM":
        csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGK/twostars3_out_general.csv'        
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row[3:5])
    data = data[1:]
    star1 = []
    star2 = []

    for line in data: 
        temp = line[0]
        temp = temp.strip(" ")
        star1.append(float(temp))
        temp1 = line[1]
        temp1 = temp1.strip(" ")
        star2.append(float(temp1))
    
    t_star_final = []
    t_star = range(len(star1))
    for i in t_star: 
        t_star_final.append(i*1/100)
    
    time = []
    o3 = []
    for line2 in file: 
        time.append(float(line2[1])/84600)  # original units are in seconds 
        o3.append(float(line2[3]))

    fig, ax = plt.subplots(2,1, figsize = (20,12))

    ax[0].set_xlim(0,400)
    ax[1].set_xlim(0,400)

    ax[0].plot(time,o3)

    ax[1].plot(t_star_final, star1)
    ax[1].plot(t_star_final, star2)

    ax[0].set_ylabel('O3 column depth (cm$^{-2}$)')
    ax[0].set_xlabel('Time (days)')

    ax[1].set_xlabel('Time (days)')

    fig.savefig("/gscratch/vsm/mwjl/projects/binary/plots/" + str(pair)+"o3plot.png", bbox_inches = 'tight')
    
def plot_ptt(inf, coupled):
    #plots phase, tst and temperature 
    solint = np.genfromtxt('/gscratch/vsm/mwjl/projects/binary/multiflare/io/solint_' + str(inf) + '.pdat')
    block_length = 128
    skip_lines = 7
    infile = '/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info_' + str(inf) + '.dat'
    t_final = []
    data = []
    pair = inf[-2:]
    if coupled == False: 
        skip_lines = 1
        block_length = 52
    print(skip_lines, block_length)
    i = 0
    while i < 9000: 
        temp = np.genfromtxt(infile, skip_header = (skip_lines + (block_length + skip_lines)*(i)), max_rows = block_length)
        T = temp[-1:,1]
        t_final.append(float(T))
        i = i+1
    if pair == "GG":
        csv_path = "/gscratch/vsm/mwjl/projects/binary/twostarsGG/twostars3_out_general.csv"
    elif pair == "GK":
        csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGM/twostars3_out_general.csv'
    elif pair == "GM":
        csv_path = '/gscratch/vsm/mwjl/projects/binary/twostarsGK/twostars3_out_general.csv'        
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row[3:5])
    data = data[1:]
    star1 = []
    star2 = []

    for line in data: 
        temp = line[0]
        temp = temp.strip(" ")
        star1.append(float(temp))
        temp1 = line[1]
        temp1 = temp1.strip(" ")
        star2.append(float(temp1))
    
    t_star_final = []
    t_star = range(len(star1))
    for i in t_star: 
        t_star_final.append(i*1/100)
    fig, ax = plt.subplots(2,1,figsize = (25,10))
    ax[0].plot(solint, label = 'solint')
    t_clima = np.linspace(1,100000,9000)
    ax[1].plot(t_clima, t_final, label = 'surface temp')
    ax[2].plot(star1, label = 'star1')
    ax[2].plot(star2, label = 'star2')
    for i in 0,1: 
        ax[i].set_xlim(0,1000)
        ax[i].legend()
    fig.savefig("ptt_test.png")
    
    

def run_plots(inf, values, coupled):
    infile = '/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info_'+str(inf)+'.dat'
    pair = inf[-2:]
    for i in values:
        plot_mixingratios(inf,i, pair, coupled)
        print(i)
    gif_path = "/gscratch/vsm/mwjl/projects/binary/plots/" + str(pair) + ".gif"
    nums = values
    inputs = []
    for i in nums: 
        name = "/gscratch/vsm/mwjl/projects/binary/plots/"+str(i)+str(pair)+str(coupled)+".png"
        inputs.append(name)
    plt.figure(figsize=(4,4))

    with imageio.get_writer(gif_path, mode='I') as writer:
        for i in range(len(inputs)):
            writer.append_data(imageio.imread(inputs[i].format(i=i)))
            
    if coupled: 
        phase_temp(infile, pair)
        plot_o3(infile, pair)
    else: 
        phase_temp_conly(infile, pair)
        plot_o3(infile, pair)

if __name__ == '__main__':

    import platform

    if platform.node().startswith("mox"):
        # On the mox login node: submit job
        runfile = __file__
        smart.utils.write_slurm_script_python(runfile,
                               name="allplt",
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
        v1 = range(1, 99000,100)
#        phase_temp('/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info_5512GG.dat', 'GG')
     #   phase_temp_conly('/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info_5110GG.dat', 'GG')

        values = range(1, 4500,10)
#        run_plots("42221GG", v1, True)
#        out_list = ("43017GG", True), ("5110GG", False), ("518GM", True), ("5110GM", False)
#        gm_list = ("518GM", True), ("5110GM", False)
#        coupled_list = ("43017GG", True), ("5110GG", False)
#        for a,b in coupled_list: 
#            run_plots(a, values, b)
        run_plots("51120GK", values, True)
      #  plot_ptt("42019GG", False)
#        plot_mixingratios('/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info_41412GG.dat', 5000, 'GG', False)
#        plot_mixingratios('/gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info_4114GG.dat', 5000, 'GG', True)
    else:
        phase_temp()


import os
import datetime

def save_as(pair):
    src = 'gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info.dat'
    currentDT = datetime.datetime.now()
    time_out = str(currentDT.month)+str(currentDT.day)+str(currentDT.hour)
    out = 'gscratch/vsm/mwjl/projects/binary/multiflare/io/spectra_info_'+str(time_out)+str(pair)+'.dat'
    os.rename(src,out)
    

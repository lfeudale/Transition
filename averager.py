import numpy as np

from commons.time_interval import TimeInterval
from commons.Timelist import TimeList
from commons.mask import Mask
from commons import time_averagers
from commons.netcdf3 import write_2d_file

INPUTDIR="/pico/scratch/userexternal/gbolzon0/TRANSITION/FORCINGS/OUTPUT_16/"
OUT_T2d_NC="TEMP_surf.nc"
OUT_S2d_NC="SAL_surf.nc"
OUT_W2d_NC="WIND_surf.nc"

TI = TimeInterval('20130101','20160101',"%Y%m%d")


TL = TimeList.fromfilenames(TI, INPUTDIR,"T*.nc",prefix='T',dateformat="%Y%m%d-%H:%M:%S")

TheMask=Mask('/pico/home/usera07ogs/a07ogs00/OPA/V2C/etc/static-data/MED1672_cut/MASK/meshmask.nc')
Mask2d = TheMask.cut_at_level(0)
WEEK_REQUESTORS=TL.getWeeklyList(5)

#for req in WEEK_REQUESTORS[:1]:
for req in WEEK_REQUESTORS:
    ii,w=TL.select(req)
    filelist = [TL.filelist[k] for k in ii]                                                                                                     
    OUTFILE="ave_weekly/ave." + req.string + "-12:00:00.nc"
    print OUTFILE

    TEMP = time_averagers.TimeAverager3D(filelist, w, 'votemper', TheMask)
    SALI = time_averagers.TimeAverager3D(filelist, w, 'vosaline', TheMask)
    WIND = time_averagers.TimeAverager2D(filelist, w, 'sowindsp', TheMask)


    TEMP[ ~TheMask.mask ]=1.e+20
    SALI[ ~TheMask.mask ]=1.e+20
    write_2d_file(TEMP[0,:,:],'votemper',OUTFILE,Mask2d)
    write_2d_file(SALI[0,:,:],'vosaline',OUTFILE,Mask2d)
    write_2d_file(WIND,'sowindsp',OUTFILE,Mask2d)


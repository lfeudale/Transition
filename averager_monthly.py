import numpy as np

from commons.time_interval import TimeInterval
from commons.Timelist import TimeList
from commons.mask import Mask
from commons.submask import SubMask
from commons import time_averagers
from commons.dataextractor import DataExtractor
from basins import V2 as OGS
from commons.netcdf3 import write_2d_file
#from commons.netcdf3 import read_2d_file
#from commons.netcdf3 import read_3d_file


INPUTDIR="/pico/scratch/userexternal/gbolzon0/TRANSITION/FORCINGS/OUTPUT_16/"

TI = TimeInterval('20130101','20151231',"%Y%m%d")


TL = TimeList.fromfilenames(TI, INPUTDIR,"T*.nc",prefix='T',dateformat="%Y%m%d-%H:%M:%S")

TheMask=Mask('/pico/home/usera07ogs/a07ogs00/OPA/V2C/etc/static-data/MED1672_cut/MASK/meshmask.nc')
Mask2d = TheMask.cut_at_level(0)
#WEEK_REQUESTORS=TL.getWeeklyList(5)
MONTH_REQUESTORS=TL.getMonthlist()

nVars  = 3
nSub   =len(OGS.P.basin_list)
nFrames =TL.nTimes
M = np.zeros((nVars,nFrames,nSub), dtype=np.float32)

#for req in WEEK_REQUESTORS[:1]:
#for req in WEEK_REQUESTORS:
for req in MONTH_REQUESTORS:
    ii,w=TL.select(req)
    filelist = [TL.filelist[k] for k in ii]                                                                                                     
    OUTFILE="ave_monthly/ave." + req.string + "15-12:00:00.nc"
    print OUTFILE

    TEMP = time_averagers.TimeAverager3D(filelist, w, 'votemper', TheMask)
    SALI = time_averagers.TimeAverager3D(filelist, w, 'vosaline', TheMask)
    WIND = time_averagers.TimeAverager2D(filelist, w, 'sowindsp', TheMask)


    TEMP[ ~TheMask.mask ]=1.e+20
    SALI[ ~TheMask.mask ]=1.e+20
    write_2d_file(TEMP[0,:,:],'votemper',OUTFILE,Mask2d)
    write_2d_file(SALI[0,:,:],'vosaline',OUTFILE,Mask2d)
    write_2d_file(WIND,'sowindsp',OUTFILE,Mask2d)


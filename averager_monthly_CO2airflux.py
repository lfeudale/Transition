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


#INPUTDIR="/pico/scratch/userexternal/gbolzon0/TRANSITION/FORCINGS/OUTPUT_16/"
#INPUTDIR="/pico/scratch/userexternal/lfeudale/Transition/"
INPUTDIR="/pico/scratch/userexternal/lfeudale/Transition/weekly_unzipped/"
TI = TimeInterval('20130101','20151231',"%Y%m%d")

TL = TimeList.fromfilenames(TI, INPUTDIR,"ave*.nc",prefix='ave.',filtervar="CO2airflux",dateformat="%Y%m%d-%H:%M:%S")

TheMask=Mask('/pico/home/usera07ogs/a07ogs00/OPA/V2C/etc/static-data/MED1672_cut/MASK/meshmask.nc')
Mask2d = TheMask.cut_at_level(0)
#WEEK_REQUESTORS=TL.getWeeklyList(5)
MONTH_REQUESTORS=TL.getMonthlist()




nVars  = 1
nSub   =len(OGS.Pred.basin_list)
nFrames =TL.nTimes
M = np.zeros((nVars,nFrames,nSub), dtype=np.float32)

#for req in WEEK_REQUESTORS[:1]:
#for req in WEEK_REQUESTORS:
for req in MONTH_REQUESTORS:
    ii,w=TL.select(req)
    filelist = [TL.filelist[k] for k in ii]                                                                                                     
    OUTFILE="ave_monthly/ave." + req.string + "15-12:00:00.CO2airflux.nc"
    print OUTFILE

    CO2airflux = time_averagers.TimeAverager2D(filelist, w, 'CO2airflux', TheMask)

    write_2d_file(CO2airflux,'CO2airflux',OUTFILE,Mask2d)


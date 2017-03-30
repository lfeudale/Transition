import numpy as np

from commons.time_interval import TimeInterval

from commons.Timelist import TimeList
from commons.mask import Mask
from commons.submask import SubMask

from commons.netcdf3 import write_2d_file
from commons.dataextractor import DataExtractor
from basins import V2 as OGS

TI = TimeInterval('20130101','20160101',"%Y%m%d")
INPUTDIR="/pico/scratch/userexternal/lfeudale/Transition/daily_unzipped/"
vars= ["pCO2"]
TL = TimeList.fromfilenames(TI, INPUTDIR,"ave.*nc",prefix="ave.",filtervar=vars[0],dateformat="%Y%m%d-%H:%M:%S")

TheMask=Mask('/pico/home/usera07ogs/a07ogs00/OPA/V2C/etc/static-data/MED1672_cut/MASK/meshmask.nc')
Mask2d = TheMask.cut_at_level(0)
jpk, jpj, jpi = TheMask.shape

nVars=len(vars)
nSub   =len(OGS.P.basin_list)
nFrames =TL.nTimes

# parte lenta, fatta a monte #
BOOL_2D = np.zeros((jpj,jpi,nSub), np.bool)
for iSub, sub in enumerate(OGS.P):
            S=SubMask( sub, maskobject=Mask2d)
            bool_2d=S.mask_at_level(0)
            BOOL_2D[:,:,iSub] = bool_2d & TheMask.mask_at_level(200)


M = np.zeros((nVars,nFrames,nSub), dtype=np.float32)

for ivar, var in enumerate(vars):
    TL = TimeList.fromfilenames(TI, INPUTDIR,"ave.*nc",prefix="ave.",filtervar=var,dateformat="%Y%m%d-%H:%M:%S")
    for iFrame, filename in enumerate(TL.filelist):
        print filename
	if var == "pCO2":
	   M3d = DataExtractor(TheMask,filename,varname=var,dimvar=3).values
	   M2d = M3d[0,:,:]
#	else:
#	   M2d = DataExtractor(Mask2d,filename,varname=var, dimvar=2).values 
        
	for iSub, sub in enumerate(OGS.P):
		bool_2d = BOOL_2D[:,:,iSub]
		subbasin_values = M2d[bool_2d] #1d array
                subbasin_area   = Mask2d.area[bool_2d]
		Weight = subbasin_area.sum()
		Weighted_mean = (subbasin_values*subbasin_area).sum() /Weight
		M[ivar,iFrame,iSub] = Weighted_mean

np.save('MediepesateBIO_daily',M)


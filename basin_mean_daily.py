import sys
import numpy as np

from commons.time_interval import TimeInterval

from commons.Timelist import TimeList
from commons.mask import Mask
from commons.submask import SubMask

#from commons.netcdf3 import write_2d_file
from commons.dataextractor import DataExtractor
from basins import V2 as OGS



TI = TimeInterval('20130101','20160101',"%Y%m%d")
#INPUTDIR="/pico/scratch/userexternal/lfeudale/Transition/ave_weekly"
INPUTDIR="/pico/scratch/userexternal/gbolzon0/TRANSITION/FORCINGS/OUTPUT_16/"

#TL = TimeList.fromfilenames(TI, INPUTDIR,"ave.*nc",prefix='ave.',dateformat="%Y%m%d-%H:%M:%S")
TL = TimeList.fromfilenames(TI, INPUTDIR,"T*.nc",prefix='T',dateformat="%Y%m%d-%H:%M:%S")



TheMask=Mask('/pico/home/usera07ogs/a07ogs00/OPA/V2C/etc/static-data/MED1672_cut/MASK/meshmask.nc')
Mask2d = TheMask.cut_at_level(0)
jpk, jpj, jpi = TheMask.shape

nVars  = 3
nSub   =len(OGS.P.basin_list)
nFrames =TL.nTimes
M = np.zeros((nVars,nFrames,nSub), dtype=np.float32)

# parte lenta, fatta a monte #
BOOL_2D = np.zeros((jpj,jpi,nSub), np.bool)

for iSub, sub in enumerate(OGS.P):
            S=SubMask( sub, maskobject=Mask2d)
            bool_2d=S.mask_at_level(0)
            BOOL_2D[:,:,iSub] = bool_2d & TheMask.mask_at_level(200)


#for ivar, var in enumerate(['votemper','vosaline','sowindsp']):
for iFrame, filename in enumerate(TL.filelist):
	print filename
	TEMP = DataExtractor(TheMask,filename,varname='votemper', dimvar=3).values
        TEMP[ ~TheMask.mask ]=1.e+20
	TEMPsurf = TEMP[0,:,:]
	SALI = DataExtractor(TheMask,filename,varname='vosaline', dimvar=3).values
        SALI[ ~TheMask.mask ]=1.e+20
        SALIsurf = SALI[0,:,:]
	WIND = DataExtractor(Mask2d,filename,varname='sowindsp', dimvar=2).values


	for iSub, sub in enumerate(OGS.P):
            bool_2d = BOOL_2D[:,:,iSub]
	
	    TEMP_subbasin_values = TEMPsurf[bool_2d] #1d array
            SALI_subbasin_values = SALIsurf[bool_2d] #1d array
            WIND_subbasin_values = WIND[bool_2d] #1d array
            subbasin_area   = Mask2d.area[bool_2d]
            Weight = subbasin_area.sum()
	    M[0,iFrame,iSub] = (TEMP_subbasin_values*subbasin_area).sum() /Weight
            M[1,iFrame,iSub] = (SALI_subbasin_values*subbasin_area).sum() /Weight
            M[2,iFrame,iSub] = (WIND_subbasin_values*subbasin_area).sum() /Weight

np.save('Mediepesate_daily',M)
np.save('TIMELIST_days',TL.Timelist)

sys.exit()


#   	write_2d_file(TEMP[0,:,:],'votemper',OUTFILE,Mask2d)
#    	write_2d_file(SALI[0,:,:],'vosaline',OUTFILE,Mask2d)
#   	write_2d_file(WIND,'sowindsp',OUTFILE,Mask2d)

	
#for ivar, var in enumerate(['votemper','vosaline','sowindsp']):
#    for iFrame, filename in enumerate(TL.filelist):
#        print filename
#        M2d = DataExtractor(Mask2d,filename,varname=var, dimvar=2).values
#        #M2d[~Mask2d.mask[0,:,:]] = np.nan
#        for iSub, sub in enumerate(OGS.Pred):
#            #S=SubMask( sub, maskobject=Mask2d)
#            #bool_2d=S.mask_at_level(0)
#            bool_2d = BOOL_2D[:,:,iSub]
#            subbasin_values = M2d[bool_2d] #1d array
#            subbasin_area   = Mask2d.area[bool_2d]
#            Weight = subbasin_area.sum()
#            Weighted_mean = (subbasin_values*subbasin_area).sum() /Weight
#            M[ivar,iFrame,iSub] = Weighted_mean
#
#
#np.save('Mediepesate',M)
#np.save('TIMELIST_weeks',TL.Timelist)

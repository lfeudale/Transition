import numpy as np
from timeseries.plot import *
from basins import V2 as OGS
import itertools
import matplotlib.cm as cm
from commons.Timelist import TimeList

TLL=np.load("../../TIMELIST_days.npy")
TL=TimeList(TLL)
WEEK_REQUESTORS=TL.getWeeklyList(5)
#CO2cal_week_mean=np.zeros(len(WEEK_REQUESTORS),dtype=np.float32)

MONTH_REQUESTORS=TL.getMonthlist()
#CO2cal_month_mean=np.zeros(len(MONTH_REQUESTORS),dtype=np.float32)

YEAR_REQUESTORS=TL.getYearlist()
CO2cal_DAILY=np.load('../../CO2airflux_day_offline.npy')

for req in WEEK_REQUESTORS:
    ii,w=TL.select(req)

#freq  = ['month','week','day']
freq  = ['week','month']
#ccols = ['green','cyan','blue']
ccols = ['blue','green']

sub_names = ['ALB','swMw','swMe','nwM','nTYR','sTYR','nADR','sADR','AEG','wION','eION','nION','wLEV','nLEV','sLEV','eLEV','MED']
axs = ['ax0','ax1']


#fig,axs=plt.subplots(nrows=5,ncols=1)
#colors = cm.rainbow(np.linspace(0, 1, len(OGS.Pred.basin_list)))
#col = itertools.cycle(colors)

#for iSub, sub in enumerate(OGS.Pred.basin_list[:1]):
for iSub, sub in enumerate(OGS.P.basin_list):
       fig,axs=plt.subplots(nrows=len(axs)) #,ncols=1)
       fig.set_size_inches(10,8)
#      for ivar, var in enumerate(['CO2airflux']):

########################################################

       for kk, tf in enumerate(freq):
   	     if (tf == 'week'):
        		M_BIO=np.load('../../MediepesateBIO.npy')
        		CO2cal=np.load('../../CO2airflux_week_offline.npy')
        		TT=np.load("../../TIMELIST_weeks.npy")
			CO2cal_mean = np.zeros(len(WEEK_REQUESTORS),dtype=np.float32)
			TTL=TimeList(TT)
			YEAR_REQUESTORS_w=TTL.getYearlist()

			CO2mod_y  = np.zeros(len(WEEK_REQUESTORS),dtype=np.float32)
			CO2cal_y  = np.zeros(len(WEEK_REQUESTORS),dtype=np.float32)
                        CO2cal_mean_y = np.zeros(len(WEEK_REQUESTORS),dtype=np.float32)

	     		for jj,req in enumerate(WEEK_REQUESTORS):
        	     		ii,w=TL.select(req)
             			CO2cal_mean[jj]=CO2cal_DAILY[ii].mean()


#			for kk,yreq in enumerate(YEAR_REQUESTORS_w):
#				iy,wy=TTL.select(yreq)
#				CO2mod_y[kk]=M_BIO[1,iy,iSub].mean()
#				CO2cal_y[kk]=CO2cal[:,iSub].mean()
				

   	     elif (tf == 'month'):
        		M_BIO=np.load('../../MediepesateBIO_monthly.npy')
        		CO2cal=np.load('../../CO2airflux_month_offline.npy')
        		TT=np.load("../../TIMELIST_months.npy")
			CO2cal_mean = np.zeros(len(MONTH_REQUESTORS),dtype=np.float32)

                        TTL=TimeList(TT)
                        YEAR_REQUESTORS_w=TTL.getYearlist()

                        CO2mod_y  = np.zeros(len(MONTH_REQUESTORS),dtype=np.float32)
                        CO2cal_y  = np.zeros(len(MONTH_REQUESTORS),dtype=np.float32)
                        CO2cal_mean_y = np.zeros(len(MONTH_REQUESTORS),dtype=np.float32)

#             elif (tf == 'day'):
#                        M_BIO=np.load('../../MediepesateBIO_daily.npy')
#                        CO2cal=np.load('../../CO2airflux_day_offline.npy')
#                        TT=np.load("../../TIMELIST_days.npy")

                	for jj,req in enumerate(MONTH_REQUESTORS):
                        	ii,w=TL.select(req)
                        	CO2cal_mean[jj]=CO2cal_DAILY[ii].mean()



             TTL=TimeList(TT)
             YEAR_REQUESTORS_w=TTL.getYearlist()

#             CO2mod_y  = np.zeros(len(YEAR_REQUESTORS),dtype=np.float32)
#             CO2cal_y  = np.zeros(len(YEAR_REQUESTORS),dtype=np.float32)
#             CO2cal_mean_y = np.zeros(len(YEAR_REQUESTORS),dtype=np.float32)

             for hh,yreq in enumerate(YEAR_REQUESTORS_w):
                        iy,wy=TTL.select(yreq)
#                        CO2mod_y[hh]=M_BIO[1,iy,iSub].mean()
#                        CO2cal_y[hh]=CO2cal[iy,iSub].mean()
                        CO2mod_y[iy[0]:iy[-1]+1]=M_BIO[1,iy,iSub].mean()
                        CO2cal_y[iy[0]:iy[-1]+1]=CO2cal[iy,iSub].mean()
			CO2cal_mean_y[iy[0]:iy[-1]+1]=CO2cal_mean[iy].mean()


   	     dt=mpldates.date2num(TT)
#	     dty=mpldates.date2num(
#   	     timelabel_list = list()
	     ax = axs[kk]

             ax.plot(dt,M_BIO[1,:,iSub],'b.-',label='BFM model')
             ax.plot(dt,CO2cal[:,iSub],'r.-',label='calculated')
             ax.plot(dt,CO2cal_mean[:],'g.-',label='calc.from daily')

	     ax.plot(dt,CO2mod_y,'b-')
             ax.plot(dt,CO2cal_y,'r-')
             ax.plot(dt,CO2cal_mean_y,'g-')
	     if (sub_names[iSub]== 'MED' ):
	     	print CO2mod_y 
	     	print CO2cal_y
	     	print CO2cal_mean_y
	     ax.xaxis_date()
	     ax.tick_params(axis='both', labelsize=8)
	     ax.set_title(str(OGS.P.basin_list[iSub]) + ' - ' + tf + 'ly',loc='center')
	     ax.set_ylabel('CO2airflux')
	     ax.set_label(tf)
	     ax.set_xlim(ax.set_xlim(dt[0],dt[-1]))
	     legend = ax.legend(loc='upper right', shadow=True, fontsize='xx-small')#,bbox_to_anchor=(1.05,0.000))
       fig.savefig(''.join(['CO2airflux_means_',sub_names[iSub],'.png']))

#       fig.show()


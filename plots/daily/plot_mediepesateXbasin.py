import numpy as np
from timeseries.plot import *
from basins import V2 as OGS
import itertools
import matplotlib.cm as cm
from commons.Timelist import TimeList

TL=np.load("../../TIMELIST_days.npy")
#WEEK_REQUESTORS=TL.getWeeklyList(5)
#for req in WEEK_REQUESTORS:
#    ii,w=TL.select(req)

#freq  = ['month','week','day']
freq  = ['day','week','month']
#ccols = ['green','cyan','blue']
ccols = ['blue','cyan','green']

sub_names = ['ALB','swMw','swMe','nwM','nTYR','sTYR','nADR','sADR','AEG','wION','eION','nION','wLEV','nLEV','sLEV','eLEV','MED']
axs = ['ax0','ax1','ax2','ax3','ax4','ax5']

#fig,axs=plt.subplots(nrows=5,ncols=1)
#colors = cm.rainbow(np.linspace(0, 1, len(OGS.Pred.basin_list)))
#col = itertools.cycle(colors)

#for iSub, sub in enumerate(OGS.Pred.basin_list[:1]):
for iSub, sub in enumerate(OGS.P.basin_list):
      fig,axs=plt.subplots(nrows=len(axs)) #,ncols=1)
      fig.set_size_inches(12,9)
      fig,axs=plt.subplots(nrows=len(axs)) #,ncols=1)
      for ivar, var in enumerate(['votemper','vosaline','sowindsp','pCO2','CO2airflux','kex']):

########################################################

        for kk, tf in enumerate(freq):
   	     if (tf == 'week'):
        		M_FOR=np.load('../../Mediepesate.npy')
        		M_BIO=np.load('../../MediepesateBIO.npy')
        		CO2cal=np.load('../../CO2airflux_week_offline.npy')
        		TT=np.load("../../TIMELIST_weeks.npy")
        		KEX=np.load("../../kex_x.npy")
   	     elif (tf == 'month'):
        		M_FOR=np.load('../../Mediepesate_monthly.npy')
        		M_BIO=np.load('../../MediepesateBIO_monthly.npy')
        		CO2cal=np.load('../../CO2airflux_month_offline.npy')
        		TT=np.load("../../TIMELIST_months.npy")
        		KEX=np.load("../../kex_x_month.npy")
             elif (tf == 'day'):
                        M_FOR=np.load('../../Mediepesate_daily.npy')
                        M_BIO=np.load('../../MediepesateBIO_daily.npy')
                        CO2cal=np.load('../../CO2airflux_day_offline.npy')
                        TT=np.load("../../TIMELIST_days.npy")
                        KEX=np.load("../../kex_x_day.npy")


   	     dt=mpldates.date2num(TT)
   	     timelabel_list = list()

########################################################
             for ivar, var in enumerate(['votemper','vosaline','sowindsp','pCO2','CO2airflux','kex']):	
		if (tf == 'day'): 
			if (ivar == 4):
				ax = axs[ivar]
				ax.plot(dt,CO2cal[:,iSub],'k')
				ivar = 5
		ax = axs[ivar]

#    for iFrame, filename in enumerate(TL.filelist):
	    	if (ivar <= 2):
			M = M_FOR
#			ax.plot(M[ivar,:,iSub],color=next(col),linewidth=1,label=OGS.Pred.basin_list[iSub])
#			ax.plot(M[ivar,:,iSub],linewidth=1,label=OGS.Pred.basin_list[iSub])
			ax.plot(dt,M[ivar,:,iSub],linewidth=1,label=OGS.P.basin_list[iSub],color=ccols[kk])
                elif (ivar == 5):
			ax.plot(dt,KEX[:,iSub],color=ccols[kk])
		else:
			M = M_BIO
			ivarbio = ivar - 3
#		        ax.plot(M[ivarbio,:,iSub],color=next(col),linewidth=1,label=OGS.Pred.basin_list[iSub])
			ax.plot(dt,M[ivarbio,:,iSub],linewidth=1,label=OGS.P.basin_list[iSub],color=ccols[kk])
		if (ivar == 4):
			ax.plot(dt,CO2cal[:,iSub],'r')
		if (ivar <1):
			ax.set_title(OGS.P.basin_list[iSub],loc='center')
#		ax.set_title(ivar,loc='center')
#		ax.ticklabel_format
		ax.tick_params(axis='both', labelsize=8)
	#	ax.set_xticklabels(fontsize='xxsmall')
		ax.xaxis_date()
		ax.set_ylabel(var)
		fig.savefig(''.join(['means_',sub_names[iSub],'.png']))
#		fig.show()

#		legend = ax.legend(loc='lower right', shadow=True, fontsize='xx-small',bbox_to_anchor=(1.05,0.000))
#ax.get_legend()
#fig.show()


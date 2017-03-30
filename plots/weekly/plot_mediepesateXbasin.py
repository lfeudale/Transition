import numpy as np
from timeseries.plot import *
from basins import V2 as OGS
import itertools
import matplotlib.cm as cm

M_FOR=np.load('../../Mediepesate.npy')
M_BIO=np.load('../../MediepesateBIO.npy')
CO2cal=np.load('../../CO2airflux_week_offline.npy')
TT=np.load("../../TIMELIST_weeks.npy")
KEX=np.load("../../kex_x.npy")
dt=mpldates.date2num(TT)
timelabel_list = list()

sub_names = ['ALB','swMw','swMe','nwM','nTYR','sTYR','nADR','sADR','AEG','wION','eION','nION','wLEV','nLEV','sLEV','eLEV']
axs = ['ax0','ax1','ax2','ax3','ax4','ax5']

#fig,axs=plt.subplots(nrows=5,ncols=1)
#colors = cm.rainbow(np.linspace(0, 1, len(OGS.Pred.basin_list)))
#col = itertools.cycle(colors)

#for iSub, sub in enumerate(OGS.Pred.basin_list[:2]):
for iSub, sub in enumerate(OGS.Pred.basin_list):
	fig,axs=plt.subplots(nrows=len(axs)) #,ncols=1)
	fig.set_size_inches(12,9)
	for ivar, var in enumerate(['votemper','vosaline','sowindsp','pCO2','CO2airflux','kex']):
		ax = axs[ivar]

#    for iFrame, filename in enumerate(TL.filelist):
	    	if (ivar <= 2):
			M = M_FOR
#			ax.plot(M[ivar,:,iSub],color=next(col),linewidth=1,label=OGS.Pred.basin_list[iSub])
#			ax.plot(M[ivar,:,iSub],linewidth=1,label=OGS.Pred.basin_list[iSub])
			ax.plot(dt,M[ivar,:,iSub],linewidth=1,label=OGS.Pred.basin_list[iSub])
                elif (ivar == 5):
			ax.plot(dt,KEX[:,iSub])
		else:
			M = M_BIO
			ivarbio = ivar - 3
#		        ax.plot(M[ivarbio,:,iSub],color=next(col),linewidth=1,label=OGS.Pred.basin_list[iSub])
			ax.plot(dt,M[ivarbio,:,iSub],linewidth=1,label=OGS.Pred.basin_list[iSub])
		if (ivar == 4):
			ax.plot(dt,CO2cal[:,iSub],'r')
		if (ivar <1):
			ax.set_title(OGS.Pred.basin_list[iSub],loc='center')
#		ax.set_title(ivar,loc='center')
#		ax.ticklabel_format
		ax.tick_params(axis='both', labelsize=8)
	#	ax.set_xticklabels(fontsize='xxsmall')
		ax.xaxis_date()
		ax.set_ylabel(var)
		fig.savefig(''.join(['means_',sub_names[iSub],'.png']))
		fig.show()

#		legend = ax.legend(loc='lower right', shadow=True, fontsize='xx-small',bbox_to_anchor=(1.05,0.000))
ax.get_legend()
fig.show()


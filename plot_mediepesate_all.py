import numpy as np
from timeseries.plot import *
from basins import V2 as OGS
import itertools
import matplotlib.cm as cm

M_FOR=np.load('Mediepesate.npy')
M_BIO=np.load('MediepesateBIO.npy')

axs = ['ax0','ax1','ax2','ax3','ax4']

fig,axs=plt.subplots(nrows=5,ncols=1)
#colors = itertools.cycle(["r", "b", "g"])
colors = cm.rainbow(np.linspace(0, 1, len(OGS.Pred.basin_list)))
col = itertools.cycle(colors)

for ivar, var in enumerate(['votemper','vosaline','sowindsp','pCO2','CO2airflux']):
#	if ivar == 0:
#                ax=ax0
#	elif ivar == 1:
#                ax=ax1
#	elif ivar == 2:
#                ax=ax2
	ax = axs[ivar]

#    for iFrame, filename in enumerate(TL.filelist):
	for iSub, sub in enumerate(OGS.Pred):
	    	if (ivar <= 2):
			M = M_FOR
			ax.plot(M[ivar,:,iSub],color=next(col),linewidth=1,label=OGS.Pred.basin_list[iSub])
		else:
			M = M_BIO
			ivarbio = ivar - 3
		        ax.plot(M[ivarbio,:,iSub],color=next(col),linewidth=1,label=OGS.Pred.basin_list[iSub])

legend = ax.legend(loc='lower right', shadow=True, fontsize='xx-small',bbox_to_anchor=(1.05,0.000))
ax.get_legend()
fig.show()


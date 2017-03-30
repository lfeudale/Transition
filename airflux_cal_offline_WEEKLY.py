import numpy as np
from timeseries.plot import *
from basins import V2 as OGS
from commons import Timelist
import sys

from math import exp, expm1

# IMPORT THE MATRICES:
M_FOR=np.load('Mediepesate.npy')
M_BIO=np.load('MediepesateBIO.npy')
TT=np.load("TIMELIST_weeks.npy")

# SAVE THE VARIABLES IN ARRAYS:
temp=M_FOR[0,:,:]
salt=M_FOR[1,:,:]
wind=M_FOR[2,:,:]
PCO2sea=M_BIO[0,:,:]
CO2airflux_model=M_BIO[1,:,:]


# CALCULATE THE SEA WATER DENSITY:

temp2 = temp * temp
temp3 = temp * temp * temp
temp4 = temp * temp * temp * temp
temp5 = temp * temp * temp * temp * temp

A= 8.24493*pow(10,-1) - 4.0899*pow(10,-3) * temp + 7.6438*pow(10,-5) * temp2 - 8.2467*pow(10,-7)*temp3 + 5.3875*pow(10,-9) * temp4

B= -5.72466*pow(10,-3) + 1.0227*pow(10,-4)*temp - 1.6546* pow(10,-6) * temp2;

C= 4.8314*pow(10,-4)

#Calculating the water density "rho_w"
rho_w = 999.842594 + 6.793952*pow(10,-2) *temp -9.095290*pow(10,-3) * temp2 + 1.001685*pow(10,-4) * temp3 - 1.120083*pow(10,-6) * temp4 + 6.536336*pow(10,-9) * temp5 


#Calculating the sea water density "rho_sw"
rho_sw = rho_w + A*salt + B *  pow(salt,1.5) + C * pow(salt,2) 
#Calculating the relative density rel_rho_sw
rel_rho_sw = rho_sw - rho_w

################################

C1=2073.1
C2=125.62
C3=3.6276
C4=0.043219
CO2SCHMIDT=660.
CM2M=0.01 # from cm to m
HOURS_PER_DAY=24
PCO2air=390 # uatm (o ppm)
ZERO_KELVIN=-273.15

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#   ! Calculate Schmidt number,
#   ! ratio between the kinematic viscosity and the molecular 
#   ! diffusivity of carbon dioxide.
#   !-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#    temp2 = temp*temp
for i in [0]:
    pschmidt = (C1 - C2*temp + C3*temp2 - C4*temp3)

#   !-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#   ! gas transfer velocity at a Schmidt number of 660
#   ! Temperature dependent
#   !-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    k660 = 2.5*(0.5246 + 1.6256*pow(10,-02) * temp + 4.9946*pow(10,-04)*temp2) 

#   !-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#   ! Calculate wind dependency
#   ! including conversion cm/hr => m/day :
#   !-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    kex = (k660 + 0.3*wind*wind)*np.sqrt(CO2SCHMIDT/pschmidt) * CM2M * HOURS_PER_DAY
#   !Alternative way 
#   !kex = (0.3_RLEN*wind*wind)*np.sqrt(CO2SCHMIDT/pschmidt)* &
#   !      CM2M*HOURS_PER_DAY
#
#   ! ---------------------------------------------------------------------
#   ! K0, solubility of co2 in the water (K Henry)
#   ! from Weiss 1974; K0 = [co2]/pco2 [mol kg-1 atm-1]
#   ! ---------------------------------------------------------------------
    tk = temp - ZERO_KELVIN
    tk100 = tk/100.0
    tk1002 = tk100*tk100
    k0 = np.exp(93.4517/tk100 - 60.2409 * np.ones(temp.shape) + 23.3585 * np.log(tk100) + salt * (0.023517 - 0.023656 * tk100 + 0.0047036 * tk1002))
#
#   !-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#   ! flux co2 in mmol/m2/day   
#   !-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#   ! (m * d-1) * uatm * (mol * kg-1 * atm-1) * (kg * m-3)
#   !     d-1   1.e-6      mol   m-2
#   !     umol m-2 d-1 / 1000 = mmol/m2/d

    CO2airflux = kex * (PCO2air - PCO2sea) * k0 * rho_sw / 1000.0
    kex_k0_rho_sw = kex * k0 * rho_sw

np.save('CO2airflux_week_offline',CO2airflux)
np.save('CO2airflux_week_model_output',CO2airflux_model)
np.save('kex_x',kex_k0_rho_sw)
sys.exit()
############################
# PLOT:
axs = ['ax0','ax1']
fig,axs=plt.subplots(nrows=2,ncols=1)
colors = cm.rainbow(np.linspace(0, 1, len(OGS.P.basin_list)))
col = itertools.cycle(colors)


############################
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter

tab_nrow = len(CO2airflux[:,0])
tab_ncol = len(CO2airflux[0,:])
tab_coln=tab_ncol+4+1
table_values = np.zeros((tab_nrow,tab_coln),np.float)
np.savetxt("tabella_" + "CO2airflux"  + ".csv",CO2airflux,fmt='%10.5f',delimiter=',',header=np.str(OGS.P.basin_list))
np.savetxt("tabella_" + "CO2airflux_model" + ".csv",CO2airflux_model,fmt='%10.5f',delimiter=',',header=np.str(OGS.P.basin_list))
#np.savetxt("tabella_" + varname  + "_@" + str(int(depth))  + "m.csv",table_values,fmt='%10.5f',delimiter=',')

A=np.zeros((CO2airflux.shape[0],1+CO2airflux.shape[1]))
B=np.zeros((CO2airflux.shape[0],1+CO2airflux.shape[1])).astype(object)
DD = np.array(len(TT))
DD = []

for jj,tday in enumerate(TT):
    tday 
    print tday.date()
    DD.append(str(tday.date()))
#DD[jj] =  str(tday.date())

DA=np.asarray(DD)
B[:,0]=DA
B[:,1:157]=CO2airflux
     
np.savetxt("tabella_" + "CO2airflux_2" + ".csv",CO2airflux,fmt='%10.5f',delimiter=',',header='date  ' + np.str(OGS.P.basin_list))

np.savetxt("tabella_" + "CO2airflux_2" + ".csv",B,fmt='%s + %10.5f',delimiter=',')

MM = np.column_stack((DA,CO2airflux))
MM2 =  np.column_stack((DA,CO2airflux_model))
np.savetxt("tabella_" + "CO2airflux_2" + ".csv",MM,fmt='%s',delimiter=',')

np.savetxt("tabella_" + "CO2airflux_2" + ".csv",MM,fmt='%s',delimiter='  ,  ',header='date  ' + np.str(OGS.P.basin_list))
np.savetxt("tabella_" + "CO2airflux_model_2" + ".csv",MM2,fmt='%s',delimiter='  ,  ',header='date  ' + np.str(OGS.P.basin_list))

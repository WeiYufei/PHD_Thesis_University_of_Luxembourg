# coding=utf-8
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt    
from scipy import stats
import pandas as pd
import uncertainties.unumpy as unp
import uncertainties as unc
import math
import scipy
from matplotlib.lines import Line2D
import matplotlib
from matplotlib.ticker import FuncFormatter
from numpy import *
import matplotlib.patches as mpatches
import requests
import matplotlib as mpl
import gc      
from pandas import Series,DataFrame
import statsmodels.api as sm
from sympy import pretty_print as su
import tkinter
from matplotlib.pyplot import colorbar
matplotlib.use('TkAgg')
import collections
import dbf
from dbfread import DBF
import os
import matplotlib.patches as patches
from matplotlib.pyplot import MultipleLocator
matplotlib.use('wxAgg')

filePath='M:\\ArcGISDbf378_toCalculateMinFUA\\'
dirs=os.listdir(filePath)

eachFUASlope=[]
eachLogFUAPop=[]
eachName=[]

fig = plt.figure(figsize=(4, 3),dpi=250)
ax1=plt.subplot()
for ipath in dirs:
    if os.path.splitext(ipath)[1]=='.dbf':
        currentDir='M:/ArcGISDbf378_toCalculateMinFUA/'+str(ipath)#traverse all the 378 dbf,, each dbf contains data of a city
        mergedCellTable=dbf.Table(currentDir,codepage=0xf0) 
        mergedCellTable.open(dbf.READ_ONLY)
        df1 = pd.DataFrame(mergedCellTable)
        df1.columns =['OBJECTID', 'FID_extrac', 'pointid', 'grid_code', 'FID_FUA_ex', 'eFUA_ID', 'UC_num', 'UC_IDs', 'eFUA_name', 'Commuting', 'Cntry_ISO', 'Cntry_name', 'FUA_area', 'UC_area', 'FUA_p_2015', 'UC_p_2015', 'Com_p_2015', 'eFUAnameEN', 'eFUAnamENS', 'Count_', 'y', 'CBDX', 'CBDY', 'x', 'eFUA_IDS', 'centrodX', 'centrodY', 'CBDPoiRs1k', 'BUFF_DIST', 'ORIG_FID', 'Shape_Leng', 'Shape_Area', 'DisLevel', 'NO2Lev', 'Log10Pop15']
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Helvetica']
        
        CBDX=df1['CBDX'][0]
        CBDY=df1['CBDY'][0]
     
        xcoorTemp=df1['centrodX']
        ycoorTemp=df1['centrodY']
        NO2AveSatelliteTemp=np.array(df1['grid_code'])
        minFUA=min(NO2AveSatelliteTemp)
        xcoorTemp=xcoorTemp.tolist()
        ycoorTemp=ycoorTemp.tolist()
        
        zeroIndexTemp=[]
        for iZeroTemp in range(len(NO2AveSatelliteTemp)):
            if NO2AveSatelliteTemp[iZeroTemp]==minFUA:
                NO2AveSatelliteTemp[iZeroTemp]=-999999999
                zeroIndexTemp.append(iZeroTemp)
                        
        for jjjIndexTempX in range(len(zeroIndexTemp)):
                xcoorTemp[zeroIndexTemp[jjjIndexTempX]]=-999999999

        for jjjIndexTempY in range(len(zeroIndexTemp)):
                ycoorTemp[zeroIndexTemp[jjjIndexTempY]]=-999999999
        
        NO2AveSatelliteTemp=NO2AveSatelliteTemp.tolist()
        for iRemoveT1 in range(len(zeroIndexTemp)):
            NO2AveSatelliteTemp.remove(-999999999)

        for iRemoveT2 in range(len(zeroIndexTemp)):
            xcoorTemp.remove(-999999999)
        
        for iRemoveT3 in range(len(zeroIndexTemp)):
            ycoorTemp.remove(-999999999)
            
            
        FuaNameTempN=df1['eFUAnamENS'][0]
        FuaNameTemp=FuaNameTempN.strip(' ')
        FuaNameTempShortN=df1['eFUA_name'][0]
        FuaNameTempShort=FuaNameTempShortN.strip(' ')
        
        FUAIdTemp=int(df1['eFUA_ID'][0])
        Pop2015Temp=round(df1['FUA_p_2015'][0],2)
        Pop2015TempForCalculate=np.array(df1['FUA_p_2015'][0])

        xcoorTempNP=np.array(xcoorTemp)
        ycoorTempNP=np.array(ycoorTemp)
        # THIS IS THE DISTANCE FROM THE PIXELS TO THE CITY CENTER
        newDist=np.sqrt((xcoorTempNP-CBDX)**2+(ycoorTempNP-CBDY)**2)
        # remove the point having a distance of 0 to avoid log(0)
        zeroIndex=[]
        for iZero in range(len(newDist)):
            if newDist[iZero]==0:
                newDist[iZero]=-999999999
                zeroIndex.append(iZero)
                        
        for jjjIndex in range(len(zeroIndex)):
                NO2AveSatelliteTemp[zeroIndex[jjjIndex]]=-999999999
        
        newDist=newDist.tolist()
        for iRemove in range(len(zeroIndex)):
            NO2AveSatelliteTemp.remove(-999999999)

        for iRemove2 in range(len(zeroIndex)):
            newDist.remove(-999999999)
        NO2AveSatelliteTemp=np.array(NO2AveSatelliteTemp)
        newDist=np.array(newDist)

        logNewDist=np.log10(newDist)
        logNO2AveSatelliteTemp=np.log10(NO2AveSatelliteTemp-minFUA)
        logPop2015TempForCalculate=np.log10(Pop2015TempForCalculate)
        
        # linear regression
        slope,intercept,rvalue,pvalue,stderr=stats.linregress(logNewDist, logNO2AveSatelliteTemp)
        
        eachFUASlope.append(slope)
        eachLogFUAPop.append(logPop2015TempForCalculate)
        eachName.append(FuaNameTempShort)
        
        def myfunc(x):
            return slope*x+intercept
        getmodel=list(map(myfunc,logNewDist))
            
plt.scatter(eachLogFUAPop, eachFUASlope, marker='o',c='black',s=3)
# linear regression
slope1,intercept1,rvalue1,pvalue1,stderr1=stats.linregress(eachLogFUAPop, eachFUASlope)
slopePrintV=round(slope1,2)
InterceptPrintV=round(intercept1,2)
eestring='K = '+str(slopePrintV)+'lgP'+' + '+str(InterceptPrintV)+", R\u00b2 = "+str(round(rvalue1*rvalue1,2))

YY= eachFUASlope
XX=eachLogFUAPop
XX = sm.add_constant(XX)
model = sm.OLS(YY, XX).fit()

#view model summary
#print(model.summary())
print("Slope is "+str(model.params[1]))
print("Std err of slope is "+str(model.bse[1]))
print("P value of slope is "+str(model.pvalues[1]))

print("Intercept is "+str(model.params[0]))
print("Std err of intercept is "+str(model.bse[0]))
print("P value of intercept is "+str(model.pvalues[0]))

print("R2 is "+str(model.rsquared))

def myfunc1(x1):
    return slope1*x1+intercept1
getmodel=list(map(myfunc1,eachLogFUAPop))

for iia in range(len(eachName)):
    ax1.text(eachLogFUAPop[iia], eachFUASlope[iia], str(eachName[iia]), color='black',fontsize=5)

plt.xticks(fontproperties='Helvetica',size=7)
plt.yticks(fontproperties='Helvetica',size=7)
        
legend_elements = [Line2D([0], [0], marker='o',color='b',label=eestring,markersize=0,linewidth=1)]
ax1.legend(handles=legend_elements, loc='best',prop={'family':'Helvetica','size':5},frameon=False)
plt.title('Real CBD')
ax1.set_xlabel('lgP',fontsize=7)
ax1.set_ylabel('B',fontsize=7)
plt.plot(eachLogFUAPop,getmodel,'b')
#plt.show()

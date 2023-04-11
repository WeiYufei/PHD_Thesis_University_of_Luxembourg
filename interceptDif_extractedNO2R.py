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

eachFUAInterceptHNO2=[]
eachLogFUAPop=[]
eachName=[]
eachFUAInterceptCBD=[]

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

        xcoorTemp=df1['centrodX']
        ycoorTemp=df1['centrodY']
        xcoorTemp1=df1['centrodX']
        ycoorTemp1=df1['centrodY']
        CBDX=df1['CBDX'][0]
        CBDY=df1['CBDY'][0]
        NO2AveSatelliteTemp=np.array(df1['grid_code'])
        minFUA=min(NO2AveSatelliteTemp)
        NO2AveSatelliteTemp1=NO2AveSatelliteTemp
        xcoorTemp=xcoorTemp.tolist()
        ycoorTemp=ycoorTemp.tolist()
        zeroIndexTemp=[]
        # remove min NO2 pixels
        for iZeroTemp in range(len(NO2AveSatelliteTemp)):
            if NO2AveSatelliteTemp[iZeroTemp]==minFUA:
                NO2AveSatelliteTemp[iZeroTemp]=-999999999
                zeroIndexTemp.append(iZeroTemp)
                        
        for jjjIndexTempX in range(len(zeroIndexTemp)):
                xcoorTemp[zeroIndexTemp[jjjIndexTempX]]=-999999999

        for jjjIndexTempY in range(len(zeroIndexTemp)):
                ycoorTemp[zeroIndexTemp[jjjIndexTempY]]=-999999999
                
        for jjjIndexTempVa in range(len(zeroIndexTemp)):
                NO2AveSatelliteTemp1[zeroIndexTemp[jjjIndexTempVa]]=-999999999
                
        NO2AveSatelliteTemp=NO2AveSatelliteTemp.tolist()
        NO2AveSatelliteTemp1=NO2AveSatelliteTemp1.tolist()
        for iRemoveT1 in range(len(zeroIndexTemp)):
            NO2AveSatelliteTemp.remove(-999999999)

        for iRemoveT2 in range(len(zeroIndexTemp)):
            xcoorTemp.remove(-999999999)
        
        for iRemoveT3 in range(len(zeroIndexTemp)):
            ycoorTemp.remove(-999999999)   
            
        for iRemoveT4 in range(len(zeroIndexTemp)):
            NO2AveSatelliteTemp1.remove(-999999999)    
                                                  
        FuaNameTempN=df1['eFUAnamENS'][0]
        FuaNameTemp=FuaNameTempN.strip(' ')
        FuaNameTempShortN=df1['eFUA_name'][0]
        FuaNameTempShort=FuaNameTempShortN.strip(' ')
        
        FUAIdTemp=int(df1['eFUA_ID'][0])
        Pop2015Temp=round(df1['FUA_p_2015'][0],2)
        Pop2015TempForCalculate=np.array(df1['FUA_p_2015'][0])


        listNO2Temp=NO2AveSatelliteTemp
        liNO2MAX=max(listNO2Temp)
        indSingleTemp=listNO2Temp.index(liNO2MAX)
        indReal=[]
        for indFRe in range(len(listNO2Temp)):
            if listNO2Temp[indFRe]==liNO2MAX:
                indReal.append(indFRe)
        xcoorForHP=[]
        ycoorForHP=[]
        for fcbd in range(len(indReal)):
            aat1=indReal[fcbd]
            xx=xcoorTemp[aat1]
            yy=ycoorTemp[aat1]
            xcoorForHP.append(xx)
            ycoorForHP.append(yy)
        # values and coordinates of the highest point
        HPNO2X=np.mean(xcoorForHP)
        HPNO2Y=np.mean(ycoorForHP)

        xcoorTempNP=np.array(xcoorTemp)
        ycoorTempNP=np.array(ycoorTemp)
        # THIS IS THE DISTANCE FROM THE PIXELS TO THE PIXEL WHERE THE NO2 IS THE HIGHEST
        newDist=np.sqrt((xcoorTempNP-HPNO2X)**2+(ycoorTempNP-HPNO2Y)**2)
        # THIS IS THE DISTANCE FROM THE PIXELS TO THE PIXEL OF THE CITY CENTER
        newDist1=np.sqrt((xcoorTempNP-CBDX)**2+(ycoorTempNP-CBDY)**2)

        # remove the point having a distance of 0 to avoid log(0)
        zeroIndex=[]
        for iZero in range(len(newDist)):
            if newDist[iZero]==0:
                newDist[iZero]=-999999999
                zeroIndex.append(iZero)
        # remove the according NO2 pixles              
        for jjjIndex in range(len(zeroIndex)):
                NO2AveSatelliteTemp[zeroIndex[jjjIndex]]=-999999999
        newDist=newDist.tolist()
        for iRemove in range(len(zeroIndex)):
            NO2AveSatelliteTemp.remove(-999999999)

        for iRemove2 in range(len(zeroIndex)):
            newDist.remove(-999999999)
        NO2AveSatelliteTemp=np.array(NO2AveSatelliteTemp)
        newDist=np.array(newDist)
        
        # remove the point having a distance of 0 to avoid log(0)
        zeroIndex1=[]
        for iZero1 in range(len(newDist1)):
            if newDist1[iZero1]==0:
                newDist1[iZero1]=-999999999
                zeroIndex1.append(iZero1)
        
        for jjjIndex1 in range(len(zeroIndex1)):
                NO2AveSatelliteTemp1[zeroIndex1[jjjIndex1]]=-999999999
        # remove the according NO2 pixles              
        newDist1=newDist1.tolist()
        for iRemove1 in range(len(zeroIndex1)):
            NO2AveSatelliteTemp1.remove(-999999999)

        for iRemove21 in range(len(zeroIndex1)):
            newDist1.remove(-999999999)
            
        NO2AveSatelliteTemp1=np.array(NO2AveSatelliteTemp1)
        newDist1=np.array(newDist1)
        
        logNewDist=newDist
        logNO2AveSatelliteTemp=np.log10(NO2AveSatelliteTemp-minFUA)
        logPop2015TempForCalculate=np.log10(Pop2015TempForCalculate)
        logNewDist1=np.log10(newDist1)
        logNO2AveSatelliteTemp1=np.log10(NO2AveSatelliteTemp1-minFUA)
        # linear regression
        slope,intercept,rvalue,pvalue,stderr=stats.linregress(logNewDist, logNO2AveSatelliteTemp)
        slopeCBD,interceptCBD,rvalueCBD,pvalueCBD,stderr=stats.linregress(logNewDist1, logNO2AveSatelliteTemp1)
        
        # collect intercept
        eachFUAInterceptHNO2.append(intercept)
        eachLogFUAPop.append(logPop2015TempForCalculate)
        eachName.append(FuaNameTempShort)
        eachFUAInterceptCBD.append(interceptCBD)
        Y=np.array(eachFUAInterceptHNO2)-np.array(eachFUAInterceptCBD)

        def myfunc(x):
            return slope*x+intercept
        getmodel=list(map(myfunc,logNewDist))
            
plt.scatter(eachLogFUAPop,Y, marker='o',c='black',s=2.5)

for iia in range(len(eachName)):
    ax1.text(eachLogFUAPop[iia], Y[iia], str(eachName[iia]), color='black',fontsize=5)

plt.xticks(fontproperties='Helvetica',size=7)
plt.yticks(fontproperties='Helvetica',size=7)
        
eestring='Difference of intercept (A) (HighestNO$_2$-Real CBD, NO$_2$ without background)'
ax1.set_xlabel('log$_{10}$P',fontsize=5)
ax1.set_ylabel(eestring,fontsize=5)
plt.show()

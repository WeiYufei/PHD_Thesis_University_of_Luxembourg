#coding=utf-8
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt    
import pandas as pd
import math
import scipy
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
from dbfread import DBF
from pylab import *
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
import matplotlib.patches as mpatches
import os

matplotlib.use('wxAgg')

mergedCellTableLong=r'M:\Eclipse_Workspace\Article2_Kriging_Py\MeCel1000GauKri.dbf'
mergedCellLong=DBF(mergedCellTableLong, encoding='cp852')#solve unicode problem
dftableCell1Long=pd.DataFrame(iter(mergedCellLong))
Pop2015Long=set(dftableCell1Long.iloc[0:862225,14].tolist())#to find the max and min limits of population for plotting
Pop2015Long2=np.round(dftableCell1Long.iloc[0:862225,14].tolist(),decimals=6)#to calculate the reference population and control precision
maxPop2015=max(pd.Series(Pop2015Long2).unique())#find non-replicated population values

DistinM2=dftableCell1Long.iloc[0:862225,27].tolist()
maxDistinM2=max(pd.Series(DistinM2).unique())
maxDist=np.round((maxDistinM2/1000).tolist(),decimals=6)#find the reference distance and control precision

logPop2015Long=[]
for jop in Pop2015Long:
    logPop2015Long.append(math.log(jop,10))
     
longPop2015Upper=max(logPop2015Long)
longPop2015Lower=min(logPop2015Long)
 
longPop2015UpperColorBar=longPop2015Upper#to plot the population legend
longPop2015LowerColorBar=longPop2015Lower#to plot the population legend

#print(longPop2015Upper)7.173815247864745
#print(longPop2015UpperColorBar)8
#print(longPop2015Lower)4.827116811518219
#print(longPop2015LowerColorBar)4
ScaleDistValue=0.45#what we get in calculating rmsc
ScaleNO2Value=0.95#what we get in calculating rmsc
binDist=1 #drawing and calculating precision
#DistRange=93 #what we get in calculating rmsc
TotalRescaledDist=[]#for collecting all the rescaled distance
TotalRescaledNO2=[]#for collecting all the rescaled no2
fig = plt.figure(figsize=(4, 3),dpi=250)
grid = plt.GridSpec(1, 20)
ax1=plt.subplot(grid[0,0:19])
filePath='M:\\ProcessedMeCel1000TablewMinFUA\\'
dirs=os.listdir(filePath)
for ipath in dirs:
    if os.path.splitext(ipath)[1]=='.csv':
        currentDir='M:/ProcessedMeCel1000TablewMinFUA/'+str(ipath)#traverse all csv files of all the cities
        mergedCell = pd.read_csv(currentDir,encoding = 'unicode_escape',low_memory = False)
        dftableCell1=pd.DataFrame(mergedCell)
        dftableCell=dftableCell1.sort_values(by=['FUA_p_2015'],ascending=False)
        Pop2015=np.round(dftableCell['FUA_p_2015'].tolist(),decimals=6)
        FUAId=dftableCell['eFUA_ID'].tolist()
        FUAName=dftableCell['eFUAnamENS'].tolist()
        NO2AveSatelliteExtracted=np.round(dftableCell['extrGrid'].tolist(),decimals=6)
        DistinM=np.round(dftableCell['CBDPoiRs1k'].tolist(),decimals=6)

        logPop2015=np.round(dftableCell['Log10Pop15'].tolist(),decimals=6)
          
        Dist=np.round((np.array(DistinM)/1000).tolist(),decimals=6)
           
        indexHead=[]#find the head index of a city
        indexEnd=[]#find the tail index of a city
        for i in range(len(FUAName)-1):
            if FUAName[i]!=FUAName[i+1]:
                indexEnd.append(i)
                indexHead.append(i+1)
        indexHead.insert(0, 0)
        indexEnd.append(len(FUAId))
                 
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Helvetica']
        plt.rcParams['axes.titlesize'] = 6
        plt.rcParams['axes.labelsize'] = 6
        plt.rcParams['xtick.labelsize'] = 6
        plt.rcParams['ytick.labelsize'] = 6
           
        normalizeLogPopRank=[]#normalize to [0,1], then calculate rank,then -1 for getting python rank, for finding the right color
        for iiiq in range(len(FUAId)):
            aio=round((logPop2015[iiiq]-longPop2015LowerColorBar)/(longPop2015UpperColorBar-longPop2015LowerColorBar)*100)-1
            normalizeLogPopRank.append(aio)
             
        clist=['yellow','darkorange','red','crimson','darkmagenta','indigo','darkslateblue']
        newcmp = LinearSegmentedColormap.from_list('mycolor',clist, N=100)
        norm = mpl.colors.Normalize(vmin=longPop2015LowerColorBar, vmax=longPop2015UpperColorBar)
        yColor=newcmp(range(100))#create color map for the legend
        #print(len(yColor))
           
        ScalDist=(np.array(Dist)/((np.array(Pop2015)/maxPop2015)**ScaleDistValue)).tolist()#scaled distance
        ScalNO2=(np.array(NO2AveSatelliteExtracted)/((np.array(Pop2015)/maxPop2015)**ScaleNO2Value)).tolist()#scaled no2

        
        DistRange=maxDist/0.45+20#+20 is because to avoid a clear cutoff just at the end of the distance
           
        for ilz in range(len(indexHead)):
            thisBegin=indexHead[ilz]
            thisEnd=indexEnd[ilz]
            thisColorRank=normalizeLogPopRank[thisBegin:thisEnd+1][0]
            #print(thisBegin)
            #print(thisEnd)
            
            thisColorConfig=yColor[thisColorRank].tolist()
            FuaNameFullTemp=FUAName[thisBegin:thisEnd+1][0]
            Pop2015Temp=Pop2015[thisBegin:thisEnd+1][0]
            FUAIdTempT=str(FUAId[thisBegin:thisEnd+1][0])
            FUAIdTemp=FUAIdTempT[:-2]
            DistTempTemp=ScalDist[thisBegin:thisEnd+1]
            DistTemp=[]
            for iresc in range(len(DistTempTemp)):
                DistTemp.append(DistTempTemp[iresc])
            
            NO2AveSatelliteTemp=ScalNO2[thisBegin:thisEnd+1]
                      
            intvalBox=list(np.arange(min(DistTemp), max(DistTemp)+binDist,binDist))
            #print(intvalBox)
            intvalBox.append(max(DistTemp))
                  
            judHead=[]# split data according to the indices
            judTail=[]
            judgeMid=[]
            for jud in range(len(intvalBox)-1):
                judHead.append(intvalBox[jud])
                judTail.append(intvalBox[jud+1])
                judgeMid.append((intvalBox[jud]+intvalBox[jud+1])/2)
                      
            forPlotNO2=[]
            for ijniF in range(len(judHead)):
                tempJudHead=judHead[ijniF]
                tempJudTail=judTail[ijniF]    
                forPlotNO2YTemp=[]    
                for iii in range(len(DistTemp)):
                    if DistTemp[iii]>=tempJudHead and DistTemp[iii]<tempJudTail:
                            forPlotNO2YTemp.append(NO2AveSatelliteTemp[iii])
                forPlotNO2YMean=np.mean(forPlotNO2YTemp)
                forPlotNO2.append(forPlotNO2YMean)
                   
            distLessThr=[] 
            NO2LessThr=[]
            for imas in range(len(judgeMid)):
                if judgeMid[imas] <DistRange:
                    distLessThr.append(judgeMid[imas])
                    NO2LessThr.append(forPlotNO2[imas])
                        
            ax1.plot(distLessThr,NO2LessThr,linestyle='solid', c=thisColorConfig, linewidth=0.5)  
            for er1 in range(len(distLessThr)):
                TotalRescaledDist.append(distLessThr[er1])
                   
            for er2 in range(len(NO2LessThr)):
                TotalRescaledNO2.append(NO2LessThr[er2])
           
        #===============================================================================
        # print(min(TotalRescaledDist))
        # print(max(TotalRescaledDist))
        #===============================================================================
           
        TotalRescaledDistTag=[]
        for iu in range(len(TotalRescaledDist)):
            TotalRescaledDistTag.append(ceil(TotalRescaledDist[iu]))
          
           
tempDict={'distanceLevelTag':TotalRescaledDistTag,'distanceLevel':TotalRescaledDist, 'NO2RescaledT':TotalRescaledNO2}
tempFrame=pd.DataFrame(tempDict)
#print(tempFrame)
tempFrameN = tempFrame[tempFrame['NO2RescaledT'].notna()]
#print(tempFrameN)
   
bq1=tempFrameN.groupby('distanceLevelTag').agg({'distanceLevel':['mean'],'NO2RescaledT':['mean','median','std']})#to draw the mean of mean and plus/minus 1 std
bq1.columns = ['ring','NO2mean','NO2median','NO2std']
bq1['mean_sd_up']=bq1['NO2mean']+bq1['NO2std']
bq1['mean_sd_down']=bq1['NO2mean']-bq1['NO2std']
bq1['mean2D']=bq1['NO2mean']*2*math.pi*bq1['ring']
bq1['sd2D']=bq1['NO2std']*2*math.pi*bq1['ring']
bq1 = bq1.dropna()
   
  
plotdist=bq1['ring'].tolist()
plotmeanno2=bq1['NO2mean'].tolist()
sdvalues=bq1['NO2std'].tolist()
plotupline=bq1['mean_sd_up'].tolist()
plotdownline=bq1['mean_sd_down'].tolist()
mean2DValues=bq1['mean2D'].tolist()
sd2DValues=bq1['NO2std'].tolist()
    
    
plt.fill_between(plotdist,plotupline,plotdownline,color="silver",alpha=0.4)
ax1.plot(plotdist,plotmeanno2,linestyle='solid', c='black', linewidth=1.5)  

signalnoise=sum(plotmeanno2)/sum(sdvalues)
#print(signalnoise)
signalnoise2D=sum(mean2DValues)/sum(sd2DValues)
#print(signalnoise2D)
#===============================================================================
# profile$signalnoise<-profile$mean/profile$sd
# signalnoise2D<-sum(profileOK$mean2D)/sum(profileOK$sd2D)
# signalNoise=sum()
#===============================================================================
             
def formatnumY(y, pos): #Scientific notation
    return '%.0f' % (y/1)
formatter2 = FuncFormatter(formatnumY)#Scientific notation
ax1.yaxis.set_major_formatter(formatter2) 
             
ax1.set_xlabel('R'+"'"+' in km (rescaled by '+str(ScaleDistValue)+')',fontsize=6.5)
ax1.set_ylabel('C(R'+"'"+') in mol/m$^2$ (rescaled by ' +str(ScaleNO2Value)+')',fontsize=6.5) 
plt.xticks(fontproperties='Helvetica',size=6)
plt.yticks(fontproperties='Helvetica',size=6)
#titleString="Mean of X of 378 FUA at rescaled distance (binned in "+str(binDist)+" km)"
#ax1.set_title(titleString,fontsize=6.5)
ax1.xaxis.set_tick_params(width=0.5)
ax1.yaxis.set_tick_params(width=0.5)
  
gray_patch = mpatches.Patch(color='silver', alpha=0.4,label='$\pm$ 1 SD')
legend_elements = [Line2D([0], [0], marker='o',linestyle='solid', label='Mean of rescaled C',color='black',markersize=0,linewidth=1.5),
                   gray_patch]
    
ax1.legend(handles=legend_elements, loc='best', fontsize=6,frameon=False)
ax1.set_xlim(xmin=0,xmax=240)         
ax1.set_ylim(ymin=0, ymax=5000)         
    
ax2 = plt.subplot(grid[0,19])#to draw the color legend
       
cmap1 = LinearSegmentedColormap.from_list('', ['yellow','darkorange','red','crimson','darkmagenta','indigo','darkslateblue'],N=100)
norm = mpl.colors.Normalize(vmin=longPop2015LowerColorBar, vmax=longPop2015UpperColorBar)
          
cbar=plt.colorbar(ScalarMappable(cmap=cmap1,norm=norm), cax=fig.add_axes([0.87, 0.5, 0.01, 0.38]),ticks=[5, 6, 7])
cbar.set_label(label='P', size=6.5, weight='normal')
cbar.ax.tick_params(labelsize=6.5)
cbar.ax.set_yticklabels(['1E5', '1E6', '1E7']) 
       
x_axis = ax2.get_xaxis()
x_axis.set_visible(False)
       
y_axis = ax2.get_yaxis()
y_axis.set_visible(False)
ax2.spines['right'].set_color('none')
ax2.spines['left'].set_color('none')
ax2.spines['top'].set_color('none')
ax2.spines['bottom'].set_color('none')
plt.xticks(fontproperties='Helvetica',size=6)
plt.yticks(fontproperties='Helvetica',size=6)
   
plt.show()

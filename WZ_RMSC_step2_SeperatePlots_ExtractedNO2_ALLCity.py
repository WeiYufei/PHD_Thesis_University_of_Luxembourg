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
mergedCellLong=DBF(mergedCellTableLong, encoding='cp852')
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

clist=['yellow','darkorange','red','crimson','darkmagenta','indigo','darkslateblue']#define the population legend - color bar
newcmp = LinearSegmentedColormap.from_list('mycolor',clist, N=100)
norm = mpl.colors.Normalize(vmin=longPop2015LowerColorBar, vmax=longPop2015UpperColorBar)

#print(longPop2015Upper)7.173815247864745
#print(longPop2015UpperColorBar)8
#print(longPop2015Lower)4.827116811518219
#print(longPop2015LowerColorBar)4
ScaleDistValue=0.45
ScaleNO2Value=0.95
binDist=1
#DistRange=93

filePath='M:\\ProcessedMeCel1000TablewMinFUA\\'
dirs=os.listdir(filePath)
for ipath in dirs:
    if os.path.splitext(ipath)[1]=='.csv':#traverse all csv files of all the cities
        currentDir='M:/ProcessedMeCel1000TablewMinFUA/'+str(ipath)
        mergedCell = pd.read_csv(currentDir,encoding = 'unicode_escape',low_memory = False)
        dftableCell1=pd.DataFrame(mergedCell)
        dftableCell=dftableCell1.sort_values(by=['FUA_p_2015'],ascending=False)
        Pop2015=np.round(dftableCell['FUA_p_2015'].tolist(),decimals=6)
        FUAId=dftableCell['eFUA_ID'].tolist()
        FUAName=dftableCell['eFUAnamENS'].tolist()
        NO2AveSatelliteExtracted=np.round(dftableCell['extrGrid'].tolist(),decimals=6)
        DistinM=np.round(dftableCell['CBDPoiRs1k'].tolist(),decimals=6)

        PopRank=dftableCell.iloc[0:104272,35].tolist()
        logPop2015=np.round(dftableCell['Log10Pop15'].tolist(),decimals=6)
          
        Dist=np.round((np.array(DistinM)/1000).tolist(),decimals=6)
           
        indexHead=[]
        indexEnd=[]
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
           
        normalizeLogPopRank=[]#normalize to [0,1], then calculate rank,then -1 for getting python rank
        for iiiq in range(len(FUAId)):
            aio=round((logPop2015[iiiq]-longPop2015LowerColorBar)/(longPop2015UpperColorBar-longPop2015LowerColorBar)*100)-1
            normalizeLogPopRank.append(aio)
           
        yColor=newcmp(range(100))
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
            
            fig = plt.figure(figsize=(4, 3),dpi=250)
            grid = plt.GridSpec(1, 20)
            ax1=plt.subplot(grid[0,0:19])
            ax1.plot(distLessThr,NO2LessThr,linestyle='solid', c=thisColorConfig, linewidth=0.5)  
            
        
            #signalnoise=sum(plotmeanno2)/sum(sdvalues)
            #print(signalnoise)
            #signalnoise2D=sum(mean2DValues)/sum(sd2DValues)
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
                         
            plt.ylim((0,max(NO2LessThr)+20))
            ax1.set_xlabel('Euclidean distance to main center in km, rescaled by '+str(ScaleDistValue),fontsize=6.5)
            ax1.set_ylabel('Average NO$_2$ in mol/m$^2$, rescaled by ' +str(ScaleNO2Value),fontsize=6.5) 
            plt.xticks(fontproperties='Helvetica',size=6)
            plt.yticks(fontproperties='Helvetica',size=6)

            tempNameFULL=FuaNameFullTemp.strip()
            titleString="Mean of annual mean tropospheric NO$_2$ columns of \n"+tempNameFULL+", ID:"+FUAIdTemp+", Population: "+str(Pop2015Temp)+"\n at rescaled distance (binned in "+str(binDist)+" km)"
            ax1.set_title(titleString,fontsize=6.5)
            ax1.xaxis.set_tick_params(width=0.5)
            ax1.yaxis.set_tick_params(width=0.5)
                          
            ax2 = plt.subplot(grid[0,19])#to draw the color legend
                    
            cmap1 = LinearSegmentedColormap.from_list('', ['yellow','darkorange','red','crimson','darkmagenta','indigo','darkslateblue'],N=100)
            norm = mpl.colors.Normalize(vmin=longPop2015LowerColorBar, vmax=longPop2015UpperColorBar)
                       
            cbar=plt.colorbar(ScalarMappable(cmap=cmap1,norm=norm), cax=fig.add_axes([0.87, 0.5, 0.01, 0.38]),ticks=[5, 6, 7])
            cbar.set_label(label='FUA Population', size=6.5, weight='normal')
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
            
            #plt.show()
            
            for iii in range(len(tempNameFULL)):#the names of some cities contain "/", so replace this with "or"
                if tempNameFULL[iii]=='/':
                    tempNameO=tempNameFULL[0:iii]+'or'+tempNameFULL[iii+1:]
                    tempNameFULL=tempNameO
            currentName=tempNameFULL.strip()
             
            NameforSave="Rescaled_"+currentName+"_ID_"+str(FUAIdTemp)+"_1km"
            # uncomment to save picture
            #===================================================================
            # AddressforSave="M://RMSC_step2_SeperatePlots_ExtractedNO2_ALLCity//"+NameforSave+'.jpg'
            # plt.savefig(AddressforSave,bbox_inches='tight')
            # plt.clf()
            # plt.close('all')
            #===================================================================
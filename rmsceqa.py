# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
import matplotlib
from tkinter.test.test_tkinter.test_font import fontname
from matplotlib.font_manager import FontProperties
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
from pylab import *
from dbfread import DBF
import math
from test.test_functools import decimal

xls = pd.read_csv("M://Eclipse_Workspace//Article2_Kriging_Py//MeCel1000GauKri_SelectedCitywMinFUA.csv",encoding = 'unicode_escape',low_memory = False)
b=xls.groupby('eFUA_name').agg({'FUA_p_2015':['mean'], 'CBDPoiRs1k':['max','min']})#find the max and min Euclidean distance of each city
b.columns = ['popSize','maxDistperCity','minDistperCity']
refPop = max(b['popSize'])#max population of 378 FUA
refDist = (max(b['maxDistperCity']))/1000#max Euclidean distance of 378 FUA
minrefDist= (min(b['minDistperCity']))/1000#min Euclidean distance of 378 FUA
refPopName = b['popSize'].idxmax()#Paris
sortedB = xls.sort_values(by=['FUA_p_2015'], ascending=False)#reorder df so bigger cities come up on top of scatterplot
rank=pd.Series(sortedB['eFUA_name']).unique() #to see levels
 
Pop=np.round(np.array(sortedB.iloc[0:104272,15].tolist()),decimals=6)#population of selected cities
distanceinM=np.round(np.array(sortedB.iloc[0:104272,28].tolist()),decimals=6)#distance in meters of selected cities
NO2=np.round(np.array(sortedB.iloc[0:104272,38].tolist()),decimals=6)#extracted no2 in meters of selected cities
cityName=sortedB.iloc[0:104272,19].tolist()#city name of selected cities
logPop2015=np.round(sortedB.iloc[0:104272,36].tolist(),decimals=6)#log10 population selected cities
PopRank=np.round(sortedB.iloc[0:104272,35].tolist())#population rank of selected cities
FUAId=np.round(np.array(sortedB.iloc[0:104272,6].tolist()))#FUA ID of selected cities
 
distance=np.round(distanceinM/1000,decimals=6) # in km
 
ScaleDist=arange(0,1.05,0.05) #will get a list begin at 0, ends at 1, with an interval of 0.05
ScaleNO2=arange(0,1.05,0.05) #will get a list begin at 0, ends at 1, with an interval of 0.05
DistRuler=arange(ceil(minrefDist),ceil(refDist)+5,1) # the interval of the distance is 1km, with an interval of 1km
   
ScaleDisttemp=[]
ScaleNO2temp=[]
Disttemp=[]
RMSCtemp=[]
pearsonMask=[]
    
for idist in range(len(ScaleDist)):
    for jno2 in range(len(ScaleNO2)):
            
        distanceRescale=distance/((Pop/refPop)**ScaleDist[idist]) #rescaled distance
        NO2Rescaled=NO2/((Pop/refPop)**ScaleNO2[jno2]) #rescaled no2
            
        for kruler in range(len(DistRuler)):
            ScaleDisttemp.append(ScaleDist[idist]) #record the current scale of distance
            ScaleNO2temp.append(ScaleNO2[jno2]) #record the current scale of no2
            Disttemp.append(DistRuler[kruler]) #to record the current ring
            DistJudMask=[] #try different values of rings by generating different masks, as a way of finding the best threshold
            for ijudDist in range(len(distanceRescale)):  
                if distanceRescale[ijudDist]>=DistRuler[kruler]:
                    DistJudMask.append(np.nan)
                else:
                    DistJudMask.append(1)
            DistJudMask=np.array(DistJudMask)
            #print(DistRuler[kruler])
            distanceRescaleCopy1=distanceRescale[:]
            NO2RescaledCopy1=NO2Rescaled[:]
            logPopCopy1=logPop2015[:]
            FUAIdCopy1=FUAId[:]
            # filter the values of dist, no2 according to the distance threshold, the according logpop and fuaid are also found
            distanceRescaleCopy=distanceRescaleCopy1*DistJudMask  
            NO2RescaledCopy=NO2RescaledCopy1*DistJudMask
            logPopCopy=logPopCopy1*DistJudMask
            FUAIdCopy=FUAIdCopy1*DistJudMask
            # drop nan
            distanceRescaleOP = [x for x in distanceRescaleCopy if math.isnan(x) == False]
            NO2RescaledOP = [y for y in NO2RescaledCopy if math.isnan(y) == False]
            logPopOP = [z for z in logPopCopy if math.isnan(z) == False]
            FUAIdOP = [k for k in FUAIdCopy if math.isnan(k) == False]
            # create a dictionary so that we can use groupby to summarize
            tempDict={'distanceT':distanceRescaleOP, 'NO2RescaledT':NO2RescaledOP, 'logPopT':logPopOP,'FUAIdT':FUAIdOP}
            tempFrame=pd.DataFrame(tempDict)
            tempPearson=tempFrame.groupby('FUAIdT')[['logPopT','NO2RescaledT']].corr().iloc[0::2,-1].tolist() #calculate pearson between scaled no2 and logpop
            tempPearsonNonan = np.array([yz for yz in tempPearson if math.isnan(yz) == False]) #drop the rows where pearson is nan (when the std is 0)
            rmsc=np.sqrt((sum(tempPearsonNonan**2))/len(tempPearsonNonan)) #rmsc equation
            RMSCtemp.append(rmsc)
            if len(tempPearsonNonan)==30:  #when calculating rmsc we make sure that only consider the situation where 30 pearson values appear
                pearsonMask.append(1)
            else:
                pearsonMask.append(np.nan)
   
pearsonMaskAY=np.array(pearsonMask) #only consider the situation where 30 pearson values appear simultaneously
ScaleDisttempN=np.array(ScaleDisttemp)*pearsonMaskAY
ScaleNO2tempN=np.array(ScaleNO2temp)*pearsonMaskAY
DisttempN=np.array(Disttemp)*pearsonMaskAY
RMSCtempN=np.array(RMSCtemp)*pearsonMaskAY
   
ScaleDistFinal = np.array([ed1 for ed1 in ScaleDisttempN if math.isnan(ed1) == False]) #drop na values
ScaleNO2Final = np.array([ed2 for ed2 in ScaleNO2tempN if math.isnan(ed2) == False]) #drop na values
DistFinal = np.array([ed3 for ed3 in DisttempN if math.isnan(ed3) == False]) #drop na values
RMSCFinal = np.array([ed4 for ed4 in RMSCtempN if math.isnan(ed4) == False]) #drop na values
   
ScaleDistFinalList=ScaleDistFinal.tolist()
ScaleNO2FinalList=ScaleNO2Final.tolist()
DistFinalList=DistFinal.tolist()
RMSCFinalList=RMSCFinal.tolist()

print(min(RMSCFinalList)) #result 5.11045796214497e-15 minimum rmsc values
Indexlocation=RMSCFinalList.index(min(RMSCFinalList)) 
print(ScaleDistFinalList[Indexlocation]) #result  0.45 scaling factor of distance
print(ScaleNO2FinalList[Indexlocation]) #result 0.9500000000000001 scaling factor of no2
print(DistFinalList[Indexlocation]) # 93.0 distance threshold
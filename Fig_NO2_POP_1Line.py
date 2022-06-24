# coding=utf-8
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.graphics.gofplots import ProbPlot
import scipy
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from sympy import pretty_print as su
from scipy.stats import pearsonr
from scipy.ndimage.filters import gaussian_filter1d
import tkinter
import matplotlib
from statsmodels.formula.api import ols

matplotlib.use('TkAgg')

xls = pd.ExcelFile('M://maintextTable.xlsx')
df1 = pd.read_excel(xls,'meanNO2-ps')
popSize=df1.iloc[0:42,3].tolist() 
meanNO2=df1.iloc[0:42,4].tolist()
sourceType=df1.iloc[0:42,5].tolist()

logPopSize=[]
for i in popSize:
    logPopSize.append(math.log(i,10))
    
logmeanNO2=[]
for j in meanNO2:
    logmeanNO2.append(math.log(j,10))

poly2 = np.polyfit(logPopSize,logmeanNO2,1)
p2 = np.poly1d(poly2)

ValmeanNO2=logPopSize[:]
for k in range(len(ValmeanNO2)):
    ValmeanNO2[k]=ValmeanNO2[k]*poly2[0]+poly2[1]

exp10ValmeanNO2=ValmeanNO2[:]
for kk in range(len(exp10ValmeanNO2)):
    exp10ValmeanNO2[kk]=10**ValmeanNO2[kk]
  
fig = plt.figure()
ax = plt.subplot()
# 
poly1 = np.polyfit(logPopSize,meanNO2,1)
p1 = np.poly1d(poly1)
fittedLineX1=np.linspace(min(list(logPopSize)),max(list(logPopSize)),3000)

model2 = ols('meanNO2 ~ 0+logPopSize', data=df1).fit() 

aa=model2.params[0]

YInter0=[]
for i in range(len(fittedLineX1)):
    YInter0.append(fittedLineX1[i]*aa)



fittedValMed=p2(fittedLineX1)
fittedVal=fittedValMed[:]
for mm in range(len(fittedValMed)):
    fittedVal[mm]=10**fittedVal[mm]

tempstring = u"mean NO₂ surface concentration (μg/m³)"
titlestring = u"mean NO₂ surface concentration (μg/m³)"
linelegend = u"mean(NO₂) = 5.1027 * pop$^ {0.1622}$ (log-log fit), R$^2$ = 0.7111"
esstring = u"Baró et al. 2015"


listsForLogPopSize = [[] for ii1 in range(len(sourceType))]
listsForMeanNO2= [[] for ii2 in range(len(sourceType))]
for uu in range(len(logPopSize)):
    md=logPopSize[uu]
    nd=meanNO2[uu]
    listsForLogPopSize[uu].append(md)
    listsForMeanNO2[uu].append(nd)

sourceTypeSet=list(set(sourceType))

LogPopMarker = [[] for ii3 in range(max(sourceTypeSet))]
meanNO2Marker = [[] for ii4 in range(max(sourceTypeSet))]

indexListMax=[]
indexListMin=[]
for ii5 in sourceTypeSet:
    aa=[i for i,x in enumerate(sourceType) if x==ii5]
    indexListMin.append(min(aa))
    indexListMax.append(max(aa))

def sumlist(listEx,minRange,maxRange):
    sumlistOp=[]
    for i in range(minRange,maxRange+1):
        sumlistOp=sumlistOp+listEx[i]
    return sumlistOp

for ii6 in range(len(sourceTypeSet)):
    LogPopMarker[ii6]=sumlist(listsForLogPopSize,indexListMin[ii6],indexListMax[ii6])
    meanNO2Marker[ii6]=sumlist(listsForMeanNO2,indexListMin[ii6],indexListMax[ii6])

makertype = ['o', 'x','^','1','3','v','<','>','s']
for mk in range(len(LogPopMarker)):
     ax.scatter(LogPopMarker[mk], meanNO2Marker[mk], marker=makertype[mk],color='k')


ax.plot(fittedLineX1, fittedVal,color='k',label='fitted values')


ax.set_xlabel('population')
ax.set_ylabel(tempstring)


legend_elements = [Line2D([0], [0], marker='o',color='k',label='Nguyen & Kim 2006 urban/nontraffic bg.',markersize=6,linewidth=0),
                   Line2D([0], [0], marker='x', color='k', label='Nguyen & Kim 2006 traffic bg.',markersize=6,linewidth=0),
                   Line2D([0], [0], marker='^', color='k', label='Lertxundi-Manterola & Saez 2009', markersize=6,linewidth=0),
                   Line2D([0], [0], marker='1', color='k', label='Masiol et al. 2013 urban/nontraffic bg.', markersize=6,linewidth=0),
                   Line2D([0], [0], marker='3', color='k', label='Masiol et al. 2013 traffic bg.', markersize=6,linewidth=0),
                   Line2D([0], [0], marker='v', color='k', label='Singh & Kulshrestha 2014', markersize=6,linewidth=0),
                   Line2D([0], [0], marker='<', color='k', label='Singh & Kulshrestha 2014 (winter)', markersize=6,linewidth=0),
                   Line2D([0], [0], marker='>', color='k', label='Singh & Kulshrestha 2014 (summer)', markersize=6,linewidth=0),
                   Line2D([0], [0], marker='s', color='k', label=esstring, markersize=6,linewidth=0),
                    Line2D([0], [0], color='k', lw=1.5, label=linelegend )]
ax.legend(handles=legend_elements, loc='best')
#ax.set_title(titlestring)
 
plt.xticks(range(3, 8), ['1E3', '1E4', '1E5', '1E6', '1E7'])
plt.show()





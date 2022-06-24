# coding=utf-8
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import tkinter
import matplotlib
from statsmodels.formula.api import ols

matplotlib.use('TkAgg')

xls = pd.ExcelFile('M://maintextTable.xlsx')
df1 = pd.read_excel(xls,'maxUHI-ps')
popSize=df1.iloc[0:57,3].tolist()
maxUHI=df1.iloc[0:57,4].tolist()
sourceType=df1.iloc[0:57,5].tolist()

logPopSize=[]
for i in popSize:
    logPopSize.append(math.log(i,10))
    
logmaxUHI=[]
for j in maxUHI:
    logmaxUHI.append(math.log(j,10))
 
poly2 = np.polyfit(logPopSize,logmaxUHI,1)
p2 = np.poly1d(poly2)

ValmaxUHI=logPopSize[:]
for k in range(len(ValmaxUHI)):
    ValmaxUHI[k]=ValmaxUHI[k]*poly2[0]+poly2[1]

exp10ValmaxUHI=ValmaxUHI[:]
for kk in range(len(exp10ValmaxUHI)):
    exp10ValmaxUHI[kk]=10**ValmaxUHI[kk]
  
fig = plt.figure()
ax = plt.subplot()

poly1 = np.polyfit(logPopSize,maxUHI,1)
p1 = np.poly1d(poly1)
fittedLineX1=np.linspace(min(list(logPopSize)),max(list(logPopSize)),3000)

model2 = ols('maxUHI ~ 0+logPopSize', data=df1).fit() 

aa=model2.params[0]

YInter0=[]
for i in range(len(fittedLineX1)):
    YInter0.append(fittedLineX1[i]*aa)

fittedValMed=p2(fittedLineX1)
fittedVal=fittedValMed[:]
for mm in range(len(fittedValMed)):
    fittedVal[mm]=10**fittedVal[mm]

tempstring = u"maximum UHI intensity (°C)"
titlestring = u"maximum UHI intensity (°C)"

listsForLogPopSize = [[] for ii1 in range(len(sourceType))]
listsForMaxUHI= [[] for ii2 in range(len(sourceType))]
for uu in range(len(logPopSize)):
    md=logPopSize[uu]
    nd=maxUHI[uu]
    listsForLogPopSize[uu].append(md)
    listsForMaxUHI[uu].append(nd)

sourceTypeSet=list(set(sourceType))

LogPopMarker = [[] for ii3 in range(max(sourceTypeSet))]
maxUHIMarker = [[] for ii4 in range(max(sourceTypeSet))]

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
    maxUHIMarker[ii6]=sumlist(listsForMaxUHI,indexListMin[ii6],indexListMax[ii6])

makertype = ['o', '1','x','^']
for mk in range(len(LogPopMarker)):
     ax.scatter(LogPopMarker[mk], maxUHIMarker[mk], marker=makertype[mk],color='k')


ax.plot(fittedLineX1, p1(fittedLineX1),color='k')

ax.plot(fittedLineX1, YInter0,color='k',label='fitted value1',linestyle='--')
ax.plot(fittedLineX1, fittedVal,color='k',label='fitted values',linestyle='-.')
 
ax.set_xlabel('population')
ax.set_ylabel(tempstring)

legend_elements = [Line2D([0], [0], marker='o',color='k',label='Oke 1973',markerfacecolor='k',markersize=8,linewidth=0),
                   Line2D([0], [0], marker='1',label='Oke & Maxwell 1975',color='k',markersize=8,linewidth=0),
                   Line2D([0], [0], marker='x', color='k', label='Torok et al. 2001',markerfacecolor='k',markersize=8,linewidth=0),
                   Line2D([0], [0], marker='^', color='k', label='Sakakibara & Matsui 2005',markerfacecolor='k', markersize=8,linewidth=0),
                    Line2D([0], [0], color='k', lw=1.5, label='max(UHI) = 2.0401 * log(pop) - 3.6879'),
                    Line2D([0], [0], color='k', linestyle='--',lw=1.5, label='max(UHI) = 1.3006 * log(pop)'),
                    Line2D([0], [0], color='k', linestyle='-.',lw=1.5, label='max(UHI) = 0.9032 * pop$^{0.1625}$ (log-log fit)')
                    ]
ax.legend(handles=legend_elements, loc='best')

plt.xticks(range(2, 8), ['1E2', '1E3', '1E4', '1E5', '1E6','1E7'])
plt.show()

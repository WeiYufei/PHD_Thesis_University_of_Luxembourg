# coding=utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pandas import Series,DataFrame

matplotlib.use('TkAgg')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica']

xls = pd.ExcelFile("M://Regression_Cell_w_MinValue_equalCellDeleted.xlsx")
 
df1 = pd.read_excel(xls,'Sheet1')
FuaName=df1.iloc[0:24239,12].tolist()
minFUAValue=df1.iloc[0:24239,30].tolist()
Pop2015=df1.iloc[0:24239,18].tolist()

fig = plt.figure(figsize=(4, 3.5),dpi=300)
ax = plt.subplot()

listByPop = [i for _,i in sorted(zip(Pop2015,FuaName))]
listByPopLH = list(set(listByPop))
listByPopLH.sort(key=listByPop.index,reverse=True)
#print(listByPopHL)

listByminFUA = [j for _,j in sorted(zip(minFUAValue,FuaName))]
listByminFUAHL = list(set(listByminFUA))
listByminFUAHL.sort(key=listByminFUA.index,reverse=True)
#print(listByminFUAHL)

indexOfPop=[]
for k in range(len(listByPopLH)):
    aa=listByPopLH.index(listByPopLH[k])
    indexOfPop.append(aa)
#print(indexOfPop)

indexOfminFUA=[]
for m in range(len(listByminFUAHL)):
    bb=listByminFUAHL[m]
    for n in range(len(listByPopLH)):
        if listByPopLH[n]==bb:
            cc=indexOfPop[n]
            indexOfminFUA.append(cc)
#print(indexOfminFUA)
arrayPop = np.array(indexOfPop)
arrayMinFUA = np.array(indexOfminFUA)
location=arrayPop-arrayMinFUA
#print(arrayPop+1)
popRankforShow=arrayPop+1#range 1-378, rank pop from high to low, 1st is Istanbul
MinFUAforPlot=arrayMinFUA+1#range 1-378, city with highest minfua range first.e.g. the first number is 63, means this city Dusseldorf has the highest minFUA and its population ranked 63th (1st pop city is Istanbul)
#print(MinFUAforPlot)
RankMinFUA_Xlist=[]
RankPop_Ylist=[]
FuaforPlot=listByminFUAHL
for ii in range(len(MinFUAforPlot)):
    xx=ii+1
    RankMinFUA_Xlist.append(xx)
    yy=MinFUAforPlot[ii]
    RankPop_Ylist.append(yy)
    
RankMinFUA_X=np.array(RankMinFUA_Xlist)
RankPop_Y=np.array(RankPop_Ylist)
rankChange=abs(RankMinFUA_X-RankPop_Y)

lessthan50=0
between50100=0
between100200=0
largerthan200=0

maklist=[]
for k in range(len(rankChange)):
    if rankChange[k]<50:
        lessthan50=lessthan50+1
    elif rankChange[k]>=50 and rankChange[k]<100:
        between50100=between50100+1  
    elif rankChange[k]>=100 and rankChange[k]<200:
        between100200=between100200+1
    elif rankChange[k]>=200:
        largerthan200=largerthan200+1  

numlist=[lessthan50,between50100,between100200,largerthan200]
#print(numlist)
labelList=['D < 50','50 <= D < 100','100 <= D < 200','D >= 200']
plt.bar(range(len(numlist)),numlist,tick_label=labelList)

x=[0,1,2,3]
for a,b in zip(x,numlist):
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=5,family='Helvetica')

plt.xlabel('D = $|$Rank of P - Rank of C$_{min}$$|$', family='Helvetica',size=5)
plt.ylabel('N', family='Helvetica',size=5)
plt.xticks(fontproperties='Helvetica',size=5)
plt.yticks(fontproperties='Helvetica',size=5)
fig.tight_layout()
framewidth=0.5
ax.spines['top'].set_linewidth(framewidth)
ax.spines['bottom'].set_linewidth(framewidth)
ax.spines['left'].set_linewidth(framewidth)
ax.spines['right'].set_linewidth(framewidth)
ax.xaxis.set_tick_params(width=0.5)
ax.yaxis.set_tick_params(width=0.5)
plt.show()

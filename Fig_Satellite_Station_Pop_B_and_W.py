# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
import matplotlib
from tkinter.test.test_tkinter.test_font import fontname
from matplotlib.font_manager import FontProperties

xls = pd.ExcelFile("M://Eclipse_Workspace//Article1_NC_R//Regression_OverlappedCell_w_Station.xlsx")
 
df1 = pd.read_excel(xls,'overlappCellStation')
FuaName=df1.iloc[0:378,0].tolist()
aveAveCell=df1.iloc[0:378,3].tolist()
Pop2015=df1.iloc[0:378,2].tolist()
aveAveStation=df1.iloc[0:378,1].tolist()

matplotlib.use('TkAgg')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica']

fig = plt.figure(figsize=(4, 3.5),dpi=300)
ax = plt.subplot()

maklist=[]
for k in range(len(Pop2015)):
    if Pop2015[k]<100000:
        maklist.append('o')
    elif Pop2015[k]>=100000 and Pop2015[k]<1000000:
        maklist.append('1')  
    elif Pop2015[k]>=1000000 and Pop2015[k]<10000000:
        maklist.append('x')
    elif Pop2015[k]>=10000000:
        maklist.append('^')   

poly1Temp = np.polyfit(aveAveStation,aveAveCell,1)
p1Temp = np.poly1d(poly1Temp)
fittedLineX=np.linspace(min(list(aveAveStation)),max(list(aveAveStation)),100)
#print (poly1Temp)
#print (p1Temp)

legend_elements = [Line2D([0], [0], marker='o',color='black', label='$\hat{C}$$_{f}$ = 1.1739*G$_{f}$ + 24.5667 \n (R$^2$ = 0.1919)',markersize=0,linewidth=0.5),
                   Line2D([0], [0], marker='o',color='black', label='P  < 1e5',markersize=2.5,linewidth=0),
                   Line2D([0], [0], marker='1',color='black', label='P $\in$ [1e5, 1e6)',markersize=2.5,linewidth=0),
                   Line2D([0], [0], marker='x',color='black', label='P $\in$ [1e6, 1e7)',markersize=2.5,linewidth=0),
                   Line2D([0], [0], marker='^',color='black', label='P $\geq$ 1e7',markersize=2.5,linewidth=0)]

plt.legend(prop={'family':'Helvetica','size':5},handles=legend_elements, loc='best',frameon=False,borderpad=0.5)

ax.plot(fittedLineX, p1Temp(fittedLineX),color='black',label='fitted values',linewidth=0.5)

for iia in range(len(Pop2015)):
    ax.plot(aveAveStation[iia], aveAveCell[iia],marker=maklist[iia],markersize=2.5,color='black')

for ii in range(len(FuaName)):
    ax.text(aveAveStation[ii], aveAveCell[ii], str(FuaName[ii]), color='blue',size=5, fontdict=None)
plt.xlabel('G$_{f}$ (μg/m$^3$)', family='Helvetica',size=5)
plt.ylabel('C$_{f}$ (μmol/m$^2$)', family='Helvetica',size=5)
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
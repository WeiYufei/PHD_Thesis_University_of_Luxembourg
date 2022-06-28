# coding=utf-8
import math
import scipy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
import matplotlib
from scipy.optimize import curve_fit
import uncertainties as unc
import uncertainties.unumpy as unp
from matplotlib.ticker import FuncFormatter
import matplotlib.patches as mpatches
matplotlib.use('TkAgg')

xls = pd.ExcelFile("M://Regression_Station.xlsx")
 
df1 = pd.read_excel(xls,'Sheet1')
FUAId=df1.iloc[0:1398,25].tolist()
FUAName=df1.iloc[0:1398,28].tolist()
NO2AveStation=df1.iloc[0:1398,21].tolist()
Dist=df1.iloc[0:1398,45].tolist()
Pop2015=df1.iloc[0:1398,34].tolist()
 
#===============================================================================
# #uncomment to see original data points (a portion)
# Dist_5E45E5=[]
# Dist_5E55E6=[]
# Dist_5E615E6=[]
# FUAID_5E45E5=[]
# FUAID_5E55E6=[]
# FUAID_5E615E6=[]
# FUAName_5E45E5=[]
# FUAName_5E55E6=[]
# FUAName_5E615E6=[]
# NO2AveStation_5E45E5=[]
# NO2AveStation_5E55E6=[]
# NO2AveStation_5E615E6=[]
#===============================================================================
#===============================================================================
# #uncomment to see original data points (a portion)
# for i in range(len(Pop2015)):
#     if Pop2015[i]>=50000 and Pop2015[i]<=150000 and Dist[i]<=10000:
#         Dist_5E45E5.append(Dist[i])
#         NO2AveStation_5E45E5.append(NO2AveStation[i])
#         FUAID_5E45E5.append(FUAId[i])
#         FUAName_5E45E5.append(FUAName[i])
#     elif Pop2015[i]>=500000 and Pop2015[i]<=1500000 and Dist[i]<=10000:
#         Dist_5E55E6.append(Dist[i])
#         NO2AveStation_5E55E6.append(NO2AveStation[i])
#         FUAID_5E55E6.append(FUAId[i])
#         FUAName_5E55E6.append(FUAName[i])
#     elif Pop2015[i]>=5000000 and Pop2015[i]<=15000000 and Dist[i]<=10000:
#         Dist_5E615E6.append(Dist[i])
#         NO2AveStation_5E615E6.append(NO2AveStation[i])
#         FUAID_5E615E6.append(FUAId[i])
#         FUAName_5E615E6.append(FUAName[i])
#===============================================================================
 
distline1 = np.arange(50,10000,50)
distline = distline1.tolist()
   
logDis=[]
for ijj in distline:
    logDis.append(math.log(ijj,10))   
  
LogStation1e5=[]
for i in range(len(logDis)):
    a=-0.1763*logDis[i]+0.2208*(math.log(100000,10))+0.7278
    LogStation1e5.append(a)
  
UnLogStation1e5=[]
for i1 in range(len(LogStation1e5)):
    ai=10**LogStation1e5[i1]
    UnLogStation1e5.append(ai)
  
LogStation1e6=[]
for j in range(len(logDis)):
    b=-0.1763*logDis[j]+0.2208*(math.log(1000000,10))+0.7278
    LogStation1e6.append(b)
      
UnLogStation1e6=[]
for i2 in range(len(LogStation1e6)):
    bi=10**LogStation1e6[i2]
    UnLogStation1e6.append(bi)
    
LogStation1e7=[]
for k in range(len(logDis)):
    c=-0.1763*logDis[k]+0.2208*(math.log(10000000,10))+0.7278
    LogStation1e7.append(c)
  
UnLogStation1e7=[]
for i3 in range(len(LogStation1e7)):
    ci=10**LogStation1e7[i3]
    UnLogStation1e7.append(ci)
 
logDisForInterval=[]
for iii1 in range(len(Dist)):
    aa1=math.log(Dist[iii1],10)
    logDisForInterval.append(aa1)
 
logPopForInterval=[]
for iii2 in range(len(Pop2015)):
    aa2=math.log(Pop2015[iii2],10)
    logPopForInterval.append(aa2)
 
logNO2ForInterval=[]
for iii3 in range(len(NO2AveStation)):
    aaa3=NO2AveStation[iii3]
    aa3=math.log(aaa3,10)
    logNO2ForInterval.append(aa3)
     
 
def f(x,a, b,c):
    return a*x[0]+b*x[1]+c
logPopAY=np.array(logPopForInterval)
logDisAY=np.array(logDisForInterval)
logNO2AY=np.array(logNO2ForInterval)
 
x = scipy.array([logDisForInterval,logPopForInterval])
y=logNO2ForInterval
popt, pcov = curve_fit(f, x, y)
a,b,c = unc.correlated_values(popt, pcov)
#===============================================================================
# print('a: ' + str(a))
# print('b: ' + str(b))
# print('c: ' + str(c))
#===============================================================================
 
pxplot=[]
for ipx in range(len(distline1)):
    qa=math.log(distline1[ipx],10)
    pxplot.append(qa)
pxplotAY=np.array(pxplot)
 
py1E5 = 10**(a*pxplotAY+b*5+c)
py1E6 = 10**(a*pxplotAY+b*6+c)
py1E7 = 10**(a*pxplotAY+b*7+c)
 
nom1E5 = unp.nominal_values(py1E5)
std1E5 = unp.std_devs(py1E5)
 
nom1E6 = unp.nominal_values(py1E6)
std1E6 = unp.std_devs(py1E6)
 
nom1E7 = unp.nominal_values(py1E7)
std1E7 = unp.std_devs(py1E7)
 
fig = plt.figure(figsize=(4, 3.5),dpi=300)
ax = plt.subplot()
 
plt.fill_between(distline1,nom1E5-1.96*std1E5,nom1E5+1.96*std1E5,color="silver",alpha=0.4)
plt.fill_between(distline1,nom1E6-1.96*std1E6,nom1E6+1.96*std1E6,color="silver",alpha=0.4)
plt.fill_between(distline1,nom1E7-1.96*std1E7,nom1E7+1.96*std1E7,color="silver",alpha=0.4)
 
ax.plot(distline, UnLogStation1e5,linestyle='solid', color='black',linewidth=0.5)
ax.plot(distline, UnLogStation1e6,linestyle='dashed', color='black',linewidth=0.5)
ax.plot(distline, UnLogStation1e7,linestyle='dashdot', color='black',linewidth=0.5)
 
#===============================================================================
# #uncomment to see original data points (a portion)
# ax.scatter(Dist_5E45E5, NO2AveStation_5E45E5,color='green',s=5)
# ax.scatter(Dist_5E55E6, NO2AveStation_5E55E6,color='blue',s=5)
# ax.scatter(Dist_5E615E6, NO2AveStation_5E615E6,color='red',s=5)
#===============================================================================

def formatnumX(x, pos): #Scientific notation
    return '%.0f' % (x/1000)
formatter1 = FuncFormatter(formatnumX)#Scientific notation
ax.xaxis.set_major_formatter(formatter1)
   
ax.set_xlabel('R (km)',family='Helvetica',size=5)
ax.set_ylabel('$\hat{G}$ (μg/m$^3$)',family='Helvetica',size=5)
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
ax.set_ylim(bottom=0)
 
gray_patch = mpatches.Patch(edgecolor=None, facecolor='silver', alpha=0.4,label='95% confidence interval')
 
legend_elements = [Line2D([0], [0], marker='o',linestyle='solid', label='P = 1e5',color='black',markersize=0,linewidth=0.5),
                   Line2D([0], [0], marker='o',linestyle='dashed', label='P = 1e6',color='black',markersize=0,linewidth=0.5),
                   Line2D([0], [0], marker='o',linestyle='dashdot', label='P = 1e7',color='black',markersize=0,linewidth=0.5),
                   gray_patch]
   
ax.legend(prop={'family':'Helvetica','size':5},handles=legend_elements, loc='best',frameon=False,borderpad=0.5)
   
plt.show()
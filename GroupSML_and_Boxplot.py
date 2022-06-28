#coding=utf-8
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt    
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

xls = pd.ExcelFile("M://Regression_Cell.xlsx")

df1 = pd.read_excel(xls,'Sheet 1')
FUAId=df1.iloc[0:24817,9].tolist()
FUAName=df1.iloc[0:24817,12].tolist()
NO2AveSatellite=df1.iloc[0:24817,3].tolist()
Dist=df1.iloc[0:24817,29].tolist()
Pop2015=df1.iloc[0:24817,18].tolist()

Pop2015Set=list(set(Pop2015))

PopBand=[]
per0=np.percentile(Pop2015Set,0)
per10=np.percentile(Pop2015Set,10)
per45=np.percentile(Pop2015Set,45)
per55=np.percentile(Pop2015Set,55)
per90=np.percentile(Pop2015Set,90)
per100=np.percentile(Pop2015Set,100)

PopBand=[per0,per10,per45,per55,per90,per100]
#print(PopBand)
LineUp=[]
LineMid=[]
LineDow=[]
for i in range(len(Pop2015)):
    if Pop2015[i]>=per0 and Pop2015[i]<=per10:
        LineDow.append(Pop2015[i])
    elif Pop2015[i]>=per45 and Pop2015[i]<=per55:
        LineMid.append(Pop2015[i])
    elif Pop2015[i]>=per90 and Pop2015[i]<=per100:
        LineUp.append(Pop2015[i])

forPlotDisU=[]
forPlotNO2U=[]
for j in range(len(Pop2015)):
    if Pop2015[j]>=per90 and Pop2015[j]<=per100:
        forPlotDisU.append(Dist[j])
        forPlotNO2U.append(NO2AveSatellite[j])

forPlotDisM=[]
forPlotNO2M=[]
for k in range(len(Pop2015)):
    if Pop2015[k]>=per45 and Pop2015[k]<=per55:
        forPlotDisM.append(Dist[k])
        forPlotNO2M.append(NO2AveSatellite[k])

forPlotDisD=[]
forPlotNO2D=[]
for m in range(len(Pop2015)):
    if Pop2015[m]>=per0 and Pop2015[m]<=per10:
        forPlotDisD.append(Dist[m])
        forPlotNO2D.append(NO2AveSatellite[m])

distlineU=np.arange(min(forPlotDisU),max(forPlotDisU),50).tolist()
distlineM=np.arange(min(forPlotDisM),max(forPlotDisM),50).tolist()
distlineD=np.arange(min(forPlotDisD),max(forPlotDisD),50).tolist()

logDisU=[]
for ijj1 in distlineU:
    logDisU.append(math.log(ijj1,10))   
    
logDisM=[]
for ijj2 in distlineM:
    logDisM.append(math.log(ijj2,10)) 
    
logDisD=[]
for ijj3 in distlineD:
    logDisD.append(math.log(ijj3,10)) 

LogStatelliteD=[]
for iqw1 in range(len(logDisD)):
    ak=-0.1823*logDisD[iqw1]+0.2161*(math.log(mean(LineDow),10))+1.2004
    LogStatelliteD.append(ak)

UnLogStatelliteD=[]
for i1 in range(len(LogStatelliteD)):
    UnLogStatelliteD.append(10**LogStatelliteD[i1])

LogStatelliteM=[]
for iqw2 in range(len(logDisM)):
    bk=-0.1823*logDisM[iqw2]+0.2161*(math.log(mean(LineMid),10))+1.2004
    LogStatelliteM.append(bk)
  
UnLogStatelliteM=[]
for i2 in range(len(LogStatelliteM)):
    UnLogStatelliteM.append(10**LogStatelliteM[i2])

LogStatelliteU=[]
for iqw3 in range(len(logDisU)):
    ck=-0.1823*logDisU[iqw3]+0.2161*(math.log(mean(LineUp),10))+1.2004
    LogStatelliteU.append(ck)

UnLogStatelliteU=[]
for i3 in range(len(LogStatelliteU)):
    UnLogStatelliteU.append(10**LogStatelliteU[i3])
    
print(mean(LineUp))
print(len(set(LineUp)))
print(mean(LineMid))
print(len(set(LineMid)))
print(mean(LineDow))
print(len(set(LineDow)))
 
print(max(LineUp))
print(max(LineMid))
print(max(LineDow))

print(min(LineUp))
print(min(LineMid))
print(min(LineDow))
  
  
print(max(distlineU))
print(max(distlineM))
print(max(distlineD))
  
print(min(distlineU))
print(min(distlineM))
print(min(distlineD))

pxplotU=[]
for ipx1 in range(len(distlineU)):
    pxplotU.append(math.log(distlineU[ipx1],10))
pxplotAYU=np.array(pxplotU)

pxplotD=[]
for ipx2 in range(len(distlineD)):
    pxplotD.append(math.log(distlineD[ipx2],10))
pxplotAYD=np.array(pxplotD)

pxplotM=[]
for ipx3 in range(len(distlineM)):
    pxplotM.append(math.log(distlineM[ipx3],10))
pxplotAYM=np.array(pxplotM)

logDisForInterval=[]
for iii1 in range(len(Dist)):
    logDisForInterval.append(math.log(Dist[iii1],10))

logPopForInterval=[]
for iii2 in range(len(Pop2015)):
    logPopForInterval.append(math.log(Pop2015[iii2],10))

logNO2ForInterval=[]
for iii3 in range(len(NO2AveSatellite)):
    logNO2ForInterval.append(math.log(NO2AveSatellite[iii3],10))
    
def f(x,a, b,c):
    return a*x[0]+b*x[1]+c

x = scipy.array([logDisForInterval,logPopForInterval])
y=logNO2ForInterval
popt, pcov = curve_fit(f, x, y)
a,b,c = unc.correlated_values(popt, pcov)

py1ED = 10**(a*pxplotAYD+b*(math.log(mean(LineDow),10))+c)
py1EM = 10**(a*pxplotAYM+b*(math.log(mean(LineMid),10))+c)
py1EU = 10**(a*pxplotAYU+b*(math.log(mean(LineUp),10))+c)
 
nom1ED = unp.nominal_values(py1ED)
std1ED = unp.std_devs(py1ED)
  
nom1EM = unp.nominal_values(py1EM)
std1EM = unp.std_devs(py1EM)
  
nom1EU = unp.nominal_values(py1EU)
std1EU = unp.std_devs(py1EU)

fig = plt.figure(figsize=(4, 3.5),dpi=300)
ax = plt.subplot()

plt.fill_between(distlineD,nom1ED-1.96*std1ED,nom1ED+1.96*std1ED,color="silver",alpha=0.4)
plt.fill_between(distlineM,nom1EM-1.96*std1EM,nom1EM+1.96*std1EM,color="silver",alpha=0.4)
plt.fill_between(distlineU,nom1EU-1.96*std1EU,nom1EU+1.96*std1EU,color="silver",alpha=0.4)
 
ax.plot(distlineD, UnLogStatelliteD,linestyle='solid', color='black',linewidth=0.5)
ax.plot(distlineM, UnLogStatelliteM,linestyle='dashed', color='black',linewidth=0.5)
ax.plot(distlineU, UnLogStatelliteU,linestyle='dashdot', color='black',linewidth=0.5)

intvalBoxU=list(np.arange(min(forPlotDisU), max(forPlotDisU), 5000))
intvalBoxM=list(np.arange(min(forPlotDisM), max(forPlotDisM), 5000))
intvalBoxD=list(np.arange(min(forPlotDisD), max(forPlotDisD), 5000))

intvalBoxU.append(max(forPlotDisU))
intvalBoxM.append(max(forPlotDisM))
intvalBoxD.append(max(forPlotDisD))

judHeadU=[]
judTailU=[]
judgeMidU=[]
for judU in range(len(intvalBoxU)-1):
    judHeadU.append(intvalBoxU[judU])
    judTailU.append(intvalBoxU[judU+1])
    judgeMidU.append((intvalBoxU[judU]+intvalBoxU[judU+1])/2)


for ijniF in range(len(judHeadU)):
    tempJudHeadU=judHeadU[ijniF]
    tempJudTailU=judTailU[ijniF]
    tempJudMidU=judgeMidU[ijniF]
    forPlotDisUIn=[]
    forPlotNO2UIn=[]
    for idfF in range(len(forPlotDisU)):
        if forPlotDisU[idfF]>=tempJudHeadU and forPlotDisU[idfF]<=tempJudTailU:
            forPlotDisUIn.append(forPlotDisU[idfF])
            forPlotNO2UIn.append(forPlotNO2U[idfF])
    tempNO2meanU=np.mean(forPlotNO2UIn)
    tempNO2stdU=np.std(forPlotNO2UIn)
    p2=plt.errorbar(tempJudMidU, tempNO2meanU, tempNO2stdU, fmt='ok', ecolor='black',lw=0.5, markersize=2.5)
    plt.hlines(tempNO2meanU+tempNO2stdU, tempJudHeadU, tempJudTailU,color="black",lw=0.5)
    plt.hlines(tempNO2meanU-tempNO2stdU, tempJudHeadU, tempJudTailU,color="black",lw=0.5)  

judHeadM=[]
judTailM=[]
judgeMidM=[]
for judM in range(len(intvalBoxM)-1):
    judHeadM.append(intvalBoxM[judM])
    judTailM.append(intvalBoxM[judM+1])
    judgeMidM.append((intvalBoxM[judM]+intvalBoxM[judM+1])/2)  
  
for ijniF1 in range(len(judHeadM)):
    tempJudHeadM=judHeadM[ijniF1]
    tempJudTailM=judTailM[ijniF1]
    tempJudMidM=judgeMidM[ijniF1]
    forPlotDisMIn=[]
    forPlotNO2MIn=[]
    for idfF1 in range(len(forPlotDisM)):
        if forPlotDisM[idfF1]>=tempJudHeadM and forPlotDisM[idfF1]<=tempJudTailM:
            forPlotDisMIn.append(forPlotDisM[idfF1])
            forPlotNO2MIn.append(forPlotNO2M[idfF1])
    tempNO2meanM=np.mean(forPlotNO2MIn)
    tempNO2stdM=np.std(forPlotNO2MIn)
    plt.errorbar(tempJudMidM, tempNO2meanM, tempNO2stdM, fmt='om', ecolor='magenta', lw=0.5,markersize=2.5)
    plt.hlines(tempNO2meanM+tempNO2stdM, tempJudHeadM, tempJudTailM,color="magenta",lw=0.5)
    plt.hlines(tempNO2meanM-tempNO2stdM, tempJudHeadM, tempJudTailM,color="magenta",lw=0.5)  
    

judHeadD=[]
judTailD=[]
judgeMidD=[]
for judD in range(len(intvalBoxD)-1):
    judHeadD.append(intvalBoxD[judD])
    judTailD.append(intvalBoxD[judD+1])
    judgeMidD.append((intvalBoxD[judD]+intvalBoxD[judD+1])/2)  
  
for ijniF2 in range(len(judHeadD)):
    tempJudHeadD=judHeadD[ijniF2]
    tempJudTailD=judTailD[ijniF2]
    tempJudMidD=judgeMidD[ijniF2]
    forPlotDisDIn=[]
    forPlotNO2DIn=[]
    for idfF2 in range(len(forPlotDisD)):
        if forPlotDisD[idfF2]>=tempJudHeadD and forPlotDisD[idfF2]<=tempJudTailD:
            forPlotDisDIn.append(forPlotDisD[idfF2])
            forPlotNO2DIn.append(forPlotNO2D[idfF2])
    tempNO2meanD=np.mean(forPlotNO2DIn)
    tempNO2stdD=np.std(forPlotNO2DIn)
    p1=plt.errorbar(tempJudMidD, tempNO2meanD, tempNO2stdD, fmt='og', ecolor='green',lw=0.5, markersize=2.5)
    plt.hlines(tempNO2meanD+tempNO2stdD, tempJudHeadD, tempJudTailD,color="green",lw=0.5)
    plt.hlines(tempNO2meanD-tempNO2stdD, tempJudHeadD, tempJudTailD,color="green",lw=0.5)  
       

def formatnumX(x, pos): #Scientific notation
    return '%.0f' % (x/1000)
formatter1 = FuncFormatter(formatnumX)#Scientific notation
ax.xaxis.set_major_formatter(formatter1)

ax.set_xlabel('R (km)',family='Helvetica',size=5)
ax.set_ylabel('$\hat{C}$ (μmol/m$^2$)',family='Helvetica',size=5)

ax.set_ylim(bottom=0)

gray_patch = mpatches.Patch(edgecolor=None, facecolor='silver',alpha=0.4,label='95% confidence interval')

legend_elements = [Line2D([0], [0], marker='o', linestyle='solid', label='P = 93,744.5 (mean of group S)',color='black',markersize=0,linewidth=0.5),
                 Line2D([0], [0], marker='o', linestyle='dashed', label='P = 341,002.5 (mean of group M)',color='black',markersize=0,linewidth=0.5),
                 Line2D([0], [0], marker='o', linestyle='dashdot', label='P = 4,312,730.1 (mean of group L)',color='black',markersize=0,linewidth=0.5),
                 Line2D([0], [0], marker='o', linestyle='solid', label='error bars of C (group S)',color='green',markersize=0,linewidth=0.5),
                 Line2D([0], [0], marker='o', linestyle='solid', label='error bars of C (group M)',color='magenta',markersize=0,linewidth=0.5),
                 Line2D([0], [0], marker='o', linestyle='solid', label='error bars of C (group L)',color='black',markersize=0,linewidth=0.5),
                 Line2D([0], [0], marker='o', linestyle='solid', label='average C in 5 km bands (group S)',color='green',markersize=2.5,linewidth=0),
                 Line2D([0], [0], marker='o', linestyle='solid', label='average C in 5 km bands (group M)',color='magenta',markersize=2.5,linewidth=0),
                 Line2D([0], [0], marker='o', linestyle='solid', label='average C in 5 km bands (group L)',color='black',markersize=2.5,linewidth=0),
                 gray_patch]

ax.legend(handles=legend_elements, loc='best',prop={'family':'Helvetica','size':5},frameon=False,borderpad=0.3)
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
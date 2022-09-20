# coding=utf-8
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import math
import statsmodels.api as sm
import scipy
from sympy import pretty_print as su
from scipy.stats import pearsonr
import tkinter
import matplotlib
matplotlib.use('TkAgg')
import collections
import dbf
from dbfread import DBF

mergedCellTable=dbf.Table('M:/Eclipse_Workspace/Article2_Kriging_Py/MeCel1000GauKri_SelectedCitiedDBF.dbf',codepage=0xf0)
mergedCellTable.open(dbf.READ_ONLY)
df1 = pd.DataFrame(mergedCellTable)
df1.columns =['OBJECTID', 'FID_extrac', 'pointid', 'grid_code', 'FID_FUA_ex', 'eFUA_ID', 'UC_num', 'UC_IDs', 'eFUA_name', 'Commuting', 'Cntry_ISO', 'Cntry_name', 'FUA_area', 'UC_area', 'FUA_p_2015', 'UC_p_2015', 'Com_p_2015', 'eFUAnameEN', 'eFUAnamENS', 'Count_', 'y', 'CBDX', 'CBDY', 'x', 'eFUA_IDS', 'centrodX', 'centrodY', 'CBDPoiRs1k', 'BUFF_DIST', 'ORIG_FID', 'Shape_Leng', 'Shape_Area', 'DisLevel', 'NO2Lev', 'PopRank', 'Log10Pop15']
df = df1.sort_values(by=['eFUA_ID'], ascending=True)#reorder df so smaller cities come up on top of scatterplot
b1=df.groupby('FUA_p_2015').agg({'eFUA_ID':['max'],'grid_code':['min']})
b1.columns = ['eFUA_ID','minFUA']
b = b1.sort_values(by=['eFUA_ID'], ascending=True)#reorder df so smaller cities come up on top of scatterplot
  
listMinValue=b['minFUA'].tolist()
listeFUAID=b['eFUA_ID'].tolist()

seekOrder=df['eFUA_ID'].tolist()
indexHead=[0]#the head index of a city
indexTail=[]#the end index of a city
   
for ih in range(len(seekOrder)-1):
    if seekOrder[ih]!=seekOrder[ih+1]:
        indexHead.append(ih+1)
        indexTail.append(ih)
indexTail.append(len(seekOrder)-1)
numberOfValues=np.array(indexTail)-np.array(indexHead)+1

minValueFinal=[]
for id in range(len(listMinValue)):
    minValueFinal=minValueFinal+[listMinValue[id]]*numberOfValues[id]#replicate the minimum value, no. of minimum value is equal to no. of cells of the city
  
 
df['minValue'] = minValueFinal#minimum no2 value of a city
extrGridValue=np.array(df['grid_code'].tolist())-np.array(minValueFinal)
df['extrGrid'] = extrGridValue#original no2 minus minimum no2 value

#df.to_csv('M:/MeCel1000GauKri_SelectedCitywMinFUA.csv',encoding='utf-8')#save to csv
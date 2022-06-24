import pandas as pd
import math
import scipy
from scipy.stats import pearsonr
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
import numpy as np

xls = pd.ExcelFile('M://maintextTable.xlsx')
df1 = pd.read_excel(xls,'meanNO2-pd')

popSize=df1.iloc[0:28,3].tolist()
meanNO2=df1.iloc[0:28,5].tolist()
area=df1.iloc[0:28,4].tolist()

areaArray=np.array(area)
popSizeArray=np.array(popSize)
denArray=popSizeArray/areaArray

popDen=denArray.tolist()

logpopDen=[]
for i in popDen:
    logpopDen.append(math.log(i,10))

logMeanNO2=[]
for j in meanNO2:
    logMeanNO2.append(math.log(j,10))
  
 
dataframe1={'LogMeanNO2':logMeanNO2,'logDen':logpopDen}
model1 = ols('LogMeanNO2 ~ logDen',dataframe1).fit()
anovat1 = anova_lm(model1)
print(anovat1)
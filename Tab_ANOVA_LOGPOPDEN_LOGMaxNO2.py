import pandas as pd
import math
import scipy
from scipy.stats import pearsonr
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
import numpy as np

xls = pd.ExcelFile('M://maintextTable.xlsx')
df1 = pd.read_excel(xls,'maxNO2-pd')

popSize=df1.iloc[0:5,3].tolist()
maxNO2=df1.iloc[0:5,5].tolist()
area=df1.iloc[0:5,4].tolist()

areaArray=np.array(area)
popSizeArray=np.array(popSize)
denArray=popSizeArray/areaArray

popDen=denArray.tolist()

logpopDen=[]
for i in popDen:
    logpopDen.append(math.log(i,10))

logMaxNO2=[]
for j in maxNO2:
    logMaxNO2.append(math.log(j,10))
  
 
dataframe1={'LogMaxNO2':logMaxNO2,'logDen':logpopDen}
model1 = ols('LogMaxNO2 ~ logDen',dataframe1).fit()
anovat1 = anova_lm(model1)
print(anovat1)
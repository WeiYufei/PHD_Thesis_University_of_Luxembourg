import pandas as pd
import math
import scipy
from scipy.stats import pearsonr
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols

xls = pd.ExcelFile('M://maintextTable.xlsx')
df1 = pd.read_excel(xls,'meanNO2-ps')

popSize=df1.iloc[0:42,3].tolist()
meanNO2=df1.iloc[0:42,4].tolist()

logPopSize=[]
for i in popSize:
    logPopSize.append(math.log(i,10))

logMeanNO2=[]
for j in meanNO2:
    logMeanNO2.append(math.log(j,10))
  
 
dataframe1={'LogMeanNO2':logMeanNO2,'logSize':logPopSize}
model1 = ols('LogMeanNO2 ~ logSize',dataframe1).fit()
anovat1 = anova_lm(model1)
print(anovat1)
import pandas as pd
import math
import scipy
from scipy.stats import pearsonr
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols

xls = pd.ExcelFile('M://maintextTable.xlsx')
df1 = pd.read_excel(xls,'maxNO2-ps')

popSize=df1.iloc[0:5,3].tolist()
maxNO2=df1.iloc[0:5,4].tolist()

logPopSize=[]
for i in popSize:
    logPopSize.append(math.log(i,10))

logMaxNO2=[]
for j in maxNO2:
    logMaxNO2.append(math.log(j,10))
  
 
dataframe1={'LogMaxNO2':logMaxNO2,'logSize':logPopSize}
model1 = ols('LogMaxNO2 ~ logSize',dataframe1).fit()
anovat1 = anova_lm(model1)
print(anovat1)
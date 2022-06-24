import pandas as pd
import math
import scipy
from scipy.stats import pearsonr
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols

xls = pd.ExcelFile('M://maintextTable.xlsx')
df1 = pd.read_excel(xls,'maxUHI-ps')

popSize=df1.iloc[0:57,3].tolist()
maxUHI=df1.iloc[0:57,4].tolist()


logPopSize=[]
for i in popSize:
    logPopSize.append(math.log(i,10))
    
logMaxUHI=[]
for j in maxUHI:
    logMaxUHI.append(math.log(j,10))
  
 
dataframe1={'LogmaxUHI':logMaxUHI,'logSize':logPopSize}
model1 = ols('LogmaxUHI ~ logSize',dataframe1).fit()
anovat1 = anova_lm(model1)
print(anovat1)
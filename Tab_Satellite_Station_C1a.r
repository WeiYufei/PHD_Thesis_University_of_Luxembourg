options(digits = 10)
library(lmtest)
library(margins)
library(openxlsx)
library(relaimpo)
library(sandwich)

data1 <- read.xlsx("M:/Eclipse_Workspace/Article1_Py_NRS/overlappedCellImproved.xlsx", sheet=1)

popSizeDr<-data1$FUA_p_2015
popSize151<-round(popSizeDr)
popSize15<-log(popSize151,base=10)

meanNO2cell1<-data1$grid_code
meanNO2cell<-log(meanNO2cell1,base=10)

meanNO2station1<-data1$AQValue
meanNO2station<-log(meanNO2station1,base=10)


###model
###################################################################
model1<-lm(meanNO2cell~meanNO2station)
summary(model1)
anova(model1)


####
manualR<-1-deviance(model1)/sum(anova(model1)[,2])
manualR

coeftest(model1, vcov = vcovHC(model1, type = "HC0"))

############################################################################

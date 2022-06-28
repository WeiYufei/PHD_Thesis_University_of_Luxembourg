options(digits = 10)
library(lmtest)
library(openxlsx)
library(sandwich)

data1 <- read.xlsx("M:/Eclipse_Workspace/Article1_NC_R/Regression_OverlappedCell_w_Station.xlsx", sheet=1)
popSize<-data1$Pop2015
meanNO2cell<-data1$grid_code
meanNO2station<-data1$AQValue


model1<-lm(meanNO2cell~meanNO2station)
summary(model1)
manualR<-1-deviance(model1)/sum(anova(model1)[,2])
manualR

coeftest(model1, vcov = vcovHC(model1, type = "HC1"))
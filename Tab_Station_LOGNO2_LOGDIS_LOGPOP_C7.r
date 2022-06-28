options(digits = 10)
library(lmtest)
library(openxlsx)
library(relaimpo)
library(sandwich)

data1 <- read.xlsx("M://Regression_Station.xlsx", sheet=1)

popSize15<-data1$FUA_p_2015
meanNO2<-data1$AQValue
distance<-data1$DisStaCen
eFUAName<-data1$eFUAnameEN
CountryN<-data1$Cntry_name
cate<-data1$StationTyp
cateFac<-as.factor(cate)

logMeanNO2<-log(meanNO2,base=10)
logPopSize<-log(popSize15,base=10)
logDis<-log(distance,base=10)

model1<-lm(logMeanNO2~logDis+logPopSize)
summary(model1)
calc.relimp(model1,rela=TRUE)

manualR<-1-deviance(model1)/sum(anova(model1)[,2])
manualR

coeftest(model1, vcov = vcovHC(model1, type = "HC1"))

##Stat_nonDuplicatedNumber
NoFUA<-unique(eFUAName)
NoCountryN<-unique(CountryN)
print(length(NoFUA))
print(length(NoCountryN))
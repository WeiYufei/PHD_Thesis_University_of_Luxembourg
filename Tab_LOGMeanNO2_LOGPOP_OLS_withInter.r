options(digits=10)
library(xlsx)
library(lmtest)
library(openxlsx)
data1 <- read.xlsx("M://maintextTable.xlsx", sheet=2)

meanNO2<-data1$MeanNO2
popSize<-data1$Population

logPopSize<-log(popSize,base=10)
logmeanNO2<-log(meanNO2,base=10)


model1<-lm(logmeanNO2~logPopSize)	

summary(model1)
manualR<-1-deviance(model1)/sum(anova(model1)[,2])
manualR


bptest(model1)

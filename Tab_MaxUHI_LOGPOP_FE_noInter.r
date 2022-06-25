options(digits=10)
library(xlsx)
library(lmtest)
library(openxlsx)
data1 <- read.xlsx("M://maintextTable.xlsx", sheet=1)

maxUHI<-data1$MaxUHI
popSize<-data1$Population
cate<-data1$SourceType

logPopSize<-log(popSize,base=10)


cateFac<-as.factor(cate)
model1<-lm(maxUHI~0+logPopSize+cateFac)


summary(model1)

waldtest(model1)

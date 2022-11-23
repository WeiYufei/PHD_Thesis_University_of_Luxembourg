options(digits = 10)
library(openxlsx)

data1 <- read.xlsx("M://Regression_Station.xlsx", sheet=1)

popSizeStat<-data1$FUA_p_2015
areaStat<-data1$FUA_area
NO2Station<-data1$AQValue
distCenterSation<-data1$DisStaCen

std <- function(x) sd(x)/sqrt(length(x))

print ("Column-Population")

round(min(unique(popSizeStat)),1)
round(max(unique(popSizeStat)),1)
round(mean(unique(popSizeStat)),1)
round(sd(unique(popSizeStat)),1)
round(std(unique(popSizeStat)),1)


print("Column-Annual mean NO2 station")

round(min(NO2Station),1)
round(max(NO2Station),1)
round(mean(NO2Station),1)
round(sd(NO2Station),1)
round(std(NO2Station),1)

print("Column-Dist station")

round(min(distCenterSation),1)
round(max(distCenterSation),1)
round(mean(distCenterSation),1)
round(sd(distCenterSation),1)
round(std(distCenterSation),1)

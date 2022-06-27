options(digits = 10)
library(openxlsx)


data1 <- read.xlsx("M://Regression_Cell.xlsx", sheet=1)

popSizeStat<-data1$FUA_p_2015
areaStat<-data1$FUA_area
NO2Cell<-data1$grid_code
distCenterCell<-data1$DisCelCen

std <- function(x) sd(x)/sqrt(length(x))

print("Column-Annual mean NO2 satellite")

round(min(NO2Cell),1)
round(max(NO2Cell),1)
round(mean(NO2Cell),1)
round(sd(NO2Cell),1)
round(std(NO2Cell),1)

print("Column-Dist satellite")

round(min(distCenterCell),1)
round(max(distCenterCell),1)
round(mean(distCenterCell),1)
round(sd(distCenterCell),1)
round(std(distCenterCell),1)


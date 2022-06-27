options(digits = 10)
library(openxlsx)


data1 <- read.xlsx("M://Regression_Cell_w_MinValue_equalCellDeleted.xlsx", sheet=1)

popSizeStat<-data1$FUA_p_2015
areaStat<-data1$FUA_area
NO2Cell<-data1$grid_code
distCenterCell<-data1$DisCelCen
NO2MinCell<-data1$minFuaFul

std <- function(x) sd(x)/sqrt(length(x))

print("Column-Minimum annual mean NO2 satellite per FUA")

round(min(NO2MinCell),1)
round(max(NO2MinCell),1)
round(mean(NO2MinCell),1)
round(sd(NO2MinCell),1)
round(std(NO2MinCell),1)



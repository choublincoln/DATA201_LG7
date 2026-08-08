library(tidyverse)
data1 <- read_csv("data/listings_october.csv")

ggplot(aes(x = longitude, y = price), data = data1) + geom_point() + theme_bw()
min(data1$price,na.rm=TRUE)
max(data1$price,na.rm=TRUE)
sd(data1$price,na.rm=TRUE)
nrow(data1)
data1|>
  count(host_name)

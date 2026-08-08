library(tidyverse)
data1 <- read_csv("data/listings_october.csv")

ggplot(aes(x = longitude, y = price), data = data1) + geom_point() + theme_bw()


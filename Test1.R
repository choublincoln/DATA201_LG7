library(tidyverse)
# chosen data-set we're focused on 
data_october <- read_csv("data/listings_october.csv") |>
  filter(neighbourhood_group == "Christchurch City") |> # filters for Christchurch City.
  mutate(month = "October", year = 2025) # creates new columns with their assigned values.


data_november <- read_csv("data/listings_november.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "November", year = 2025)











# Pallima stuff 
min(data1$price,na.rm=TRUE)
max(data1$price,na.rm=TRUE)
sd(data1$price,na.rm=TRUE)
nrow(data1)
data1|>
  count(host_name)


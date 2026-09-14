"what to do here: Basically run all this code you only want to do this ONCE ONLY!!"
"The output data we get will go into the Data3 Folder that you should have created"

library(tidyverse)
listings_oct_to_june <- read_csv("data/listings_oct_to_june.csv") # MUST RUN
bonds <- read_csv("data2/bonds.csv")

#___________________________________________________________________________________________________
"Airbnb Cleaning"
Airbnb_listings_cleaned <- listings_oct_to_june |>
  mutate(id = as.character(id)) |> # converting id to character
  select(id, neighbourhood, latitude, longitude, room_type, price, availability_365,
         month, year) # column drops

write.csv(Airbnb_listings_cleaned, "data3/Airbnb_listings_cleaned.csv", row.names = FALSE)
#___________________________________________________________________________________________________
"Bonds Cleaning"





#___________________________________________________________________________________________________


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
         month, year) # Selecting only these columns for the analyses, drops others

write.csv(Airbnb_listings_cleaned, "data3/Airbnb_listings_cleaned.csv", row.names = FALSE)
#___________________________________________________________________________________________________
"Bonds Cleaning"
mean(bonds$`Location Id` == "NULL") * 100 # Calculates the percentage of Missing Location Id's in the Bonds data set
mean(bonds$`Location Id` == "-99") * 100 # Calculates the percentage of Location Id's = -99



#___________________________________________________________________________________________________
"Filtering Timeframe"

# Filter to match Christchurch listings:
# October 2025 to June 2026
bonds_filtered <- bonds %>%
  filter(
    TimeFrame >= as.Date("2025-10-01"),
    TimeFrame <= as.Date("2026-06-30")
  )

sort(unique(bonds_filtered$TimeFrame))









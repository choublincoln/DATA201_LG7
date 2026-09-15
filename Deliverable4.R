"what to do here: Basically run all this code you only want to do this ONCE ONLY!!"
"The output data we get will go into the Data3 Folder that you should have created"

library(tidyverse)
listings_oct_to_june <- read_csv("data/listings_oct_to_june.csv") # MUST RUN

#___________________________________________________________________________________________________

"place functions in here :)"

#___________________________________________________________________________________________________

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


drop_column <- function(csvfile, col_name) {"Drops unnecessary columns."
  drop_file <- csvfile |>
    select(-all_of(col_name))
  drop_file
  }


drop_row <- function(csvfile, col_name) {"Drops problematic rows. Not sure if this is necessary."
  new_data |>
    filter(!is.na(.csvfile[[col_name]]))
  new_data
  }


na_rent <- function(csvfile) {"Drops listings that probably have not been rented."
  
  }
#___________________________________________________________________________________________________




#___________________________________________________________________________________________________



#___________________________________________________________________________________________________



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




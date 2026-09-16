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
         month, year, minimum_nights) # Selecting only these columns for the analyses, drops others

write.csv(Airbnb_listings_cleaned, "data3/Airbnb_listings_cleaned.csv", row.names = FALSE)


#___________________________________________________________________________________________________
"Filtering Timeframe"

# Filter to match Christchurch listings:
# October 2025 to June 2026

bonds$TimeFrame <- as.Date(bonds$TimeFrame, format = "%d/%m/%Y")

bonds_filtered <- bonds %>%
  filter(
    TimeFrame >= as.Date("2025-10-01"),
    TimeFrame <= as.Date("2026-06-30")
  )

# The above code was broken. I fixed it (Daniel)

sort(unique(bonds_filtered$TimeFrame))
#___________________________________________________________________________________________________

"Bonds Cleaning"
null_per <- mean(bonds_filtered$`Location Id` == "NULL") * 100 # Calculates the percentage of Missing Location Id's in the Bonds data set
aggregate_per <- mean(bonds_filtered$`Location Id` == "-99") * 100 # Calculates the percentage of Location Id's = -99

count_na <- bonds_filtered |> 
  count(`Location Id` == "NULL")
count_agg <- bonds_filtered |> 
  count(`Location Id` == "-99")

drop_column <- function(data, col_name) {#Drops unnecessary columns.
  drop_file <- data |>
    select(-all_of(col_name))
  drop_file
  }


drop_row <- function(data, col_name, value) {#Drops problematic rows.
  data %>%
    filter(
      !is.na(.data[[col_name]]),
      .data[[col_name]] != value
    )
  }


tenancy_data <- function(data) { # Cleans tenancy report data

  na_row_drop <- drop_row(data, "Location Id", "NULL")
  all_row_drop <- drop_row(na_row_drop, "Location Id", "-99")
  
  all_row_drop <- all_row_drop |>
    mutate(
      `Median Rent` = as.integer(`Median Rent`),
      `Geometric Mean Rent` = as.integer(`Geometric Mean Rent`),
      `Upper Quartile Rent` = as.integer(`Upper Quartile Rent`),
      `Lower Quartile Rent` = as.integer(`Lower Quartile Rent`)
    )
  
  write.csv(all_row_drop, "data3/tenancy_cleaned.csv", row.names = FALSE)
  print("New csv file created.")
  
  all_row_drop
}

tenancy_data(bonds_filtered)

cat("Percentage of null values in Location ID:", null_per, "%\n")
cat("Percentage of -99 values in Location ID:", aggregate_per, "%\n")
#___________________________________________________________________________________________________






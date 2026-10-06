# =========================================================
# IMPORT DATA
# =========================================================

library(tidyverse)

listings_oct_to_august <- readRDS(
  "output_data/listings_oct_to_august.rds"
) # MUST RUN

listings_oct_to_august$id <- as.character(listings_oct_to_august$id)

bonds <- read_csv("input_data/bonds.csv")


# =========================================================
# FUNCTIONS (Daniels)
# =========================================================

drop_column <- function(data, col_name) {
  # Drops inputted columns.
  drop_file <- data |>
    select(-all_of(col_name))
  drop_file
}

drop_row <- function(data, col_name, value) {
  # Drops inputted rows.
  data %>%
    filter(
      !is.na(.data[[col_name]]),
      .data[[col_name]] != value
    )
}

tenancy_data <- function(data) {
  # Cleans Tenancy Services data and saves to file.
  na_row_drop <- drop_row(data, "Location Id", "NULL")
  all_row_drop <- drop_row(na_row_drop, "Location Id", "-99")
  
  all_row_drop <- all_row_drop |>
    mutate(
      `Median Rent` = as.integer(`Median Rent`),
      `Geometric Mean Rent` = as.integer(`Geometric Mean Rent`),
      `Upper Quartile Rent` = as.integer(`Upper Quartile Rent`),
      `Lower Quartile Rent` = as.integer(`Lower Quartile Rent`)
    )
  
  saveRDS(
    all_row_drop,
    "output_data/tenancy_cleaned.rds"
  )
  
  print("New csv file created.")
  
  view(all_row_drop)
}
# =========================================================
# AIRBNB CLEANING (Lincolns)
# =========================================================

Airbnb_listings_cleaned <- listings_oct_to_august |>
  mutate(id = as.character(id)) |>
  select(
    id,
    neighbourhood,
    latitude,
    longitude,
    room_type,
    price,
    availability_365,
    month,
    year,
    minimum_nights
  )


# =========================================================
# TIMEFRAME FILTERING (Eans)
# =========================================================

bonds$TimeFrame <- as.Date(
  bonds$TimeFrame,
  format = "%d/%m/%Y"
)

bonds_filtered <- bonds %>%
  filter(
    TimeFrame >= as.Date("2025-10-01"),
    TimeFrame <= as.Date("2026-06-30")
  )

sort(unique(bonds_filtered$TimeFrame))


# =========================================================
# BONDS DATA EXPLORATION (Daniels)
# =========================================================

percentage_na_values <- mean(
  bonds_filtered$`Location Id` == "NULL"
) * 100

percentage_agg_values <- mean(
  bonds_filtered$`Location Id` == "-99"
) * 100

count_na_values <- bonds_filtered |> 
  count(`Location Id` == "NULL")

count_agg_values <- bonds_filtered |> 
  count(`Location Id` == "-99")

# Print Results:

cat(
  "Percentage of null values in Location ID:",
  percentage_na_values,
  "%\n"
)

cat(
  "Percentage of -99 values in Location ID:",
  percentage_agg_values,
  "%\n"
)


# =========================================================
# BONDS DATA CLEANING (Daniels)
# =========================================================

tenancy_data(bonds_filtered)


# =========================================================
# SAVE CLEANED DATA (Lincolns)
# =========================================================

# Validating
view(Airbnb_listings_cleaned)


saveRDS(Airbnb_listings_cleaned, "output_data/Airbnb_listings_cleaned.rds")
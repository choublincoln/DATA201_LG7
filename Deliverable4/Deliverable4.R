# =========================================================
# IMPORT DATA
# =========================================================

library(tidyverse)

listings_oct_to_june <- read_csv(
  "Deliverable4/input_data/listings_oct_to_june.csv",
  col_types = cols(id = col_character())
) # MUST RUN

bonds <- read_csv("Deliverable4/input_data/bonds.csv")


# =========================================================
# FUNCTIONS (Daniels)
# =========================================================

drop_column <- function(data, col_name) {
  drop_file <- data |>
    select(-all_of(col_name))
  drop_file
}

drop_row <- function(data, col_name, value) {
  data %>%
    filter(
      !is.na(.data[[col_name]]),
      .data[[col_name]] != value
    )
}

tenancy_data <- function(data) {
  na_row_drop <- drop_row(data, "Location Id", "NULL")
  all_row_drop <- drop_row(na_row_drop, "Location Id", "-99")
  
  all_row_drop <- all_row_drop |>
    mutate(
      `Median Rent` = as.integer(`Median Rent`),
      `Geometric Mean Rent` = as.integer(`Geometric Mean Rent`),
      `Upper Quartile Rent` = as.integer(`Upper Quartile Rent`),
      `Lower Quartile Rent` = as.integer(`Lower Quartile Rent`)
    )
  
  write.csv(
    all_row_drop,
    "Deliverable4/output_data/tenancy_cleaned.csv",
    row.names = FALSE
  )
  
  print("New csv file created.")
  
  all_row_drop
}


# =========================================================
# AIRBNB CLEANING (Lincolns)
# =========================================================

Airbnb_listings_cleaned <- listings_oct_to_june |>
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

null_per <- mean(
  bonds_filtered$`Location Id` == "NULL"
) * 100

aggregate_per <- mean(
  bonds_filtered$`Location Id` == "-99"
) * 100

count_na <- bonds_filtered |> 
  count(`Location Id` == "NULL")

count_agg <- bonds_filtered |> 
  count(`Location Id` == "-99")

cat(
  "Percentage of null values in Location ID:",
  null_per,
  "%\n"
)

cat(
  "Percentage of -99 values in Location ID:",
  aggregate_per,
  "%\n"
)


# =========================================================
# BONDS DATA CLEANING (Daniels)
# =========================================================

tenancy_data(bonds_filtered)


# =========================================================
# SAVE CLEANED DATA (Lincolns)
# =========================================================

write.csv(
  Airbnb_listings_cleaned,
  "Deliverable4/output_data/Airbnb_listings_cleaned.csv",
  row.names = FALSE
)
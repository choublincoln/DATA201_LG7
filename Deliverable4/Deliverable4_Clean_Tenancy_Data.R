library(tidyverse)

bonds <- read_csv("input_data/bonds.csv")


# =========================================================
# Functions
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
    filter(!is.na(.data[[col_name]]), .data[[col_name]] != value)
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
      `Lower Quartile Rent` = as.integer(`Lower Quartile Rent`))
  
  all_row_drop
}

# =========================================================
# TIMEFRAME FILTERING 
# =========================================================

bonds$TimeFrame <- as.Date(bonds$TimeFrame,format = "%d/%m/%Y")

bonds_filtered <- bonds %>%
  filter(TimeFrame >= as.Date("2025-10-01"),
         TimeFrame <= as.Date("2026-06-30"))

sort(unique(bonds_filtered$TimeFrame))


# =========================================================
# BONDS DATA EXPLORATION 
# =========================================================

percentage_na_values <- mean(bonds_filtered$`Location Id` == "NULL") * 100

percentage_agg_values <- mean(bonds_filtered$`Location Id` == "-99") * 100

count_na_values <- bonds_filtered |> 
  count(`Location Id` == "NULL")

count_agg_values <- bonds_filtered |> 
  count(`Location Id` == "-99")

# Print Results:
cat("Percentage of null values in Location ID:", percentage_na_values, "%\n")
cat("Percentage of -99 values in Location ID:", percentage_agg_values, "%\n")


# =========================================================
# BONDS DATA CLEANING 
# =========================================================

clean_tenancy <- tenancy_data(bonds_filtered)

#Download
write_csv(clean_tenancy, "output_data/Deliverable4_output/tenancy_cleaned.csv")
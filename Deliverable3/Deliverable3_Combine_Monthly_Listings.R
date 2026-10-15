
# =========================================================
# COMBINED AIRBNB DATASET PIPELINE
# =========================================================

library(tidyverse)
library(lubridate)

# =========================================================
# 1. DISCOVER INPUT FILES
# =========================================================

# Find all monthly Airbnb CSV files
input_files <- list.files(path = "input_data", pattern = "^listings_.*\\.csv$", full.names = TRUE)

# Stop if no matching files are found
if (length(input_files) == 0) {
  stop("No monthly Airbnb CSV files found in input_data/.")
}

# =========================================================
# 2. IMPORT AND COMBINE DATA
# =========================================================

combined_listings <- map_dfr(input_files, function(file_path) {
  
  # Extract the month and year from the filename
  file_name <- basename(file_path)
  month_year <- str_remove(file_name, "^listings_")
  month_year <- str_remove(month_year, "\\.csv$")
  
  # Convert the month and year into a date
  snapshot_date <- parse_date_time(month_year, orders = "B_Y", quiet = TRUE)
  
  # Stop if the filename does not contain a valid month and year
  if (is.na(snapshot_date)) {
    stop(paste("Could not determine month and year from filename:",
               file_name,
               "- use a format such as listings_october_2025.csv"))
  }
  
  # Read the monthly dataset
  monthly_listings <- read_csv(file_path, show_col_types = FALSE)
  
  # Filter Christchurch City listings and add month/year
  monthly_listings |>
    filter(neighbourhood_group == "Christchurch City") |>
    mutate(month = month.name[month(snapshot_date)], year = year(snapshot_date))
})

combined_listings <- combined_listings |>
  mutate(month = factor(month, levels = month.name, ordered = TRUE)) |>
  arrange(year, month) |>
  mutate(month = as.character(month))

# =========================================================
# 3. PUBLISH
# =========================================================

# Save the combined dataset
write_csv(combined_listings, "output_data/Deliverable3_output/combined_listings.csv")

# =========================================================
# IMPORT DATA
# =========================================================

library(tidyverse)

airbnb_data <- read_csv("output_data/Deliverable3_output/combined_listings.csv")
airbnb_data$id <- as.character(airbnb_data$id) # makes sure id is treated as text

# =========================================================
# AIRBNB CLEANING 
# =========================================================

airbnb_listings_cleaned <- airbnb_data |>
  mutate(id = as.character(id)) |>
  select(id, neighbourhood, latitude, longitude, room_type, price,
         availability_365, month, year, minimum_nights)

# =========================================================
# SAVE CLEANED DATA 
# =========================================================


write_csv(airbnb_listings_cleaned, "output_data/Deliverable4_output/Airbnb_listings_cleaned.csv")
# =========================================================
# IMPORT DATA
# =========================================================

library(tidyverse)

listings_oct_to_august <- readRDS(
  "output_data/listings_oct_to_august.rds"
) # MUST RUN

listings_oct_to_august$id <- as.character(listings_oct_to_august$id)

# =========================================================
# AIRBNB CLEANING (Lincolns)
# =========================================================

airbnb_listings_cleaned <- listings_oct_to_august |>
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
# SAVE CLEANED DATA (Lincolns)
# =========================================================

# Validating
view(airbnb_listings_cleaned)


saveRDS(airbnb_listings_cleaned, "output_data/Airbnb_listings_cleaned.rds")
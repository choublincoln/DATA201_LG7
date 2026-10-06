# =========================================================
# 1. IMPORT AND COMBINE DATA
# =========================================================

library(tidyverse)

# Import each monthly dataset, keep Christchurch City listings,
# and add the corresponding month and year.

data_october <- read_csv("input_data/listings_october.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "October", year = 2025)

data_november <- read_csv("input_data/listings_november.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "November", year = 2025)

data_december <- read_csv("input_data/listings_december.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "December", year = 2025)

data_january <- read_csv("input_data/listings_january.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "January", year = 2026)

data_february <- read_csv("input_data/listings_february.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "February", year = 2026)

data_march <- read_csv("input_data/listings_march.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "March", year = 2026)

data_april <- read_csv("input_data/listings_april.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "April", year = 2026)

data_may <- read_csv("input_data/listings_may.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "May", year = 2026)

data_june <- read_csv("input_data/listings_june.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "June", year = 2026)

data_july <- read_csv("input_data/listings_july.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "July", year = 2026)

data_august <- read_csv("input_data/listings_august.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "August", year = 2026)

# Combine all monthly Christchurch listings into one dataset.

listings_oct_to_august <- bind_rows(
  data_october,
  data_november,
  data_december,
  data_january,
  data_february,
  data_march,
  data_april,
  data_may,
  data_june,
  data_july,
  data_august
)


# Save the combined dataset.
# The input copy allows the pipeline to use the combined data later.


saveRDS(listings_oct_to_august, file = "output_data/listings_oct_to_august.rds")
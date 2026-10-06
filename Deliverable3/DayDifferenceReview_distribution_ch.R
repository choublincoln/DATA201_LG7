# =========================================================
# EAN'S DATA WRANGLING PIPELINE
# =========================================================

library(tidyverse)

# =========================================================
# DISCOVER
# =========================================================

# Check the data type of last_review
class(listings_oct_to_june$last_review)


# =========================================================
# STRUCTURE
# =========================================================

# No Structure code contributed by Ean.


# =========================================================
# CLEAN
# =========================================================

# Remove listings with missing last_review values
listings_Ean_filtered <- listings_oct_to_june |>
  drop_na(last_review)


# =========================================================
# ENRICH
# =========================================================

# Add a date for each monthly dataset and calculate the
# number of days between the dataset date and last review date
listings_Ean_filtered <- listings_Ean_filtered |>
  mutate(
    dataset_date = case_when(
      month == "October" ~ as.Date("2025-10-30"),
      month == "November" ~ as.Date("2025-11-30"),
      month == "December" ~ as.Date("2025-12-30"),
      month == "January" ~ as.Date("2026-01-30"),
      month == "February" ~ as.Date("2026-02-28"),
      month == "March" ~ as.Date("2026-03-30"),
      month == "April" ~ as.Date("2026-04-30"),
      month == "May" ~ as.Date("2026-05-30"),
      month == "June" ~ as.Date("2026-06-30")
    ),
    day_difference_review = as.numeric(
      dataset_date - last_review
    )
  )


# =========================================================
# PUBLISH
# =========================================================

# Plot the distribution of the number of days between
# the dataset date and the last review
ggplot(
  listings_Ean_filtered,
  aes(
    x = cut(
      day_difference_review,
      breaks = c(0, 50, 100, 200, 500, 1000, Inf),
      labels = c(
        "0–50",
        "51–100",
        "101–200",
        "201–500",
        "501–1000",
        "1000+"
      )
    )
  )
) +
  geom_bar() +
  labs(
    title = "Day Difference on Last Review Distribution of Christchurch",
    x = "Days Since Last Review",
    y = "Number of Listings"
  ) +
  theme_bw()
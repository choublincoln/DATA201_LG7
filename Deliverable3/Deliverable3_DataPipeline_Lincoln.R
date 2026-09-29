# =========================================================
# LINCOLN'S DATA WRANGLING PIPELINE
# =========================================================

library(tidyverse)


# =========================================================
# DISCOVER
# =========================================================

# No Discover code contributed by Lincoln.


# =========================================================
# STRUCTURE
# =========================================================

# Load the combined Airbnb dataset.

listings_oct_to_june <- read_csv(
  "Deliverable3/input_data/listings_oct_to_june.csv"
)


# Remove columns that are not required for the analysis.

listings_oct_to_june <- listings_oct_to_june |>
  select(
    -host_id,
    -host_name,
    -room_type,
    -minimum_nights,
    -calculated_host_listings_count,
    -availability_365,
    -license
  )


# =========================================================
# CLEAN
# =========================================================

# Remove listings with missing price values.

listings_Lincoln_filtered <- listings_oct_to_june |>
  drop_na(price)


# =========================================================
# ENRICH
# =========================================================

# No enrichment is required for Lincoln's section.


# =========================================================
# PUBLISH
# =========================================================

# Create a bar chart showing the distribution of
# Christchurch Airbnb listing prices.

ggplot(
  listings_Lincoln_filtered,
  aes(
    x = cut(
      price,
      breaks = c(
        0,
        50,
        100,
        200,
        500,
        1000,
        Inf
      ),
      labels = c(
        "$0–$50",
        "$51–$100",
        "$101–$200",
        "$201–$500",
        "$501–$1000",
        "$1000+"
      )
    )
  )
) +
  geom_bar() +
  labs(
    title = "Price Distribution of Christchurch",
    x = "Price ($NZD)",
    y = "Number of Listings"
  ) +
  theme_bw()

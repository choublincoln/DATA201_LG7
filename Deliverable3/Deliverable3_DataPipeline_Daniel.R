
# =========================================================
# DANIEL'S DATA WRANGLING PIPELINE
# =========================================================

library(tidyverse)
combined_listings <- read.csv("output_data/Deliverable3_output/combined_listings.csv")

# =========================================================
# DISCOVER
# =========================================================

# No Discover code contributed by Daniel.


# =========================================================
# STRUCTURE
# =========================================================

# Drops unnecessary columns from the dataset
column_filter <- function(csvfile) {
  drop_file <- csvfile |>
    select(-host_id, -host_name, -room_type, -minimum_nights, -calculated_host_listings_count,
      -availability_365, -license)
  drop_file
}


# Selects each unique property using its highest number of reviews
select_top <- function(data) {
  
  top_properties <- data |>
    select(id, name, number_of_reviews) |>
    group_by(id) |>
    slice_max(order_by = number_of_reviews, n = 1, with_ties = FALSE, na_rm = TRUE) |>
    ungroup() |>
    arrange(desc(number_of_reviews))
  
  top_properties
}


# =========================================================
# CLEAN
# =========================================================

# No Clean code contributed by Daniel.


# =========================================================
# ENRICH
# =========================================================

# No Enrich code contributed by Daniel.


# =========================================================
# PUBLISH
# =========================================================

# Selects unique properties with their highest number of reviews
write_top <- function(data) {
  
  filtered_data <- column_filter(data)
  top_reviews <- select_top(filtered_data)
  
  top_reviews
}


# Select the properties with the highest number of reviews per ID
highest_reviews <- write_top(combined_listings)

# Validation
view(highest_reviews)

# Save the results
write_csv(highest_reviews, "output_data/Deliverable3_output/highest_reviews.csv")

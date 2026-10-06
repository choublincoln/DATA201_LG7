# =========================================================
# DANIEL'S DATA WRANGLING PIPELINE
# =========================================================

library(tidyverse)

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
    select(
      -host_id,
      -host_name,
      -room_type,
      -minimum_nights,
      -calculated_host_listings_count,
      -availability_365,
      -license
    )
  
  drop_file
}


# Selects the properties with the highest number of reviews
# (top 10% of listings)
select_top <- function(data) {
  
  num_reviews <- data |>
    select(id, name, number_of_reviews)
  
  num_rows <- nrow(data)
  percent_rows <- ceiling(num_rows * 0.1)
  
  top_properties <- num_reviews |>
    arrange(desc(number_of_reviews)) |>
    slice_head(n = percent_rows)
  
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

# Selects the properties with the highest number of reviews
write_top <- function(data) {
  
  filtered_data <- column_filter(data)
  top_reviews <- select_top(filtered_data)
  
  top_reviews
}


# Read the June/August dataset
august_data <- read_csv("input_data/listings_august.csv")

# Select the properties with the highest number of reviews
highest_reviews <- write_top(august_data)

# Validation
view(highest_reviews)

# Save the results
saveRDS(highest_reviews, file = "output_data/highest_reviews.rds")
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
  percent_rows <- num_rows * 0.1
  
  row_sort <- num_reviews[order(-num_reviews$number_of_reviews), ]
  
  top_properties <- row_sort[1:percent_rows, ]
  
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

# Writes the properties with the highest number of reviews
# to a CSV file
write_top <- function(data) {
  filtered_data <- column_filter(data)
  
  top_reviews <- select_top(filtered_data)
  
  write.csv(
    top_reviews,
    "Deliverable3/output_data/top_reviews.csv",
    row.names = FALSE
  )
  
  top_reviews
}

# Run the function using the June dataset
write_top(data_june)
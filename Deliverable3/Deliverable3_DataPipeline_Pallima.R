
# =========================================================
# PALLIMA'S DATA WRANGLING PIPELINE
# =========================================================

library(tidyverse)

# =========================================================
# DISCOVER
# =========================================================

# Load the combined Christchurch Airbnb dataset
combined_listings <- read_csv("output_data/Deliverable3_output/combined_listings.csv")
airbnb_data <- combined_listings


# ---------------------------------------------------------
# Summary statistics for all columns
# ---------------------------------------------------------

summary_statistics <- map_dfr(names(airbnb_data), function(column_name) {
  
  column_values <- airbnb_data[[column_name]]
  missing_count <- sum(is.na(column_values))
  unique_count <- n_distinct(column_values, na.rm = TRUE)
  
  if (is.numeric(column_values) &&
      !(column_name %in% c("id", "host_id", "year"))) {
    
    valid_values <- column_values[!is.na(column_values)]
    
    tibble(variable = column_name, type = "numeric", total_rows = length(column_values),
      missing = missing_count,
      missing_percent = round(missing_count / length(column_values) * 100, 2),
      unique_values = unique_count,
      minimum = if(length(valid_values) == 0) NA_real_ else min(valid_values),
      maximum = if(length(valid_values) == 0) NA_real_ else max(valid_values),
      mean = if(length(valid_values) == 0) NA_real_ else mean(valid_values),
      std_dev = if(length(valid_values) <= 1) NA_real_ else sd(valid_values),
      most_common = NA_character_,
      most_common_count = NA_integer_
    )
    
  } else {
    
    character_values <- as.character(column_values)
    character_values <- character_values[
      !is.na(character_values) & character_values != ""
    ]
    
    value_frequencies <- sort(table(character_values), decreasing = TRUE)
    most_common_value <- if(length(value_frequencies) == 0) {
      NA_character_
    } else {
      names(value_frequencies)[1]
    }
    
    most_common_frequency <- if(length(value_frequencies) == 0) {
      NA_integer_
    } else {
      as.integer(value_frequencies[1])
    }
    
    tibble(variable = column_name, type = ifelse(column_name %in% c("id", "host_id"),
        "identifier",
        "categorical/text"),
      total_rows = length(column_values),
      missing = missing_count,
      missing_percent = round(
        missing_count / length(column_values) * 100, 2
      ),
      unique_values = unique_count,
      minimum = NA_real_,
      maximum = NA_real_,
      mean = NA_real_,
      std_dev = NA_real_,
      most_common = most_common_value,
      most_common_count = most_common_frequency
    )
  }
})


# ---------------------------------------------------------
# Category counts
# ---------------------------------------------------------

category_counts <- airbnb_data |>
  select(neighbourhood_group, neighbourhood, room_type, month, year) |>
  mutate(across(everything(), as.character)) |>
  pivot_longer(cols = everything(), names_to = "variable", values_to = "category") |>
  mutate(category = replace_na(category, "<MISSING>")) |>
  count(variable, category, name = "count") |>
  arrange(variable, desc(count))


# ---------------------------------------------------------
# Last review date summary
# ---------------------------------------------------------

last_review_dates <- as.Date(airbnb_data$last_review)

review_date_summary <- tibble(variable = "last_review", 
                              earliest_date = min(last_review_dates, na.rm = TRUE),
                              latest_date = max(last_review_dates, na.rm = TRUE),
                              missing = sum(is.na(last_review_dates)))


# =========================================================
# STRUCTURE
# =========================================================

# No Structure code contributed by Pallima.


# =========================================================
# CLEAN
# =========================================================

# No Clean code contributed by Pallima.


# =========================================================
# ENRICH
# =========================================================

# No Enrich code contributed by Pallima.


# =========================================================
# PUBLISH
# =========================================================

# Validate and view the results
View(summary_statistics)
View(category_counts)
View(review_date_summary)

# Save the summary statistics
write_csv(summary_statistics, "output_data/Deliverable3_output/summary_statistics.csv")

write_csv(category_counts, "output_data/Deliverable3_output/category_counts.csv")

write_csv(review_date_summary, "output_data/Deliverable3_output/date_summary.csv")

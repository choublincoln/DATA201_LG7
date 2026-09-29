# =========================================================
# PALLIMA'S DATA WRANGLING PIPELINE
# =========================================================

library(tidyverse)

# =========================================================
# DISCOVER
# =========================================================

# Load the combined Christchurch Airbnb dataset
listings_oct_to_june <- read_csv(
  "Deliverable3/input_data/listings_oct_to_june.csv"
)

df <- listings_oct_to_june


# ---------------------------------------------------------
# Summary statistics for all columns
# ---------------------------------------------------------

summary_all <- map_dfr(names(df), function(col) {
  
  x <- df[[col]]
  
  missing_n <- sum(is.na(x))
  unique_n <- n_distinct(x, na.rm = TRUE)
  
  if (is.numeric(x) && !(col %in% c("id", "host_id", "year"))) {
    
    valid_x <- x[!is.na(x)]
    
    tibble(
      variable = col,
      type = "numeric",
      total_rows = length(x),
      missing = missing_n,
      missing_percent = round(
        missing_n / length(x) * 100, 2
      ),
      unique_values = unique_n,
      minimum = if(length(valid_x) == 0) NA_real_ else min(valid_x),
      maximum = if(length(valid_x) == 0) NA_real_ else max(valid_x),
      mean = if(length(valid_x) == 0) NA_real_ else mean(valid_x),
      std_dev = if(length(valid_x) <= 1) NA_real_ else sd(valid_x),
      most_common = NA_character_,
      most_common_count = NA_integer_
    )
    
  } else {
    
    y <- as.character(x)
    y <- y[!is.na(y) & y != ""]
    
    freq <- sort(table(y), decreasing = TRUE)
    
    common_value <- if(length(freq) == 0) {
      NA_character_
    } else {
      names(freq)[1]
    }
    
    common_count <- if(length(freq) == 0) {
      NA_integer_
    } else {
      as.integer(freq[1])
    }
    
    tibble(
      variable = col,
      type = ifelse(
        col %in% c("id", "host_id"),
        "identifier",
        "categorical/text"
      ),
      total_rows = length(x),
      missing = missing_n,
      missing_percent = round(
        missing_n / length(x) * 100, 2
      ),
      unique_values = unique_n,
      minimum = NA_real_,
      maximum = NA_real_,
      mean = NA_real_,
      std_dev = NA_real_,
      most_common = common_value,
      most_common_count = common_count
    )
  }
})


# ---------------------------------------------------------
# Category counts
# ---------------------------------------------------------

category_counts <- df |>
  select(
    neighbourhood_group,
    neighbourhood,
    room_type,
    month,
    year
  ) |>
  mutate(
    across(everything(), as.character)
  ) |>
  pivot_longer(
    cols = everything(),
    names_to = "variable",
    values_to = "category"
  ) |>
  mutate(
    category = replace_na(category, "<MISSING>")
  ) |>
  count(
    variable,
    category,
    name = "count"
  ) |>
  arrange(
    variable,
    desc(count)
  )

View(category_counts)


# ---------------------------------------------------------
# Last review date summary
# ---------------------------------------------------------

last_review_dates <- as.Date(df$last_review)

date_summary <- tibble(
  variable = "last_review",
  earliest_date = min(
    last_review_dates,
    na.rm = TRUE
  ),
  latest_date = max(
    last_review_dates,
    na.rm = TRUE
  ),
  missing = sum(
    is.na(last_review_dates)
  )
)

View(date_summary)


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

# Save the summary statistics
write_csv(
  summary_all,
  "Deliverable3/output_data/summary_statistics.csv"
)

# Save the category counts
write_csv(
  category_counts,
  "Deliverable3/output_data/category_counts.csv"
)

# Save the last review date summary
write_csv(
  date_summary,
  "Deliverable3/output_data/date_summary.csv"
)
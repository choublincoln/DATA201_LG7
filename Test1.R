"what to do up here: Basically run all this code all the way down until line 48
 you only want to do this ONCE ONLY!!"

library(tidyverse)
# chosen data-set we're focused on 
data_october <- read_csv("data/listings_october.csv") |> # |> is a pipe basically meaning "and then"
  filter(neighbourhood_group == "Christchurch City") |> # filters for Christchurch City.
  mutate(month = "October", year = 2025) # creates new columns with their assigned values.

data_november <- read_csv("data/listings_november.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "November", year = 2025)

data_december <- read_csv("data/listings_december.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "December", year = 2025)

data_january <- read_csv("data/listings_january.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "January", year = 2026)

data_february <- read_csv("data/listings_february.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "February", year = 2026)

data_march <- read_csv("data/listings_march.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "March", year = 2026)

data_april <- read_csv("data/listings_april.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "April", year = 2026)

data_may <- read_csv("data/listings_may.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "May", year = 2026)

data_june <- read_csv("data/listings_june.csv") |>
  filter(neighbourhood_group == "Christchurch City") |>
  mutate(month = "June", year = 2026)

# Combining the listings from October 2025 to June 2026
listings_oct_to_june <- bind_rows(data_october, data_november, data_december,
                                  data_january, data_february, data_march,
                                  data_april, data_may, data_june)

# Run Only Once to download the concatenated data-set in your data file
write.csv(listings_oct_to_june, "data/listings_oct_to_june.csv", row.names = FALSE)












## Data Wrangling Pipeline from here down below write your code down here
## COPY AND PASTE EVERYTHING FROM THE MAIN BRANCH AND PASTE IT IN YOUR OWN BRANCH.
## COMMIT AND PUSH IT SO ALL BRANCHES ARE SYNCED
## then start working on your workflow with the template of the no code solution.

#___________________________________________________________________________________________________

## Discover
listings_oct_to_june <- read_csv("data/listings_oct_to_june.csv") # MUST RUN


# Pallima statistics will be here
df <- listings_oct_to_june

# SUMMARY FOR ALL COLUMNS

summary_all <- map_dfr(names(df), function(col) {
  
  x <- df[[col]]
  missing_n <- sum(is.na(x))
  unique_n <- n_distinct(x, na.rm = TRUE)
  
  # Numeric columns
  # ID, host ID and year are not treated as normal numeric measures
  if (is.numeric(x) && !(col %in% c("id", "host_id", "year"))) {
    
    valid_x <- x[!is.na(x)]
    
    tibble(
      variable = col,
      type = "numeric",
      total_rows = length(x),
      missing = missing_n,
      missing_percent = round(missing_n / length(x) * 100, 2),
      unique_values = unique_n,
      
      minimum = if(length(valid_x) == 0) NA_real_
      else min(valid_x),
      
      maximum = if(length(valid_x) == 0) NA_real_
      else max(valid_x),
      
      mean = if(length(valid_x) == 0) NA_real_
      else mean(valid_x),
      
      std_dev = if(length(valid_x) <= 1) NA_real_
      else sd(valid_x),
      
      most_common = NA_character_,
      most_common_count = NA_integer_
    )
    
  } else {
    
    # Categorical / text / identifier columns
    y <- as.character(x)
    y <- y[!is.na(y) & y != ""]
    
    freq <- sort(table(y), decreasing = TRUE)
    
    common_value <- if(length(freq) == 0) NA_character_
    else names(freq)[1]
    
    common_count <- if(length(freq) == 0) NA_integer_
    else as.integer(freq[1])
    
    tibble(
      variable = col,
      type = ifelse(
        col %in% c("id", "host_id"),
        "identifier",
        "categorical/text"
      ),
      total_rows = length(x),
      missing = missing_n,
      missing_percent = round(missing_n / length(x) * 100, 2),
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

# CATEGORY + COUNT TABLE

category_counts <- df |>
  select(
    neighbourhood_group,
    neighbourhood,
    room_type,
    month,
    year
  ) |>
  mutate(across(everything(), as.character)) |>
  pivot_longer(
    cols = everything(),
    names_to = "variable",
    values_to = "category"
  ) |>
  mutate(
    category = replace_na(category, "<MISSING>")
  ) |>
  count(variable, category, name = "count") |>
  arrange(variable, desc(count))

# Open category counts
View(category_counts)

# Date summary for last_review

last_review_dates <- as.Date(df$last_review)

date_summary <- tibble(
  variable = "last_review",
  earliest_date = min(last_review_dates, na.rm = TRUE),
  latest_date = max(last_review_dates, na.rm = TRUE),
  missing = sum(is.na(last_review_dates))
)

View(date_summary)


write_csv(
  summary_all,
  "data/summary_statistics.csv"
)

write_csv(
  category_counts,
  "data/category_counts.csv"
)

write_csv(
  date_summary,
  "data/date_summary.csv"
)

#--- means your code should stop here for each part (helps prevent merging conflicts)

#___________________________________________________________________________________________________

## Structure
"Column Filter that drops unecessary Columns"
listings_oct_to_june <- listings_oct_to_june |>
  select(-host_id, -host_name, -room_type, -minimum_nights, -calculated_host_listings_count,
         -availability_365, -license) # MUST RUN

# Daniel

column_filter <- function(csvfile) { "Drops unecessary columns and returns data."
  drop_file <- csvfile |>
    select(-host_id, -host_name, -room_type, -minimum_nights, -calculated_host_listings_count,
           -availability_365, -license)
  drop_file
}

select_top <- function(data) { "Selects properties with highest numbers of reviews(10%)."
  num_reviews <- data |> select(id, name, number_of_reviews)
  num_rows <- nrow(data)
  percent_rows <- num_rows*0.1
  row_sort <- num_reviews[order(-num_reviews$number_of_reviews), ]
  top_properties <- row_sort[1:percent_rows, ]
  top_properties
}
#---

# Ean
class(listings_oct_to_june$last_review) # Already set to Date

#---

#___________________________________________________________________________________________________

## Clean

# Lincoln
listings_Lincoln_filtered <- listings_oct_to_june |>
  drop_na(price) # drops missing price values

#--- 

# Daniel


#---

# Ean
listings_Ean_filtered <- listings_oct_to_june |>
  drop_na(last_review)

#---

#___________________________________________________________________________________________________

## Enrich

# Ean
dataset_date <- as.Date("2026-06-22") # June's data-set date
listings_Ean_filtered <- listings_Ean_filtered |>
  mutate(day_difference_review = as.numeric(dataset_date - last_review)) # Makes a new column on the difference of the days since the last review
#---

#___________________________________________________________________________________________________

## Publish

# Lincoln
ggplot(listings_Lincoln_filtered, 
       aes(x = cut(price, 
                   breaks = c(0, 50, 100, 200, 500, 1000, Inf), # Histogram Cutoffs
                   labels = c("$0–$50", "$51–$100", "$101–$200", 
                              "$201–$500", "$501–$1000", "$1000+")))) + 
  geom_bar() +
  labs(title = "Price Distribution of Christchurch",
       x = "Price ($NZD)",
       y = "Number of Listings") + # Labels
  theme_bw()
#--- 

# Daniel

write_top <- function(data){ "Writes a csv file with the properties with highest reviews"
  filtered_data <- column_filter(data)
  top_reviews <- select_top(filtered_data)
  write.csv(top_reviews, "data/top_reviews.csv", row.names = FALSE)
  top_reviews
}

write_top(data_june)
#---

# Ean
ggplot(listings_Ean_filtered, 
       aes(x = cut(day_difference_review, 
                   breaks = c(0, 50, 100, 200, 500, 1000, Inf), # Histogram Cutoffs
                   labels = c("0–50", "51–100", "101–200", 
                              "201–500", "501–1000", "1000+")))) +
  geom_bar() +
  labs(
    title = "Day Difference on Last Review Distribution of Christchurch",
    x = "Days Since Last Review",
    y = "Number of Listings"
  ) +
  theme_bw()
#---

#___________________________________________________________________________________________________




# =========================================================
# EAN'S DATA WRANGLING PIPELINE
# =========================================================

library(tidyverse)


# =========================================================
# DISCOVER
# =========================================================

# Load the combined Airbnb dataset
combined_listings <- read_csv("output_data/Deliverable3_output/combined_listings.csv")

# Check the data type of last_review
class(combined_listings$last_review)


# =========================================================
# STRUCTURE
# =========================================================

# No Structure code contributed by Ean.


# =========================================================
# CLEAN
# =========================================================

# Remove listings with missing last_review values
listings_Ean_filtered <- combined_listings |>
  drop_na(last_review)


# =========================================================
# ENRICH
# =========================================================

# Add a date for each monthly dataset and calculate the
# number of days between the dataset date and last review date
listings_Ean_filtered <- listings_Ean_filtered |>
  mutate(
    month_number = match(month, month.name),
    
    dataset_date = as.Date(
      paste(year, month_number, "01", sep = "-"),
      format = "%Y-%m-%d"
    ),
    
    # Calculate the last calendar day of each month
    dataset_date = as.Date(
      format(dataset_date + 32, "%Y-%m-01")
    ) - 1,
    
    last_review = as.Date(last_review),
    
    day_difference_review = as.numeric(dataset_date - last_review)
  ) |>
  select(-month_number)


# Remove rows with invalid dataset dates
listings_Ean_filtered <- listings_Ean_filtered |>
  drop_na(dataset_date)


# Exclude late reviews causing negative values
listings_Ean_filtered <- listings_Ean_filtered |>
  filter(day_difference_review >= 0)


# =========================================================
# PUBLISH
# =========================================================

# Plot the distribution of the number of days between
# the dataset date and the last review
plot <- ggplot(
  listings_Ean_filtered,
  aes(x = cut(day_difference_review,
              breaks = c(0, 7, 14, 30, 50, 100, 200, 500, 1000, Inf),
              
              labels = c("0–7", "8–14", "15–30", "31–50",
                         "51–100", "101–200", "201–500",
                         "501–1000", "1000+"),
              
              include.lowest = TRUE))) +
  
  geom_bar() +
  labs(title = "Day Difference on Last Review Distribution of Christchurch",
       x = "Days Since Last Review",
       y = "Number of Listings") + theme_bw()


# Save the plot
ggsave("output_data/Deliverable3_output/date_difference.png",
       plot = plot,
       width = 6,
       height = 4,
       dpi = 150)
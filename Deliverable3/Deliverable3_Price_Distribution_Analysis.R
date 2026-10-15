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

combined_listings <- read_csv("output_data/Deliverable3_output/combined_listings.csv")



# Remove columns that are not required for the analysis.

combined_listings <- combined_listings |>
  select(-host_id, -host_name, -room_type, -minimum_nights, -calculated_host_listings_count,
         -availability_365, -license)


# =========================================================
# CLEAN
# =========================================================

# Keep the latest record for each unique listing ID
listings_filtered <- combined_listings |>
  mutate(month = factor(month, levels = month.name, ordered = TRUE)) |>
  arrange(year, month) |>
  group_by(id) |>
  slice_tail(n = 1) |>
  ungroup() |>
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

plot <- ggplot(listings_filtered,
  aes(x = cut(price,
      breaks = c(0, 50, 100, 200, 500, 1000, Inf),
      labels = c("$0–$50", "$51–$100", "$101–$200","$201–$500", "$501–$1000",
                  "$1000+")))) +
  geom_bar() +

  labs(title = "Price Distribution of Christchurch",
       x = "Price ($NZD)", y = "Number of Listings") + theme_bw()



# Downloading
ggsave("output_data/Deliverable3_output/price_distribution.png", plot = plot, width = 6,
        height = 4, dpi = 150)

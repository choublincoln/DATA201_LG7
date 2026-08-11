"what to do up here: Basically run all this code all the way down until line 46
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

# Lincoln


#--- means your code should stop here for each part (helps prevent merging conflicts)


# Pallima statistics will be here
min(data1$price,na.rm=TRUE)
max(data1$price,na.rm=TRUE)
sd(data1$price,na.rm=TRUE)
nrow(data1)
data1|>
  count(host_name)
#---

#___________________________________________________________________________________________________

## Structure
"Column Filter that drops unecessary Columns"
listings_oct_to_june <- listings_oct_to_june |>
  select(-host_id, -host_name, -room_type, -minimum_nights, -calculated_host_listings_count,
         -availability_365, -license) # MUST RUN
# Lincoln


#--- means your code should stop here for each part (helps prevent merging conflicts)

# Daniel


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
  mutate(day_difference_review = as.numeric(dataset_date - last_review)) # Makes a new column of the difference of the days since the last review
#---

#___________________________________________________________________________________________________

## Publish

# Lincoln
ggplot(listings_Lincoln_filtered, 
       aes(x = cut(price, breaks = c(0, 50, 100, 200,
                                     500, 1000, Inf)))) + # Histogram Cutoffs
  geom_bar() +
  labs(title = "Price Distribution of Christchurch",
       x = "Price ($NZD)",
       y = "Number of Listings") + # Labels
  theme_bw()
#--- 

# Daniel


#---

# Ean
ggplot(listings_Ean_filtered, 
       aes(x = cut(day_difference_review, breaks = c(0, 50, 100, 200,
                                     500, 1000, Inf)))) + # Histogram Cutoffs
  geom_bar() +
  labs(title = "Day Difference on Last Review Distribution of Christchurch",
       x = "Days",
       y = "Number of Listings") + # Labels
  theme_bw()

#---

#___________________________________________________________________________________________________












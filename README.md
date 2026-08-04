# DATA201_LG7
DATA201 26S2 Group
## Team
- Lincoln
- Ean
- Daniel
- Pallima


## Dataset Columns

| Field                                           | Type     | Calculated | Description                                                        |
|-------------------------------------------------|----------|------------|--------------------------------------------------------------------|
| id                                              | integer  |            | Airbnb's unique identifier for the listing                         |
| listing_url                                     | text     | Yes        | URL to the Airbnb listing                                          |
| scrape_id                                       | bigint   | Yes        | Inside Airbnb "Scrape" this listing was part of                    |
| last_scraped                                    | datetime | Yes        | UTC date and time the listing was scraped                          |
| source                                          | text     |            | Source of the listing ("neighbourhood search" or "previous scrape")|
| name                                            | text     |            | Name of the listing                                                |
| description                                     | text     |            | Detailed description of the listing                                |
| neighborhood_overview                           | text     |            | Host's description of the neighbourhood                            |
| picture_url                                     | text     |            | URL to the Airbnb-hosted listing image                             |
| host_id                                         | integer  |            | Airbnb's unique identifier for the host                            |
| host_url                                        | text     | Yes        | URL to the host's Airbnb profile                                   |
| host_name                                       | text     |            | Name of the host                                                   |
| host_since                                      | date     |            | Date the host joined Airbnb                                        |
| host_location                                   | text     |            | Host's self-reported location                                      |
| host_about                                      | text     |            | Description about the host                                         |
| host_response_time                              | text     |            | Typical response time of the host                                  |
| host_response_rate                              | text     |            | Percentage of messages the host responds to                        |
| host_acceptance_rate                            | text     |            | Rate at which the host accepts booking requests                    |
| host_is_superhost                               | boolean  |            | Whether the host is a Superhost (t/f)                              |
| host_thumbnail_url                              | text     |            | URL to the host's thumbnail image                                  |
| host_picture_url                                | text     |            | URL to the host's profile picture                                  |
| host_neighbourhood                              | text     |            | Host's neighbourhood                                               |
| host_listings_count                             | text     |            | Number of listings the host has                                    |
| host_total_listings_count                       | text     |            | Total number of listings the host has                              |
| host_verifications                              | text     |            | Verification methods completed by the host                         |
| host_has_profile_pic                            | boolean  |            | Whether the host has a profile picture (t/f)                       |
| host_identity_verified                          | boolean  |            | Whether the host's identity is verified (t/f)                      |
| neighbourhood                                   | text     |            | Neighbourhood name                                                 |
| neighbourhood_cleansed                          | text     | Yes        | Geocoded neighbourhood based on latitude and longitude             |
| neighbourhood_group_cleansed                    | text     | Yes        | Geocoded neighbourhood group                                       |
| latitude                                        | numeric  |            | Latitude (WGS84)                                                   |
| longitude                                       | numeric  |            | Longitude (WGS84)                                                  |
| property_type                                   | text     |            | Self-selected property type                                        |
| room_type                                       | text     |            | Entire home/apt, Private room, Shared room, or Hotel room          |
| accommodates                                    | integer  |            | Maximum number of guests accommodated                              |
| bathrooms                                       | numeric  |            | Number of bathrooms                                                |
| bathrooms_text                                  | string   |            | Text description of bathrooms                                      |
| bedrooms                                        | integer  |            | Number of bedrooms                                                 |
| beds                                            | integer  |            | Number of beds                                                     |
| amenities                                       | json     |            | List of amenities                                                  |
| price                                           | currency |            | Nightly listing price in local currency                            |
| minimum_nights                                  | integer  |            | Minimum nights per booking                                         |
| maximum_nights                                  | integer  |            | Maximum nights per booking                                         |
| minimum_minimum_nights                          | integer  | Yes        | Smallest minimum nights from the calendar                          |
| maximum_minimum_nights                          | integer  | Yes        | Largest minimum nights from the calendar                           |
| minimum_maximum_nights                          | integer  | Yes        | Smallest maximum nights from the calendar                          |
| maximum_maximum_nights                          | integer  | Yes        | Largest maximum nights from the calendar                           |
| minimum_nights_avg_ntm                          | numeric  | Yes        | Average minimum nights from the calendar                           |
| maximum_nights_avg_ntm                          | numeric  | Yes        | Average maximum nights from the calendar                           |
| calendar_updated                                | date     |            | Date the calendar was last updated                                 |
| has_availability                                | boolean  |            | Whether the listing is available (t/f)                             |
| availability_30                                 | integer  | Yes        | Availability in the next 30 days                                   |
| availability_60                                 | integer  | Yes        | Availability in the next 60 days                                   |
| availability_90                                 | integer  | Yes        | Availability in the next 90 days                                   |
| availability_365                                | integer  | Yes        | Availability in the next 365 days                                  |
| calendar_last_scraped                           | date     |            | Date the calendar was last scraped                                 |
| number_of_reviews                               | integer  |            | Total number of reviews                                            |
| number_of_reviews_ltm                           | integer  | Yes        | Number of reviews in the last 12 months                            |
| number_of_reviews_l30d                          | integer  | Yes        | Number of reviews in the last 30 days                              |
| first_review                                    | date     | Yes        | Date of the first review                                           |
| last_review                                     | date     | Yes        | Date of the most recent review                                     |
| review_scores_rating                            | numeric  |            | Overall rating                                                     |
| review_scores_accuracy                          | numeric  |            | Accuracy rating                                                    |
| review_scores_cleanliness                       | numeric  |            | Cleanliness rating                                                 |
| review_scores_checkin                           | numeric  |            | Check-in rating                                                    |
| review_scores_communication                     | numeric  |            | Communication rating                                               |
| review_scores_location                          | numeric  |            | Location rating                                                    |
| review_scores_value                             | numeric  |            | Value rating                                                       |
| license                                         | text     |            | Licence, permit, or registration number                            |
| instant_bookable                                | boolean  |            | Whether the listing can be booked instantly (t/f)                  |
| calculated_host_listings_count                  | integer  | Yes        | Number of listings the host has in the current scrape              |
| calculated_host_listings_count_entire_homes     | integer  | Yes        | Number of entire home listings the host has                        |
| calculated_host_listings_count_private_rooms    | integer  | Yes        | Number of private room listings the host has                       |
| calculated_host_listings_count_shared_rooms     | integer  | Yes        | Number of shared room listings the host has                        |
| reviews_per_month                               | numeric  | Yes        | Average number of reviews per month over the listing's lifetime    |

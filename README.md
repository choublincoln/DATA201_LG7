# DATA201_LG7
DATA201 26S2 Group
## Team
- Lincoln
- Ean
- Daniel
- Pallima


# Dataset Source

The dataset used in this project is the **New Zealand summary listings dataset** published by **Inside Airbnb**.

The file is named:

`listings.csv`

The selected snapshot is dated:

**19 June 2026**

Each row represents one Airbnb listing, while the 18 columns describe:

- Listing identity
- Host identity
- Geographic location
- Room type
- Price
- Minimum-night rules
- Reviews
- Calculated host-listing counts
- Future availability
- Licence information

Column definitions were interpreted using Inside Airbnb's **Version 4.3 listings data dictionary**.

---

# Source Information

| Source Item | Documentation |
|---|---|
| Publisher | Inside Airbnb, a mission-driven project that publishes data about Airbnb's effects on residential communities |
| Geographic coverage | New Zealand |
| Publication date | 19 June 2026 |
| File documented here | `listings.csv` — the summary listings file described by Inside Airbnb as suitable for visualizations |
| Unit of observation | One row represents one Airbnb listing observed in the New Zealand snapshot |

---

# Summary Dataset and Detailed Dictionary Relationship

The detailed dictionary file attached to Inside Airbnb provides detailed descriptions of the larger compressed dataset:


listings.csv.gz


However, in our analysis, we used the smaller 18-column summary dataset:


listings.csv


Since both datasets contain many of the same fields, we used the detailed dictionary as a reference to understand and describe the columns in our dataset.

However, two field names are slightly different between the two files. The following cross-reference table shows the corresponding fields used for our summary dataset.

| Summary-file column | Matching field in the detailed dictionary |
|---|---|
| neighbourhood_group | neighbourhood_group_cleansed |
| neighbourhood | neighbourhood_cleansed |
| All other fields | Same field name in the detailed dictionary |

---

# Data Dictionary: All 18 Source Columns

All 18 columns of our data file are given below.

| Column | Interpretation |
|---|---|
| **id** | Airbnb's unique identifier for one listing. It is a key used to distinguish and join records, not a quantity to calculate with. Store long IDs as text in Excel so they are not rounded. Even if a single host can have multiple listings, and that's why their host ID can appear repeatedly, for each listing this ID number is unique. |
| **name** | The public title or name of the listing. It helps identify a property for human readers, but titles are not standardised and may be blank. |
| **host_id** | Airbnb's unique identifier for the host or user. The same host_id can appear on several rows when one host has multiple listings. |
| **host_name** | The host's displayed name, usually a first name or names. It can be missing and is not a reliable unique identifier; use host_id when grouping hosts. |
| **neighbourhood_group** | The higher-level geographic area assigned from listing coordinates using public or open boundary files. In the New Zealand summary dataset, it identifies broad city or council areas, including Christchurch City. |
| **neighbourhood** | The more detailed geocoded neighbourhood within the broader group. It is assigned from latitude and longitude rather than entered consistently by hosts. |
| **latitude** | North-south coordinate in the WGS84 coordinate system. New Zealand latitudes are normally negative because the country is south of the Equator. Together with longitude, it gives an approximate map position. |
| **longitude** | East-west coordinate in the WGS84 coordinate system. New Zealand longitudes are normally positive east values. Pair it with latitude for mapping. |
| **room_type** | The accommodation category: Entire home/apt, Private room, Shared room, or Hotel room. It is useful for comparing price and availability across accommodation types. |
| **price** | The listing's daily or nightly advertised price in local currency. For this New Zealand dataset it should be interpreted as NZD. Blank prices should be excluded from price calculations rather than changed to zero. |
| **minimum_nights** | The minimum stay required for the listing at the time of the snapshot. Calendar-specific rules may differ, so this is a summary booking rule rather than a permanent value. |
| **number_of_reviews** | The total number of reviews recorded for the listing by the snapshot date. It is a lifetime count and can be used to rank highly reviewed listings. |
| **last_review** | The date of the most recent review. A blank value is normally valid when number_of_reviews is 0; a review date should not be invented. |
| **reviews_per_month** | Inside Airbnb's calculated average number of reviews per month over the listing's observed review history. It is not the same as reviews in the last calendar month and is normally blank for never-reviewed listings. |
| **calculated_host_listings_count** | The number of listings associated with the host in the current scrape and geographic coverage. It can distinguish single-listing hosts from multi-listing operators, but it is not necessarily the host's worldwide total. |
| **availability_365** | The number of days marked available during the next 365 days according to the listing calendar. An unavailable day may be booked or blocked by the host, so this field is not a direct occupancy measure. |
| **number_of_reviews_ltm** | The number of reviews received in the last twelve months before the snapshot. Unlike number_of_reviews, this field focuses on recent review activity. |
| **license** | A licence, permit or registration number when one is published. Blank values can mean not supplied, not applicable or unavailable; they should not automatically be treated as errors.



# Dataset 2: Detailed Quarterly Tenancy Rental Bond Dataset
# Dataset source

The dataset used in this project is the **Detailed Quarterly Tenancy Rental Bond dataset** published by **Tenancy Services, New Zealand**. The file is named **Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv**. Each row represents a quarterly rental bond record grouped by location, dwelling type, and number of bedrooms. The 12 columns describe rental market characteristics, including geographic identifiers, dwelling information, bond activity, and rental price statistics.

Column definitions were interpreted using the documentation provided by Tenancy Services for the rental bond dataset.

| **Source item** | **Documentation** |
| ---------------- | ---------------- |
| Publisher | Tenancy Services, Ministry of Business, Innovation & Employment (MBIE), New Zealand |
| Official source page | Tenancy Services Rental Bond data |
| Geographic coverage | New Zealand |
| Publication period | Quarterly records from Q1 2020 onwards |
| File documented here | Detailed Quarterly Tenancy Rental Bond dataset |
| Unit of observation | One row represents rental bond statistics for a specific location, dwelling type, and bedroom category during a quarter |

---

The detailed documentation provided by Tenancy Services describes the rental bond dataset and explains the meaning of each field included in the quarterly rental bond records. In our analysis, we used the **Detailed Quarterly Tenancy Rental Bond dataset (Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv)**, which contains 12 columns describing rental market activity, property characteristics, geographic identifiers, and rental price statistics.

Since the dataset documentation provides definitions for each field, we used the official Tenancy Services documentation as a reference to understand and describe the columns used in our analysis. The following data dictionary explains each column, its purpose, and how it is used within our project. Fields such as **Location ID** and **TimeFrame** were retained because they are important for future integration with the Christchurch listing dataset and for comparing rental trends across locations and time periods.

# Data dictionary: all 12 source columns

All 12 columns of our data file are given below.

| **Column** | **Interpretation** |
| ---------- | ------------------ |
| **TimeFrame** | The quarter or reporting period in which the rental bond records were collected. It helps identify when each rental market observation occurred and allows analysis of changes in rental prices, bond activity, and market trends over time. This field should be retained because it is required for time-based comparisons and future integration with other datasets. |
| **Location ID** | This column works like an ID number for each location in the dataset. Instead of storing the full location name, the dataset uses this unique number to identify different areas. It helps us know which rental records belong to the same place and is useful when we need to compare or join this dataset with another dataset based on location. |
| **Dwelling Type** | Dwelling Type tells us what type of property the rental record belongs to. For example, it helps us identify whether the rental is for a house, flat, or another type of dwelling. This information is useful because different property types may have different rental prices and market trends. |
| **Number Of Beds** | This column shows the number of bedrooms associated with each rental property record. It helps us understand the size of the property and allows us to compare rental prices and bond activity between properties with different numbers of bedrooms. |
| **Total Bonds** | This column shows us how many rental bonds were recorded for a particular type of property in a specific location and time period. It gives an idea of how many rental properties or tenancies are represented in the dataset and helps us analyse rental market activity. |
| **Active Bonds** | This column shows the number of rental bonds that were still active during a specific period. It represents rental agreements that were currently ongoing and had not ended at the time of reporting. This helps us understand the number of active rental properties or tenancies in a particular location. |
| **Closed Bonds** | Closed Bonds tells us how many rental agreements ended during a particular time and location. It helps us see how many tenancies have finished and provides information about rental market activity, such as tenant movement and changes in rental availability. |
| **Median Rent** | This column shows the typical weekly rental price for a particular group of properties. Instead of using the average, it shows the middle value, which gives a better idea of what most renters are likely to pay without being strongly affected by unusually expensive or cheap rentals. |
| **Geometric Mean Rent** | Geometric Mean Rent gives us an average rental price that is less affected by unusually expensive or cheap properties. It helps provide a more balanced view of rental prices, especially when rental values vary a lot within the same location or property group. |
| **Upper Quartile Rent** | This column tells us the rental price level for more expensive properties within a specific group. It helps us understand how much renters may pay for properties that are towards the higher-priced side of the market and compare differences in rental prices across locations or property types. |
| **Lower Quartile Rent** | Lower Quartile Rent tells us the rental price level for cheaper properties within a specific group. It helps us understand the lower range of rental costs and compare how affordable rental properties are across different locations or property types. |
| **Log Std Dev Weekly Rent** | This column shows the variation in weekly rental prices after applying a logarithmic transformation. It measures how much rental prices differ within a specific location, dwelling type, and bedroom category during a given period. A higher value indicates that rental prices are more spread out, while a lower value means rental prices are more similar. |

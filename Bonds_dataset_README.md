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

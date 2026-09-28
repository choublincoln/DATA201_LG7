# Data Cleaning Tasks

## Airbnb Dataset

### 1. Convert `id` from numeric to character

- The `id` variable will be converted from numeric to character/text.

### Why?

`id` is an identifier, not a quantitative measurement. Treating it as numeric could incorrectly imply that mathematical operations or comparisons between IDs are meaningful. Converting it to character makes its purpose as a unique identifier clearer and prevents it from being treated as a numerical variable during analysis.

### Duplicate IDs

Duplicate `id` values were retained because the dataset contains repeated observations of the same Airbnb listing across different months. The combination of `id`, month, and year distinguishes observations from different time periods. Removing duplicate IDs would incorrectly remove valid temporal observations and reduce the information available for analysing changes in rental prices and availability over time.

### Missing Price Values

The reason for the missingness is unknown, and the available variables do not provide sufficient evidence to determine a missing-data mechanism. Therefore, the missing values were retained rather than imputed, as imputing prices could introduce assumptions and potentially bias the analysis.

A missing price does not necessarily indicate that a property has no future availability. `availability_365` represents the number of days the listing is marked as available for booking over the following 365 days. Therefore, a listing can have `price = NA` while still having a high `availability_365` value. Since the reason for the missing price cannot be confirmed, the missing prices will only be excluded when conducting analyses that specifically require price information.

# Table for Columns to Keep/Delete Airbnb

| Column | Keep/Delete | Why |
|---|---|---|
| `id` | **Keep** | Unique Airbnb listing identifier needed to identify |
| `name` | **Delete** | Listing name isn't relevant to price vs. availability (our analysis) |
| `host_id` | **Delete** | Not relevant to the analysis |
| `host_name` | **Delete** | Not relevant to the analysis |
| `neighbourhood` | **Keep** | Could be useful for Christchurch geographic comparisons |
| `neighbourhood_group` | **Delete** | All observations belong to Christchurch City, making this column redundant. |
| `latitude` | **Keep** | Potentially useful for geographic analysis/joining |
| `longitude` | **Keep** | Potentially useful for geographic analysis/joining |
| `room_type` | **Keep** | Could explain differences in rental prices |
| `price` | **Keep** | Main variable we are comparing |
| `minimum_nights` | **Keep** | relevant to future analysis |
| `number_of_reviews` | **Delete** | Not relevant to the analysis |
| `last_review` | **Delete** | Not relevant to the analysis |
| `reviews_per_month` | **Delete** | Not relevant to the analysis |
| `calculated_host_listings_count` | **Delete** | Not relevant to the analysis |
| `availability_365` | **Keep** | This represents property availability |
| `number_of_reviews_ltm` | **Delete** | Not relevant to the analysis |
| `license` | **Delete** | Not relevant to the analysis 100% missing anyway |
| `month` | **Keep** | Important for comparing changes over time |
| `year` | **Keep** | Needed alongside month for the time period |

## Airbnb Dataset Summary

In summary: **11 variables/columns have been removed resulting in 9 variables/columns in the cleaned Airbnb Listings Dataset.**

---

# Bonds Dataset

## 2. Remove observations with missing Location ID

- Rows where Location ID is missing will be removed.

### Why?

The Location Id is needed to identify the corresponding geographic location. Without an ID, the observation cannot be reliably matched to a location, making it unsuitable for a location-specific analysis. Through statistics calculations, only 0.35% of observations had a missing Location Id, so removing these observations is expected to have minimal impact on the overall dataset.

### Number of Rows Affected: 794 were removed

---

## 3. Remove Location ID = -99

- Observations with Location ID = -99 will be removed.

### Why?

The value -99 does not correspond to a geographic location in the official Location ID definitions provided by Tenancy Services/Stats NZ, and its geographic meaning cannot be confirmed from the available documentation. Therefore, these observations cannot be reliably assigned to Christchurch or another specific location. As only 0.48% of observations have a Location Id of -99, removing them is expected to have minimal impact on the overall dataset while preventing unidentified observations from affecting the location-specific analysis.

[Stats NZ Datafinder — Statistical Area 2 2019 Generalised](https://datafinder.stats.govt.nz/layer/98970-statistical-area-2-2019-generalised/)

### Number of Rows Affected: 1091 were removed

---

## 4. Filter the Bonds Data to the Airbnb Study Period

- Only observations covering the same study period as the Airbnb dataset will be retained.

### Why?

The Airbnb dataset covers **October 2025 to June 2026**, so the bonds data should cover the corresponding period to allow meaningful comparison between the two datasets.

---

# Mini Data Conversions for Easier Future Analysis

## All Rent Columns

**Column data types → Number**

All the data types were previously: **character**

---

# Table for Columns to Keep/Delete Bonds

| Column | Keep/Delete | Why |
|---|---|---|
| `TimeFrame` | **Keep** | Needed to compare rental data over the same time periods as the Airbnb dataset. |
| `Location Id` | **Keep** | Needed to identify/filter Christchurch data. Can be removed later after filtering if no longer needed. |
| `Dwelling Type` | **Keep** | Useful for comparing different types of rental properties and potentially matching property types with Airbnb. |
| `Number Of Beds` | **Keep** | Useful for comparing properties of similar size and analysing rental-price differences. |
| `Total Bonds` | **Keep** | Provides information about the total number of rental bonds and can help describe the rental market. |
| `Active Bonds` | **Keep** | Important for measuring the number of currently active rental properties. |
| `Closed Bonds` | **Keep** | Not directly relevant to comparing current rental prices and property availability but may provide useful information |
| `Median Rent` | **Keep** | Important measure of conventional rental prices to compare with Airbnb prices. |
| `Geometric Mean Rent` | **Keep** | Provides another measure of typical rental prices and may be useful when comparing rental-price trends. |
| `Upper Quartile Rent` | **Keep** | Useful for understanding the distribution of rental prices and comparing higher-priced rentals. |
| `Lower Quartile Rent` | **Keep** | Useful for understanding the distribution of rental prices and comparing lower-priced rentals. |
| `Log Std Dev Weekly Rent` | **Keep** | Measures variability in weekly rent, but may provide useful information |

## Bonds Dataset Summary

In summary: ** no variables/columns have been removed










# Joining the Bonds Dataset and Airbnb
The Airbnb dataset was given SA2 area codes using the latitude and longitude of each listing. The bond dataset was then filtered to include only records where both Dwelling Type and Number of Beds were “ALL”, giving overall rental statistics rather than separate statistics for different property or bedroom types. This prevented multiple bond records from matching the same Airbnb observation. The datasets were then joined using SA2 code and time, with a left join so that all Airbnb observations were retained.

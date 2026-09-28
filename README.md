# DATA201_LG7
DATA201 26S2 Group
## Team
- Lincoln
- Ean
- Daniel
- Pallima

# Christchurch Rental Market Analysis

## Project Overview

This project analyses the Christchurch rental market using Airbnb listing data and Tenancy Services rental data. The aim is to combine and process these datasets to investigate patterns in rental prices, property characteristics, and rental availability across Christchurch.

The project involves collecting, cleaning, transforming, and combining data from different sources. The Airbnb dataset provides information about individual rental listings, including location, room type, price, availability, and minimum nights. The Tenancy Services dataset provides rental information such as median rent, geometric mean rent, upper and lower quartile rents, dwelling type, and location identifiers.

Because the datasets use different formats and geographic and time identifiers, several data-processing steps are required before they can be combined. Airbnb listings are matched to Statistical Area 2 (SA2) locations using their latitude and longitude coordinates. The resulting SA2 codes are then used to connect the Airbnb listings with the corresponding Tenancy Services data.

## Project Workflow

The project follows several main stages:

1. **Airbnb Data** – The Christchurch Airbnb listing data is prepared and cleaned for analysis.
2. **Tenancy Services Data** – Rental bond and rental market data from Tenancy Services is cleaned and prepared.
3. **Geographic Matching** – Airbnb listings are assigned an SA2 code based on their geographic coordinates.
4. **Time Matching** – The datasets are aligned using their relevant dates or time periods.
5. **Data Merging** – The Airbnb and Tenancy Services datasets are combined using common geographic and time identifiers.
6. **Analysis** – The resulting dataset can be used to investigate rental patterns across Christchurch.

## Data Sources

The project uses data from:

* **Airbnb listing data** – information about Christchurch Airbnb properties, including price, location, room type, availability, and minimum nights.
* **Tenancy Services** – New Zealand rental market data containing rental prices and related statistics by geographic area and time period.
* **Stats NZ Datafinder** – used to obtain SA2 geographic identifiers for Airbnb listings based on their latitude and longitude coordinates.

## Repository Contents

The repository contains the code, datasets, and documentation required to reproduce the data-processing workflow. Separate README files provide more detailed information about the individual datasets and the data-cleaning process.

* **Airbnb dataset** – information about Christchurch Airbnb listings.
* **Bonds/Tenancy dataset** – rental and bond information from Tenancy Services.
* **Data cleaning** – code and documentation describing the decisions made when cleaning and preparing the datasets.
* **SA2 matching and merging** – code used to assign geographic identifiers and combine the datasets.

## Reproducibility

The code is designed so that the data-processing steps can be rerun to reproduce the cleaned datasets and merged data. API credentials used for geographic matching are stored separately in an environment file and are not included in the repository.

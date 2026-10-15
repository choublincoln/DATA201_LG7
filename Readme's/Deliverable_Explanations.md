# Project Deliverables

## Deliverable 2: Initial Data Exploration
Downloaded the June 2026 New Zealand Airbnb listings dataset and explored its structure and key variables using a no-code data mining tool. Created visualisations to examine price distributions across New Zealand and Christchurch, calculated the number of days since each property's last review, and identified highly reviewed properties.

## Deliverable 3: Data Collection and Aggregation
Collected Airbnb listings datasets from October 2025 to June 2026, filtered them to include only Christchurch properties, and added a month-year column. Combined the monthly datasets into a single dataset and generated summary statistics and missing-value counts to understand the data.

## Deliverable 4: Data Cleaning and Preparation
Cleaned the combined Christchurch Airbnb dataset by handling missing values, removing unnecessary columns, and applying appropriate data preparation rules. Also downloaded, filtered, and cleaned the rental bond dataset from Tenancy Services to cover the same timeframe. Documented cleaning decisions and saved the prepared datasets for further analysis.

## Deliverable 5: Data Integration and Analysis
Used the Koordinates API and Stats NZ geographic data to assign area codes to Airbnb properties based on their latitude and longitude. Joined the Airbnb and rental bond datasets using geographic area codes and timeframes to compare short-term and long-term rental prices, property availability, and rental patterns across Christchurch.

## Deliverable 6: Code Quality and Design Principles
Reviewed and improved the data wrangling code to follow good coding practices. Documented the changes made, demonstrated how to sanity-check the pipeline, and created a design principles document describing the pipeline's inputs, outputs, main processing steps, and coding strategies.

## Deliverable 7: Pipeline Automation
Automated the data wrangling pipeline so that newly downloaded Airbnb datasets for July and August 2026 can be processed using a single command. Integrated the new months into the existing dataset and updated the analyses and visualisations without manually repeating each processing step.
# Deliverable 6: Documentation of Coding Practices

## 1. Team Contributions

### Lincoln

#### Repository Organisation
- Added folders for individual deliverables to improve file organisation and make files easier to locate.
- Updated code paths to reflect changes to the project structure.
- Created separate README files for data cleaning, the Airbnb dataset, and the rental bond dataset, while keeping the main README as a summary of the GitHub project.

#### Deliverable 3
- Separated different tasks into individual scripts for different group members rather than combining all code into one R script, improving readability and organisation.
- Added comments to improve code clarity.

#### Deliverable 4
- Added headings to improve readability and organisation.
- Added more comments to explain the code.

#### Deliverable 5: Joining and API
- **Comments and documentation:** Added comments explaining the purpose of important processing steps and checks.
- **Code organisation:** Structured the code into clear stages for loading, preparation, filtering, checking, and joining.
- **Readability:** Reformatted longer lines and removed unnecessary parentheses to make the code easier to read.
- **Sanity checking:** Documented the existing duplicate and matched/unmatched checks so their purpose is clear.
- **Reproducibility and data integrity:** Reviewed the code to ensure datasets are processed through code and the original input data is not overwritten.
- **Functionality:** The joining process itself was not changed because it was already working correctly.

### Daniel

#### Deliverable 4
- Added comments for clarity.
- Renamed variables to make their purpose clearer and the code more self-documenting.

#### Deliverable 5
- Removed or addressed magic numbers to improve code clarity.
- Renamed variables to make their purpose clearer and the code more self-documenting.
- Added comments for additional clarity.

### Pallima

#### Deliverable 3: Data Wrangling and Summary Statistics
- **Code organisation:** Organised the code into clear sections for discovering the data, generating summary statistics, calculating category counts, summarising dates, and producing outputs.
- **Summary statistics:** Created a summary of all variables, including variable type, number of rows, missing values, percentage of missing values, number of unique values, minimum, maximum, average, and standard deviation where applicable.
- **Handling different variable types:** Used different approaches for numeric and categorical/text variables. Numeric variables were summarised using minimum, maximum, average, and standard deviation, while categorical variables were summarised using their most common value and frequency.
- **Missing-value checking:** Calculated the number and percentage of missing values for each variable to help identify potential data-quality issues before further analysis.
- **Category counts:** Created frequency tables for important categorical variables such as `neighbourhood_group`, `neighbourhood`, `room_type`, month, and year to show how observations are distributed across categories.
- **Date checking:** Converted `last_review` into a date format and calculated the earliest and latest review dates, as well as the number of missing dates.
- **Readability and maintainability:** Used descriptive object names such as `summary_all`, `category_counts`, and `date_summary` to make each output easier to understand.
- **Reproducibility and data integrity:** Generated summary statistics and counts through code rather than calculating them manually. The original dataset was not overwritten, and the resulting summaries were saved as separate CSV files.
- **Output generation:** Saved `summary_statistics.csv`, `category_counts.csv`, and `date_summary.csv` so they could be reused in later stages of the project.

#### Deliverable 5: Christchurch Central Airbnb Price Analysis
- **Code organisation:** Structured the analysis into clear steps for loading the final joined dataset, filtering Christchurch Central listings, calculating the price statistic, and exporting the results.
- **Data filtering:** Filtered the dataset using the Christchurch Central SA2 code (`326600`) to ensure that only relevant Airbnb listings were included.
- **Comments and documentation:** Used clear variable names and explanations for each processing step, including dataset loading, area filtering, price calculation, and saving the output file.
- **Statistical calculation:** Calculated the median Airbnb price for Christchurch Central. The median was selected because Airbnb prices can contain extreme values, and the median provides a more representative measure of the typical listing price.
- **Sanity checking:** Inspected the filtered dataset using `head()` and confirmed that the SA2 code matched the intended location.
- **Output generation:** Created a separate summary file containing the neighbourhood, SA2 code, and price information. The output was saved as a CSV file for reuse in reporting and further analysis.
- **Reproducibility and data integrity:** Did not modify the original joined dataset. Filtering and calculations were performed through code, and the processed output was saved separately.
- **Functionality:** The main analysis process was not changed because the existing workflow correctly identified Christchurch Central listings and calculated the required price statistic.

### Ean

#### Deliverable 4: Timeframe Filtering
- **Sanity checking:** Added checks after converting `TimeFrame` to confirm that dates were parsed correctly, the October 2025 to June 2026 filter did not return an empty dataset, and every retained date fell within that period.
- **Readability:** Printed the distinct dates remaining after filtering so that the timeframe could be inspected and explained to the tutor.
- **Reliability:** Updated the script to create the output folder before saving the cleaned files.

#### Deliverable 5: Airbnb and Rental Property Comparison
- **Code review:** Reviewed the comparison by SA2 location, year, and quarter. The script counts unique Airbnb listing IDs and compares them with the `Active Bonds` rental count.
- **Sanity check identified:** Because the joined dataset repeats the rental count across Airbnb rows, `Active Bonds` should be checked for one consistent value for each location and quarter before selecting its first value.
- **Scope:** The current comparison counts properties. The optional comparison of beds has not been implemented.

---

## 2. Design Principles Document

### 2.1 Inputs to the Pipeline

Our pipeline uses two main datasets:

- Airbnb listings dataset containing Christchurch Airbnb listings.
- Rental bond dataset containing Christchurch rental bond information.

The Airbnb data includes important variables such as:

- Listing ID
- Neighbourhood
- Latitude
- Longitude
- Room type
- Price
- Availability
- Month
- Year

The latitude and longitude values are also used with the Koordinates API and a Stats NZ geographic dataset to identify the correct area code for each Airbnb listing.

The rental bond data contains rental information that can be matched with the Airbnb data using geographic area codes and a similar timeframe.

### 2.2 Outputs from the Pipeline

The main outputs from the pipeline are cleaned datasets that are ready for analysis.

The cleaned Airbnb dataset contains only the variables needed for the project, while retaining latitude and longitude for geographic matching. An additional area-code column is added using the Koordinates API.

The rental bond dataset is cleaned and filtered so that it contains Christchurch data for the required timeframe.

The final outputs can then be used to compare Airbnb activity with rental-market information across different geographic areas in Christchurch.

### 2.3 Main Steps in the Pipeline

The pipeline follows these main steps:

1. **Import the datasets:** Load the Airbnb listings and rental bond datasets into the program.
2. **Clean the Airbnb data:** Keep only the variables required for the project and convert variables into suitable data types where necessary.
3. **Clean the rental bond data:** Remove unnecessary information and keep the data relevant to Christchurch.
4. **Filter the timeframe:** Filter the rental bond dataset so that it matches the Airbnb timeframe, from October 2025 to June 2026.
5. **Obtain geographic area codes:** Use the latitude and longitude from each Airbnb listing to query the Koordinates API and identify the matching Stats NZ area code.
6. **Add the area code to the Airbnb dataset:** Store the returned area code as a new column in the Airbnb dataset.
7. **Perform sanity checks:** Check that important transformations have worked correctly. For example, verify that filtered dates fall within the correct timeframe and check for missing area codes.
8. **Save the cleaned datasets:** Export the processed datasets into the output folder so they can be used for later analysis.

### 2.4 Coding and Software Strategies

Several coding best practices are used throughout the project.

#### Clear Variable Names

Descriptive variable and dataset names are used so that team members can understand what each object represents. For example, `Airbnb_listings_cleaned` and `bonds_filtered` clearly describe the contents of the datasets.

#### Organised Code Structure

The code is divided into sections based on the different stages of the pipeline, such as importing, cleaning, filtering, API querying, validation, and exporting.

This makes the code easier to read, maintain, and debug.

#### Comments and Documentation

Comments are used to explain the purpose of important sections of the code. The focus is on explaining why a section exists rather than commenting on every individual line.

#### Avoiding Repeated Code

Where possible, repeated tasks should be placed into functions or reusable processes. This reduces duplication and makes the code easier to update.

#### Reproducibility

The original datasets are kept separate from the cleaned outputs. Changes to the data are performed through code rather than by manually editing the files.

This allows the pipeline to be rerun and its processing steps to be repeated.

#### Sanity Checking

Checks are included at important stages of the pipeline to make sure the results are reasonable.

For example, after filtering the rental bond data, the minimum and maximum dates can be checked to ensure that they fall between October 2025 and June 2026.

Missing area codes can also be checked after using the Koordinates API.

#### Maintaining Data Integrity

The pipeline avoids changing the original raw datasets. Instead, cleaned versions are created and saved separately.

This reduces the risk of accidentally losing or modifying the original data.

### 2.5 Overall Design Principle

The overall design of the pipeline is to create a workflow that is clear, organised, reproducible, and easy to check.

Each stage of the pipeline has a specific purpose, and sanity checks are used to help ensure that the data is processed correctly before it is used for analysis.

### 2.6 AI-Assisted Documentation

AI was used to assist with the preparation of the design principles document.

During the review, the team noticed that the initial AI-generated description focused on the Airbnb dataset and did not account for the rental bond dataset. This omission was identified and the documentation was revised to include both datasets and their roles in the pipeline.

### TO RUN THE PIPELINE, USE THE FOLLOWING COMMANDS:
# 1: DOWNLOAD "winget install GnuWin32.Make" IN THE TERMINAL TO INSTALL MAKE
# 2: CLOSE AND REOPEN THE TERMINAL
# 

# =========================================================
# DATA201 - AUTOMATED DATA WRANGLING PIPELINE
# =========================================================

PYTHON ?= python
RSCRIPT ?= Rscript

# =========================================================
# 1. INPUT FILES
# =========================================================

MONTHLY_LISTINGS := $(wildcard input_data/listings_*.csv)

BONDS_INPUT := input_data/bonds.csv
GEOGRAPHIC_MAPPING := input_data/geographic-areas-table-2023.csv

# =========================================================
# 2. OUTPUT DIRECTORIES
# =========================================================

D3_DIR := output_data/Deliverable3_output
D4_DIR := output_data/Deliverable4_output
D5_DIR := output_data/Deliverable5_output

# =========================================================
# 3. DELIVERABLE 3 OUTPUTS
# =========================================================

COMBINED_LISTINGS := $(D3_DIR)/combined_listings.csv

HIGHEST_REVIEWS := $(D3_DIR)/highest_reviews.csv
DATE_DIFFERENCE := $(D3_DIR)/date_difference.png
PRICE_DISTRIBUTION := $(D3_DIR)/price_distribution.png
SUMMARY_STATISTICS := $(D3_DIR)/summary_statistics.csv

# =========================================================
# 4. DELIVERABLE 4 OUTPUTS
# =========================================================

AIRBNB_CLEANED := $(D4_DIR)/Airbnb_listings_cleaned.csv
TENANCY_CLEANED := $(D4_DIR)/tenancy_cleaned.csv

# =========================================================
# 5. DELIVERABLE 5 OUTPUTS
# =========================================================

AIRBNB_SA2 := $(D5_DIR)/Airbnb_listings_sa2.csv
AIRBNB_UNIQUE_SA2 := $(D5_DIR)/Airbnb_unique_listings_sa2.csv

JOINED_DATA := $(D5_DIR)/Airbnb_bond_joined_final.csv

SA3_COMPARISON := $(D5_DIR)/airbnb_vs_rentals_sa3.png
CENTRAL_PRICES := $(D5_DIR)/Christchurch_Central_Airbnb_prices.csv
RENT_DIFFERENCE := $(D5_DIR)/listings_sa3_rent_diff.csv

# =========================================================
# 6. DEFAULT TARGET
# =========================================================

.PHONY: all deliverable3 deliverable4 deliverable5

all: deliverable3 deliverable4 deliverable5

# =========================================================
# 7. CREATE OUTPUT DIRECTORIES
# =========================================================

$(D3_DIR):
	$(PYTHON) -c "import os; os.makedirs('$(D3_DIR)', exist_ok=True)"

$(D4_DIR):
	$(PYTHON) -c "import os; os.makedirs('$(D4_DIR)', exist_ok=True)"

$(D5_DIR):
	$(PYTHON) -c "import os; os.makedirs('$(D5_DIR)', exist_ok=True)"

# =========================================================
# 8. DELIVERABLE 3 - COMBINE MONTHLY DATASETS
# =========================================================

$(COMBINED_LISTINGS): $(MONTHLY_LISTINGS) Deliverable3/Deliverable3_combining_datasets.R | $(D3_DIR)
	$(RSCRIPT) Deliverable3/Deliverable3_combining_datasets.R

# =========================================================
# 9. DELIVERABLE 3 - ANALYSIS PIPELINES
# =========================================================

$(HIGHEST_REVIEWS): $(COMBINED_LISTINGS) Deliverable3/Deliverable3_DataPipeline_Daniel.R
	$(RSCRIPT) Deliverable3/Deliverable3_DataPipeline_Daniel.R

$(DATE_DIFFERENCE): $(COMBINED_LISTINGS) Deliverable3/Deliverable3_DataPipeline_Ean.R
	$(RSCRIPT) Deliverable3/Deliverable3_DataPipeline_Ean.R

$(PRICE_DISTRIBUTION): $(COMBINED_LISTINGS) Deliverable3/Deliverable3_DataPipeline_Lincoln.R
	$(RSCRIPT) Deliverable3/Deliverable3_DataPipeline_Lincoln.R

$(SUMMARY_STATISTICS): $(COMBINED_LISTINGS) Deliverable3/Deliverable3_DataPipeline_Pallima.R
	$(RSCRIPT) Deliverable3/Deliverable3_DataPipeline_Pallima.R

deliverable3: $(COMBINED_LISTINGS) $(HIGHEST_REVIEWS) $(DATE_DIFFERENCE) $(PRICE_DISTRIBUTION) $(SUMMARY_STATISTICS)

# =========================================================
# 10. DELIVERABLE 4 - DATA CLEANING
# =========================================================

$(AIRBNB_CLEANED): $(COMBINED_LISTINGS) Deliverable4/clean_airbnb_data.R | $(D4_DIR)
	$(RSCRIPT) Deliverable4/clean_airbnb_data.R

$(TENANCY_CLEANED): $(BONDS_INPUT) Deliverable4/clean_tenancy_data.R | $(D4_DIR)
	$(RSCRIPT) Deliverable4/clean_tenancy_data.R

deliverable4: $(AIRBNB_CLEANED) $(TENANCY_CLEANED)

# =========================================================
# 11. DELIVERABLE 5 - SA2 API LOOKUP
# =========================================================

$(AIRBNB_SA2): $(AIRBNB_CLEANED) Deliverable5/Deliverable5_API.py .env | $(D5_DIR)
	$(PYTHON) Deliverable5/Deliverable5_API.py

# =========================================================
# 12. DELIVERABLE 5 - JOIN DATASETS
# =========================================================

$(JOINED_DATA): $(AIRBNB_SA2) $(TENANCY_CLEANED) Deliverable5/Deliverable_join.py
	$(PYTHON) Deliverable5/Deliverable_join.py

# =========================================================
# 13. DELIVERABLE 5 - ANALYSIS OUTPUTS
# =========================================================

$(SA3_COMPARISON): $(JOINED_DATA) $(GEOGRAPHIC_MAPPING) Deliverable5/Delivarable5_Ean.py
	$(PYTHON) Deliverable5/Delivarable5_Ean.py

$(CENTRAL_PRICES): $(JOINED_DATA) Deliverable5/Deliverable5-Pallima.py
	$(PYTHON) Deliverable5/Deliverable5-Pallima.py

$(RENT_DIFFERENCE): $(JOINED_DATA) $(GEOGRAPHIC_MAPPING) Deliverable5/largest_rent_diff_D5.py
	$(PYTHON) Deliverable5/largest_rent_diff_D5.py

deliverable5: $(AIRBNB_SA2) $(JOINED_DATA) $(SA3_COMPARISON) $(CENTRAL_PRICES) $(RENT_DIFFERENCE)

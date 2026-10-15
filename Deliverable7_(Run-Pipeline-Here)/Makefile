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
JOINED_DATA := $(D5_DIR)/Airbnb_bond_joined_final.csv

SA3_COMPARISON := $(D5_DIR)/airbnb_vs_rentals_sa3.png
CENTRAL_PRICES := $(D5_DIR)/Christchurch_Central_Airbnb_prices.csv
RENT_DIFFERENCE := $(D5_DIR)/listings_sa3_rent_diff.csv


# =========================================================
# 6. REPORT OUTPUT
# =========================================================

REPORT := Overall_report.html


# =========================================================
# 7. DEFAULT TARGET
# =========================================================

.PHONY: all deliverable3 deliverable4 deliverable5 clean

all: $(REPORT)


# =========================================================
# 8. CREATE OUTPUT DIRECTORIES
# =========================================================

$(D3_DIR):
	$(PYTHON) -c "import os; os.makedirs('$(D3_DIR)', exist_ok=True)"

$(D4_DIR):
	$(PYTHON) -c "import os; os.makedirs('$(D4_DIR)', exist_ok=True)"

$(D5_DIR):
	$(PYTHON) -c "import os; os.makedirs('$(D5_DIR)', exist_ok=True)"


# =========================================================
# 9. DELIVERABLE 3 - COMBINE MONTHLY DATASETS
# =========================================================

$(COMBINED_LISTINGS): \
	$(MONTHLY_LISTINGS) \
	Deliverable3/Deliverable3_Combine_Monthly_Listings.R | $(D3_DIR)
	$(RSCRIPT) Deliverable3/Deliverable3_Combine_Monthly_Listings.R


# =========================================================
# 10. DELIVERABLE 3 - ANALYSIS
# =========================================================

$(HIGHEST_REVIEWS): \
	$(COMBINED_LISTINGS) \
	Deliverable3/Deliverable3_Highest_Reviews_Analysis.R
	$(RSCRIPT) Deliverable3/Deliverable3_Highest_Reviews_Analysis.R


$(DATE_DIFFERENCE): \
	$(COMBINED_LISTINGS) \
	Deliverable3/Deliverable3_Date_Difference_Analysis.R
	$(RSCRIPT) Deliverable3/Deliverable3_Date_Difference_Analysis.R


$(PRICE_DISTRIBUTION): \
	$(COMBINED_LISTINGS) \
	Deliverable3/Deliverable3_Price_Distribution_Analysis.R
	$(RSCRIPT) Deliverable3/Deliverable3_Price_Distribution_Analysis.R


$(SUMMARY_STATISTICS): \
	$(COMBINED_LISTINGS) \
	Deliverable3/Deliverable3_Summary_Statistics.R
	$(RSCRIPT) Deliverable3/Deliverable3_Summary_Statistics.R


deliverable3: \
	$(COMBINED_LISTINGS) \
	$(HIGHEST_REVIEWS) \
	$(DATE_DIFFERENCE) \
	$(PRICE_DISTRIBUTION) \
	$(SUMMARY_STATISTICS)


# =========================================================
# 11. DELIVERABLE 4 - DATA CLEANING
# =========================================================

$(AIRBNB_CLEANED): \
	$(COMBINED_LISTINGS) \
	Deliverable4/Deliverable4_Clean_Airbnb_Data.R | $(D4_DIR)
	$(RSCRIPT) Deliverable4/Deliverable4_Clean_Airbnb_Data.R


$(TENANCY_CLEANED): \
	$(BONDS_INPUT) \
	Deliverable4/Deliverable4_Clean_Tenancy_Data.R | $(D4_DIR)
	$(RSCRIPT) Deliverable4/Deliverable4_Clean_Tenancy_Data.R


deliverable4: \
	$(AIRBNB_CLEANED) \
	$(TENANCY_CLEANED)


# =========================================================
# 12. DELIVERABLE 5 - ASSIGN SA2 CODES
# =========================================================

$(AIRBNB_SA2): \
	$(AIRBNB_CLEANED) \
	Deliverable5/Deliverable5_Assign_SA2_Codes.py \
	.env | $(D5_DIR)
	$(PYTHON) Deliverable5/Deliverable5_Assign_SA2_Codes.py


# =========================================================
# 13. DELIVERABLE 5 - JOIN DATASETS
# =========================================================

$(JOINED_DATA): \
	$(AIRBNB_SA2) \
	$(TENANCY_CLEANED) \
	Deliverable5/Deliverable5_Join_Airbnb_Tenancy.py
	$(PYTHON) Deliverable5/Deliverable5_Join_Airbnb_Tenancy.py


# =========================================================
# 14. DELIVERABLE 5 - ANALYSIS
# =========================================================

$(SA3_COMPARISON): \
	$(JOINED_DATA) \
	$(GEOGRAPHIC_MAPPING) \
	Deliverable5/Deliverable5_Compare_Airbnb_Rentals.py
	$(PYTHON) Deliverable5/Deliverable5_Compare_Airbnb_Rentals.py


$(CENTRAL_PRICES): \
	$(JOINED_DATA) \
	Deliverable5/Deliverable5_Christchurch_Central_Prices.py
	$(PYTHON) Deliverable5/Deliverable5_Christchurch_Central_Prices.py


$(RENT_DIFFERENCE): \
	$(JOINED_DATA) \
	$(GEOGRAPHIC_MAPPING) \
	Deliverable5/Deliverable5_Rental_Price_Difference.py
	$(PYTHON) Deliverable5/Deliverable5_Rental_Price_Difference.py


deliverable5: \
	$(AIRBNB_SA2) \
	$(JOINED_DATA) \
	$(SA3_COMPARISON) \
	$(CENTRAL_PRICES) \
	$(RENT_DIFFERENCE)


# =========================================================
# 15. OVERALL REPORT
# =========================================================

$(REPORT): \
	Overall_report.Rmd \
	$(COMBINED_LISTINGS) \
	$(HIGHEST_REVIEWS) \
	$(DATE_DIFFERENCE) \
	$(PRICE_DISTRIBUTION) \
	$(SUMMARY_STATISTICS) \
	$(AIRBNB_CLEANED) \
	$(TENANCY_CLEANED) \
	$(AIRBNB_SA2) \
	$(JOINED_DATA) \
	$(SA3_COMPARISON) \
	$(CENTRAL_PRICES) \
	$(RENT_DIFFERENCE)
	$(RSCRIPT) -e "rmarkdown::render('Overall_report.Rmd', output_file='Overall_report.html')"


# =========================================================
# 16. CLEAN
# =========================================================

clean:
	$(PYTHON) -c "import shutil, os; [shutil.rmtree(p, ignore_errors=True) for p in ['$(D3_DIR)', '$(D4_DIR)', '$(D5_DIR)']]; os.remove('$(REPORT)') if os.path.exists('$(REPORT)') else None"
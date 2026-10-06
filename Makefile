.PHONY: all clean

all: report.html


# =========================================================
# DELIVERABLE 3
# =========================================================

output_data/listings_oct_to_august.rds: \
	Deliverable3/Deliverable3_combining_datasets.R \
	input_data/listings_october.csv \
	input_data/listings_november.csv \
	input_data/listings_december.csv \
	input_data/listings_january.csv \
	input_data/listings_february.csv \
	input_data/listings_march.csv \
	input_data/listings_april.csv \
	input_data/listings_may.csv \
	input_data/listings_june.csv \
	input_data/listings_july.csv \
	input_data/listings_august.csv
	Rscript Deliverable3/Deliverable3_combining_datasets.R


output_data/highest_reviews.rds: \
	Deliverable3/Deliverable3_DataPipeline_Daniel.R \
	input_data/listings_august.csv
	Rscript Deliverable3/Deliverable3_DataPipeline_Daniel.R


output_data/date_difference.png: \
	Deliverable3/Deliverable3_DataPipeline_Ean.R \
	output_data/listings_oct_to_august.rds
	Rscript Deliverable3/Deliverable3_DataPipeline_Ean.R


output_data/price_distribution.png: \
	Deliverable3/Deliverable3_DataPipeline_Lincoln.R \
	output_data/listings_oct_to_august.rds
	Rscript Deliverable3/Deliverable3_DataPipeline_Lincoln.R


# =========================================================
# DELIVERABLE 4
# =========================================================

output_data/airbnb_listings_cleaned.rds: \
	clean_airbnb_data.R \
	output_data/listings_oct_to_august.rds
	Rscript clean_airbnb_data.R

output_data/tenancy_cleaned.rds: \
	clean_tenancy_data.R \
	input_data/bonds.csv
	Rscript clean_tenancy_data.R


# =========================================================
# DELIVERABLE 5
# =========================================================

output_data/Airbnb_listings_sa2.rds: \
	Deliverable5/Deliverable5_API.py \
	output_data/airbnb_listings_cleaned.rds
	Python Deliverable5/Deliverable5_API.py

output_data/Airbnb_bond_joined_final.rds: \
	Deliverable5/Deliverable5_join.py \
	output_data/Airbnb_listings_sa2.rds \
	output_data/tenancy_cleaned.rds
	Python Deliverable5/Deliverable5_join.py

output_data/airbnb_vs_rentals.png: \
	Deliverable5/Delivarable5_Ean.py \
	output_data/Airbnb_bond_joined_final.rds
	Python Deliverable5/Delivarable5_Ean.py

output_data/listings_sa3_rent_diff.rds: \
	Deliverable5/largest_rent_diff_D5.py \
	output_data/Airbnb_bond_joined_final.rds \
	input_data/geographic-areas-table-2023.csv \
	Python Deliverable5/largest_rent_diff_D5.py

output_data/Christchurch_Central_Airbnb_prices.rds: \
	Deliverable5/Deliverable5-Pallima.py \
	output_data/Airbnb_bond_joined_final.rds
	Python Deliverable5/Deliverable5-Pallima.py

# =========================================================
# REPORT
# =========================================================

report.html: \
	report.qmd \
	output_data/listings_oct_to_august.rds \
	output_data/highest_reviews.rds \
	output_data/date_difference.png \
	output_data/price_distribution.png \
	output_data/airbnb_listings_cleaned.rds \
	output_data/tenancy_cleaned.rds \
	output_data/Airbnb_listings_sa2.rds \
	output_data/Airbnb_bond_joined_final.rds
	quarto render report.qmd


# =========================================================
# CLEAN
# =========================================================

clean:
	rm -f output_data/listings_oct_to_august.rds \
	      output_data/highest_reviews.rds \
	      output_data/date_difference.png \
	      output_data/price_distribution.png \
	      output_data/airbnb_listings_cleaned.rds \
	      output_data/tenancy_cleaned.rds \
	      output_data/Airbnb_listings_sa2.rds \
	      output_data/Airbnb_listings_sa2_TEST.rds \
	      report.html

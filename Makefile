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

output_data/airbnb_listings_cleaned.rds \
output_data/tenancy_cleaned.rds: \
	Deliverable4/Deliverable4.R \
	output_data/listings_oct_to_august.rds \
	input_data/bonds.csv
	Rscript Deliverable4/Deliverable4.R


# =========================================================
# DELIVERABLE 5
# =========================================================

output_data/Airbnb_listings_sa2.rds: \
	Deliverable5/Deliverable5_API.py \
	output_data/airbnb_listings_cleaned.rds
	python Deliverable5/Deliverable5_API.py


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
	output_data/Airbnb_listings_sa2.rds
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

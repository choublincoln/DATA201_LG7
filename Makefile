.PHONY: all clean

all: report.html

output_data/listings_oct_to_august.rds: Deliverable3/Deliverable3_combining_datasets.R \
	listings_october.csv \
	listings_november.csv \
	listings_december.csv \
	listings_january.csv \
	listings_february.csv \
	listings_march.csv \
	listings_april.csv \
	listings_may.csv \
	listings_june.csv \
	listings_july.csv \
	listings_august.csv
	Rscript Deliverable3/Deliverable3_combining_datasets.R

output_data/highest_reviews.rds: Deliverable3/Deliverable3_DataPipeline_Daniel.R input_data/listings_august.csv
	Rscript Deliverable3/Deliverable3_DataPipeline_Daniel.R

output_data/date_difference.png: Deliverable3/Deliverable3_DataPipeline_Ean.R output_data/listings_oct_to_august.rds
	Rscript Deliverable3/Deliverable3_DataPipeline_Ean.R
	
output_data/price_distribution.png: Deliverable3/Deliverable3_DataPipeline_Lincoln.R output_data/listings_oct_to_august.rds
	Rscript Deliverable3/Deliverable3_DataPipeline_Lincoln.R

output_data/airbnb_listings_cleaned.rds: Deliverable4/clean_airbnb_data.R output_data/listings_oct_to_august.rds
	Rscript Deliverable4/clean_airbnb_data.R

output_data/output_data/tenancy_cleaned.rds: Deliverable4/clean_tenancy_data.R input_data/bonds.csv
	Rscript Deliverable4/clean_tenancy_data.R
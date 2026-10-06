.PHONY: all clean

all: report.html

output_data/listings_oct_to_august.rds: Deliverable3/Deliverable3_combining_datasets.R
	Rscript Deliverable3/Deliverable3_combining_datasets.R

<<<<<<< HEAD
output_data/highest_reviews.rds: Deliverable_DataPipeline_Daniel.R input_data/listings_august.csv
	Rscript Deliverable_DataPipeline_Daniel.R

output_data/date_difference.png: Deliverable_DataPipeline_Ean.R output_data/listings_oct_to_august.rds
	Rscript Deliverable_DataPipeline_Ean.R
	
output_data/date_difference.png: Deliverable_DataPipeline_Lincoln.R output_data/listings_oct_to_august.rds
	Rscript Deliverable_DataPipeline_Lincoln.R
=======
output_data/highest_reviews.rds: Deliverable3/Deliverable3_DataPipeline_Daniel.R input_data/listings_august.csv
	Rscript Deliverable3/Deliverable3_DataPipeline_Daniel.R

output_data/date_difference.png: Deliverable3/Deliverable3_DataPipeline_Ean.R output_data/listings_oct_to_august.rds
	Rscript Deliverable3/Deliverable3_DataPipeline_Ean.R
	
output_data/date_difference.png: Deliverable3/Deliverable3_DataPipeline_Lincoln.R output_data/listings_oct_to_august.rds
	Rscript Deliverable3/Deliverable3_DataPipeline_Lincoln.R
>>>>>>> 57f0a8d67dfb9813530e20a6a69bea75018b2de8

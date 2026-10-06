.PHONY: all clean

all: report.html

output_data/listings_oct_to_august.rds: Deliverable3/Deliverable3_combining_datasets.R
	Rscript Deliverable3/Deliverable3_combining_datasets.R


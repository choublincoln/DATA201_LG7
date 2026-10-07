import subprocess
import sys

subprocess.run([r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe", "Deliverable3/Deliverable3_combining_datasets.R"], check=True)
subprocess.run([r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe", "Deliverable3/Deliverable3_DataPipeline_Daniel.R"], check=True)
subprocess.run([r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe", "Deliverable3/Deliverable3_DataPipeline_Ean.R"], check=True)
subprocess.run([r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe", "Deliverable3/Deliverable3_DataPipeline_Lincoln.R"], check=True)
subprocess.run([r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe", "Deliverable3/Deliverable3_DataPipeline_Pallima.R"], check=True)

subprocess.run([r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe", "Deliverable4/clean_airbnb_data.R"], check=True)
subprocess.run([r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe", "Deliverable4/clean_tenancy_data.R"], check=True)

# subprocess.run([sys.executable, "Deliverable5/Deliverable5_API.py"], check=True)
subprocess.run([sys.executable, "Deliverable5/Deliverable5_join.py"], check=True)
# subprocess.run([sys.executable, "Deliverable5/Deliverable5_Ean.py"], check=True)
subprocess.run([sys.executable, "Deliverable5/Deliverable5_Pallima.py"], check=True)
subprocess.run([sys.executable, "Deliverable5/largest_rent_diff_D5.py"], check=True)
"what to do here: Basically run all this code you only want to do this ONCE ONLY!!"
"The output data we get will go into the Data3 Folder that you should have created"

library(tidyverse)
listings_oct_to_june <- read_csv("data/listings_oct_to_june.csv") # MUST RUN

#___________________________________________________________________________________________________

"place functions in here :)"

#___________________________________________________________________________________________________

drop_column <- function(csvfile, col_name) {"Drops unnecessary columns."
  drop_file <- csvfile |>
    select(-all_of(col_name))
  drop_file
  }


drop_row <- function(csvfile, col_name) {"Drops problematic rows. Not sure if this is necessary."
  new_data |>
    filter(!is.na(.csvfile[[col_name]]))
  new_data
  }


na_rent <- function(csvfile) {"Drops listings that probably have not been rented."
  
  }
#___________________________________________________________________________________________________



#___________________________________________________________________________________________________



#___________________________________________________________________________________________________



#___________________________________________________________________________________________________
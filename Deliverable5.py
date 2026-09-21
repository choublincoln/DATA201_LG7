"Lincoln's code"
import pandas as pd
Airbnb_data = pd.read_csv("data3/Airbnb_listings_cleaned.csv")
Airbnb_data['sa2_code'] = None
print(Airbnb_data)


#__________________________________________________________________________________________________________________________________________________________
"Daniel's code"






#__________________________________________________________________________________________________________________________________________________________
"Lincoln's code"
Tencancy_data = pd.read_csv("data3/tenancy_cleaned.csv")

# Creates a date and quarter in Airbnb:
Airbnb_data["date"] = pd.to_datetime(
    Airbnb_data[["year", "month"]].assign(day=1)
)

Airbnb_data["quarter"] = Airbnb_data["date"].dt.to_period("Q")

# Convert Tenancy_data timeframe to datetime 
Tencancy_data["TimeFrame"] = pd.to_datetime(Tencancy_data["TimeFrame"],
    dayfirst=True
)

Tencancy_data["quarter"] = Tencancy_data["TimeFrame"].dt.to_period("Q")

# merging columns
merged_dataset = pd.merge(Airbnb_data, Tencancy_data,
    left_on=["sa2code", "quarter"],
    right_on=["Location Id", "quarter"],
    how="left"
)

#__________________________________________________________________________________________________________________________________________________________
"Ean's code"






#__________________________________________________________________________________________________________________________________________________________
"Pallima's code"
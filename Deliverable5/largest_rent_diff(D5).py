import pandas as pd
rental_data = pd.read_csv("Deliverable5/input_data/Airbnb_bond_joined_final.csv")
rental_data['price difference'] = None

mapping = pd.read_csv("Deliverable5/input_data/geographic-areas-table-2023.csv")

week_days = 7

## Joins airbnb dataset with geographic areas table to get the SA3 code for each SA2 code in the airbnb dataset.

mapping_unique = mapping[
    ["SA22023_code", "SA32023_code"]
].drop_duplicates(subset="SA22023_code")

rental_with_sa3 = rental_data.merge(
    mapping_unique,
    left_on="sa2_code",
    right_on="SA22023_code",
    how="left"
)

print("Number of rows in rental_with_sa3:", len(rental_with_sa3)) ## Checks for potential issues with the join operation

rental_with_sa3 = rental_with_sa3.drop(columns=["SA22023_code"])

## Calculates the price difference between the Airbnb weekly rent and the Geometric Mean Rent

for index, row in rental_with_sa3.iterrows():
    sa2_code = row['sa2_code']
    if pd.notnull(row['SA32023_code']) and pd.notnull(row['Geometric Mean Rent']):
        airbnb_weekly_rent = row['price'] * week_days
        rental_with_sa3.at[index, 'price difference'] = airbnb_weekly_rent - row['Geometric Mean Rent']

## Checks for potential issues with the price difference calculation

print("Number of rows in rental_with_sa3 with price differences:", len(rental_with_sa3[rental_with_sa3['price difference'].notnull()]))

## Calculates the maximum price difference for each SA3 code

sa3_code_list = rental_with_sa3['SA32023_code'].unique().tolist()
sa3_code_list.sort()
rental_drop_nan = rental_with_sa3.dropna(subset=['price difference'])

max_diff = 0
sa3_with_max_diff = None

for sa3_code in sa3_code_list:
    sa3_data = rental_drop_nan[rental_drop_nan['SA32023_code'] == sa3_code]
    if len(sa3_data) > 0:
        max_diff_row = sa3_data.loc[sa3_data['price difference'].idxmax()]
        print(f"SA3 Code: {sa3_code}, Max Price Difference: {max_diff_row['price difference']}, Airbnb Price: {max_diff_row['price']}, Geometric Mean Rent: {max_diff_row['Geometric Mean Rent']}")
        if max_diff_row['price difference'] > max_diff:
            max_diff = max_diff_row['price difference']
            sa3_with_max_diff = sa3_code

print(f"SA3 Code with the largest price difference: {sa3_with_max_diff}, Max Price Difference: {max_diff}")

## Saves price difference data to a CSV file for further analysis

output_file = ("Deliverable5/output_data/listings_sa3.csv")
rental_drop_nan.to_csv(output_file,index=False)
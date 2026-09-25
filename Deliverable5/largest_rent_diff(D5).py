import pandas as pd
joined_data = pd.read_csv("Deliverable5/input_data/Airbnb_bond_joined_final.csv")
joined_data['price difference'] = None

mapping = pd.read_csv("Deliverable5/input_data/geographic-areas-table-2023.csv")

mapping_unique = mapping[
    ["SA22023_code", "SA32023_code"]
].drop_duplicates(subset="SA22023_code")

joined_sa3 = joined_data.merge(
    mapping_unique,
    left_on="sa2_code",
    right_on="SA22023_code",
    how="left"
)

print("Number of rows in joined_sa3:", len(joined_sa3))

joined_sa3 = joined_sa3.drop(columns=["SA22023_code"])

for index, row in joined_sa3.iterrows():
    sa2_code = row['sa2_code']
    if pd.notnull(row['SA32023_code']) and pd.notnull(row['Geometric Mean Rent']):
        airbnb_weekly_rent = row['price'] * 7
        joined_sa3.at[index, 'price difference'] = airbnb_weekly_rent - row['Geometric Mean Rent']

print("Number of rows in joined_sa3 with price differences:", len(joined_sa3[joined_sa3['price difference'].notnull()]))

list_sa3 = joined_sa3['SA32023_code'].unique().tolist()
list_sa3.sort()
joined_nan_drop = joined_sa3.dropna(subset=['price difference'])

max_diff = 0
big_dif_sa3 = None

for sa3_code in list_sa3:
    sa3_data = joined_nan_drop[joined_nan_drop['SA32023_code'] == sa3_code]
    if len(sa3_data) > 0:
        max_diff_row = sa3_data.loc[sa3_data['price difference'].idxmax()]
        print(f"SA3 Code: {sa3_code}, Max Price Difference: {max_diff_row['price difference']}, Airbnb Price: {max_diff_row['price']}, Geometric Mean Rent: {max_diff_row['Geometric Mean Rent']}")
        if max_diff_row['price difference'] > max_diff:
            max_diff = max_diff_row['price difference']
            big_dif_sa3 = sa3_code

print(f"SA3 Code with the largest price difference: {big_dif_sa3}, Max Price Difference: {max_diff}")

output_file = ("Deliverable5/output_data/listings_sa3.csv")
joined_nan_drop.to_csv(output_file,index=False)
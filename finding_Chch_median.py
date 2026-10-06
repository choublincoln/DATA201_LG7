import pandas as pd
joined_data = pd.read_csv("data3/listings_sa3.csv")

chch_data = joined_data[joined_data['sa2_code'] == 326600]

chch_median = chch_data['price'].median()
print(f"Median price for Christchurch Central is: {chch_median}")
import pandas as pd

df = pd.read_csv("Deliverable5/input_data/Airbnb_bond_joined_final.csv")
print(df.columns)
central = df[df["sa2_code"] == 326600]

central.head()
median_price = central["price"].median()

print("Median Airbnb price in Christchurch Central:", median_price)
central_summary = central[
    [
        "neighbourhood",
        "sa2_code",
        "price"
    ]
]

central_summary.head(10)
central_summary.to_csv(
    "Deliverable5/output_data/Christchurch_Central_Airbnb_prices.csv",
    index=False
)

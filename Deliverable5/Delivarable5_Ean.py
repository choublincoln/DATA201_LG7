import pandas as pd
import matplotlib.pyplot as plt


# Load the joined dataset
joined = pd.read_csv(
    "Deliverable5/input_data/Airbnb_bond_joined_final.csv",
    dtype={"id": "string", "sa2_code": "string"}
)


# Clean the location codes
joined["sa2_code"] = joined["sa2_code"].str.strip()


# Count unique Airbnb properties in each location for each quarter
airbnb_counts = (
    joined
    .groupby(["year", "quarter", "sa2_code"])
    .agg(Airbnb_Count=("id", "nunique"))
    .reset_index()
)


# Get the number of active long-term rentals in each location
# Active Bonds is repeated for Airbnb rows in the same area,
# so only one value is needed
rental_counts = (
    joined
    .dropna(subset=["Active Bonds"])
    .groupby(["year", "quarter", "sa2_code"])
    .agg(Rental_Count=("Active Bonds", "first"))
    .reset_index()
)


# Combine Airbnb and rental counts
comparison = pd.merge(
    airbnb_counts,
    rental_counts,
    on=["year", "quarter", "sa2_code"],
    how="left"
)


# Only keep locations where rental data is available
comparison_available = comparison.dropna(
    subset=["Rental_Count"]
).copy()


# Show the comparison
print("\n===================================")
print("AIRBNB VS LONG-TERM RENTALS")
print("===================================")

print(comparison_available.head(20))


# Find the latest quarter in the dataset
latest_year = comparison_available["year"].max()

latest_quarter = (
    comparison_available[
        comparison_available["year"] == latest_year
    ]["quarter"].max()
)


# Keep only the latest quarter
latest_comparison = comparison_available[
    (comparison_available["year"] == latest_year)
    & (comparison_available["quarter"] == latest_quarter)
].copy()


# Sort locations by number of Airbnbs
latest_comparison = latest_comparison.sort_values(
    "Airbnb_Count",
    ascending=False
)


# Show the top 15 locations
top_locations = latest_comparison.head(15)

print("\n===================================")
print(f"TOP LOCATIONS - {latest_year} Q{latest_quarter}")
print("===================================")

print(top_locations)


# Create the comparison graph
top_locations.plot(
    x="sa2_code",
    y=["Airbnb_Count", "Rental_Count"],
    kind="bar",
    figsize=(12, 6)
)

plt.title(
    f"Airbnb vs Long-Term Rentals by Location "
    f"({latest_year} Q{latest_quarter})"
)

plt.xlabel("SA2 Location Code")
plt.ylabel("Number of Properties")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
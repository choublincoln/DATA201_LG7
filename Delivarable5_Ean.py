import pandas as pd
import matplotlib.pyplot as plt


# Load the joined Airbnb and tenancy dataset
joined = pd.read_csv(
    "data3/Airbnb_bond_joined_final.csv",
    dtype={"id": "string", "sa2_code": "string"}
)


# Count unique Airbnb listings in each location and month
airbnb_counts = (
    joined
    .groupby(["sa2_code", "time"])
    .agg(Airbnb_Count=("id", "nunique"))
    .reset_index()
)


# Get one long-term rental count for each location and month
# Active Bonds is repeated for every Airbnb row in the same location,
# so we only take the first value instead of adding them together
rental_counts = (
    joined
    .groupby(["sa2_code", "time"])
    .agg(Rental_Count=("Active Bonds", "first"))
    .reset_index()
)


# Combine the Airbnb and rental counts
comparison = pd.merge(
    airbnb_counts,
    rental_counts,
    on=["sa2_code", "time"],
    how="left"
)


# Show the comparison table
print("\n===================================")
print("AIRBNB VS LONG-TERM RENTALS")
print("===================================")

print(comparison.head(20))


# Only use months where rental data is available
available_months = (
    comparison
    .dropna(subset=["Rental_Count"])["time"]
    .unique()
)

latest_month = max(available_months)

print("\nLatest month with both datasets:", latest_month)


# Keep the latest month that has both Airbnb and rental information
latest_comparison = comparison[
    comparison["time"] == latest_month
].copy()


# Sort by number of Airbnbs
latest_comparison = latest_comparison.sort_values(
    "Airbnb_Count",
    ascending=False
)


# Show the top 15 locations
top_locations = latest_comparison.head(15)

print("\n===================================")
print(f"TOP LOCATIONS - {latest_month}")
print("===================================")

print(top_locations)


# Plot Airbnb and long-term rental counts
top_locations.plot(
    x="sa2_code",
    y=["Airbnb_Count", "Rental_Count"],
    kind="bar",
    figsize=(12, 6)
)

plt.title(
    f"Airbnb vs Long-Term Rentals by Location ({latest_month})"
)

plt.xlabel("SA2 Location Code")
plt.ylabel("Number of Properties")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
# =========================================================
# PALLIMA'S DELIVERABLE 5
# CHRISTCHURCH CENTRAL AIRBNB PRICE ANALYSIS
# =========================================================

import pandas as pd

# =========================================================
# 1. LOAD THE FINAL JOINED DATASET
# =========================================================

# Load the final Airbnb and rental bond joined dataset
df = pd.read_csv("output_data/Deliverable5_output/Airbnb_bond_joined_final.csv", dtype={"id": "string"})

# Check the available columns
print("Available columns:")
print(df.columns)


# =========================================================
# 2. KEEP UNIQUE AIRBNB LISTINGS
# =========================================================

# Sort the Airbnb data by year and month to identify the latest snapshot
month_order = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

df["month_number"] = df["month"].map(month_order)
df = df.sort_values(["year", "month_number"])

# Keep only the latest record for each Airbnb listing
df = df.drop_duplicates(subset="id", keep="last").copy()

# Check the number of unique listings
print("\nNumber of unique Airbnb listings:", df["id"].nunique())


# =========================================================
# 3. IDENTIFY CHRISTCHURCH CENTRAL
# =========================================================

# Christchurch Central has SA2 code 326600
central = df[df["sa2_code"].astype("string").str.strip() == "326600"].copy()


# Check the filtered data
print("\nFirst 5 Christchurch Central records:")
print(central.head())


# =========================================================
# 4. SANITY CHECK
# =========================================================

# Check the number of Christchurch Central listings
print("\nNumber of Christchurch Central listings:", len(central))

# Confirm that only the required SA2 code is present
print("\nSA2 code(s) in the filtered data:", central["sa2_code"].unique())


# =========================================================
# 5. CALCULATE THE MEDIAN AIRBNB PRICE
# =========================================================

# Convert Airbnb prices to numeric values
central["price"] = pd.to_numeric(central["price"], errors="coerce")

# Calculate the median Airbnb price using unique listings
median_price = central["price"].median()

print("\nMedian Airbnb price in Christchurch Central:", median_price)


# =========================================================
# 6. PREPARE THE OUTPUT
# =========================================================

# Select the variables required for the output
central_summary = central[["neighbourhood", "sa2_code", "price"]].copy()


# Check the output
print("\nChristchurch Central summary:")
print(central_summary.head(10))


# =========================================================
# 7. SAVE THE OUTPUT
# =========================================================

# Save the Christchurch Central results
output_file = ("output_data/Deliverable5_output/Christchurch_Central_Airbnb_prices.csv")

central_summary.to_csv(output_file, index=False)

print("\nChristchurch Central Airbnb price results "
      "saved successfully.")

print(f"Saved to: {output_file}")
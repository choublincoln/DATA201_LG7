# =========================================================
# PALLIMA'S DELIVERABLE 5
# CHRISTCHURCH CENTRAL AIRBNB PRICE ANALYSIS
# =========================================================

import pandas as pd


# =========================================================
# 1. LOAD THE FINAL JOINED DATASET
# =========================================================

# Load the final Airbnb and rental bond joined dataset
df = pd.read_csv(
    "Deliverable5/input_data/Airbnb_bond_joined_final.csv"
)

# Check the available columns
print("Available columns:")
print(df.columns)


# =========================================================
# 2. IDENTIFY CHRISTCHURCH CENTRAL
# =========================================================

# Christchurch Central has SA2 code 326600
central = df[
    df["sa2_code"] == 326600
].copy()


# Check the filtered data
print("\nFirst 5 Christchurch Central records:")
print(central.head())


# =========================================================
# 3. SANITY CHECK
# =========================================================

# Check the number of Christchurch Central listings
print(
    "\nNumber of Christchurch Central listings:",
    len(central)
)

# Confirm that only the required SA2 code is present
print(
    "\nSA2 code(s) in the filtered data:",
    central["sa2_code"].unique()
)


# =========================================================
# 4. CALCULATE THE MEDIAN AIRBNB PRICE
# =========================================================

# Calculate the median Airbnb price for Christchurch Central
median_price = central["price"].median()

print(
    "\nMedian Airbnb price in Christchurch Central:",
    median_price
)


# =========================================================
# 5. PREPARE THE OUTPUT
# =========================================================

# Select the variables required for the output
central_summary = central[
    [
        "neighbourhood",
        "sa2_code",
        "price"
    ]
].copy()


# Check the output
print("\nChristchurch Central summary:")
print(central_summary.head(10))


# =========================================================
# 6. SAVE THE OUTPUT
# =========================================================

# Save the Christchurch Central results
central_summary.to_csv(
    "Deliverable5/output_data/Christchurch_Central_Airbnb_prices.csv",
    index=False
)

print(
    "\nChristchurch Central Airbnb price results "
    "saved successfully."
)
import pandas as pd

"""Lincoln's code: Joining the Airbnb and Bonds datasets"""

# =========================================================
# 1. LOAD DATASETS
# =========================================================

"""Load the cleaned Airbnb and Tenancy Services datasets."""
airbnb = pd.read_csv(
    "Deliverable5/input_data/Airbnb_listings_sa2.csv",
    dtype={"id": "string"}
)

bond = pd.read_csv(
    "Deliverable5/input_data/tenancy_cleaned.csv"
)


# =========================================================
# 2. PREPARE AREA CODES
# =========================================================

"""Convert both area-code columns to strings so they can be matched consistently between the two datasets."
strip() removes any extra whitespace. Rename Location Id so both datasets use the same column name for the area code."""

airbnb["sa2_code"] = airbnb["sa2_code"].astype("string").str.strip()
bond["Location Id"] = bond["Location Id"].astype("string").str.strip()
bond = bond.rename(columns={"Location Id": "sa2_code"})


# =========================================================
# 3. CREATE AIRBNB TIME COLUMN
# =========================================================

"""Convert each Airbnb month into its corresponding quarter so it can be matched with the bond data."""

quarterly = {
    "January": 1,
    "February": 1,
    "March": 1,
    "April": 2,
    "May": 2,
    "June": 2,
    "July": 3,
    "August": 3,
    "September": 3,
    "October": 4,
    "November": 4,
    "December": 4
}

airbnb["quarter"] = airbnb["month"].map(quarterly)


# =========================================================
# 4. CREATE BOND TIME COLUMN
# =========================================================

"""Map each Tenancy Services reporting date to its corresponding quarter. 
   Check that the TimeFrame values have been converted
   to the expected quarter values."""

bond_quarterly = {
    "2025-10-01": 4,
    "2026-01-01": 1,
    "2026-04-01": 2
}

bond["TimeFrame"] = bond["TimeFrame"].astype("string")
bond["quarter"] = bond["TimeFrame"].map(bond_quarterly)

print(bond["TimeFrame"].head())
print(bond["quarter"].head())


# =========================================================
# 5. FILTER BOND DATA
# =========================================================

"""Keep only the overall rental statistics:
# - All dwelling types
# - All numbers of beds
This prevents more specific categories from being
included in the join."""

bond_all = bond[
    (bond["Dwelling Type"] == "ALL") &
    (bond["Number Of Beds"] == "ALL")
].copy()


# =========================================================
# 6. CHECK FOR DUPLICATES
# =========================================================

"""Check for duplicate SA2 and quarter combinations.
Duplicates could cause Airbnb rows to be duplicated
when the datasets are joined."""

duplicates = bond_all.duplicated(
    subset=["sa2_code", "quarter"]
).sum()

print("===================================")
print("BOND DATA CHECK")
print("===================================")

print(f"Bond rows after filtering: {len(bond_all):,}")
print(f"Duplicate SA2 + quarter combinations: {duplicates:,}")


# =========================================================
# 7. JOIN AIRBNB AND BOND DATA
# =========================================================

"""Use a left join so all Airbnb listings are retained.
Matching bond information is added where the SA2 code
and quarter are the same in both datasets."""

joined = pd.merge(
    airbnb,
    bond_all,
    on=["sa2_code", "quarter"],
    how="left"
)


# =========================================================
# 8. CHECK JOIN RESULTS
# =========================================================

print("\n===================================")
print("JOIN RESULTS")
print("===================================")

"""Compare the number of rows before and after the join
   to check for unexpected changes. Count Airbnb observations 
   that successfully matched with a bond median rent value."""

print(f"Airbnb rows before join: {len(airbnb):,}")
print(f"Rows after join: {len(joined):,}")


matched = joined["Median Rent"].notna().sum()
unmatched = joined["Median Rent"].isna().sum()

print(f"Matched Airbnb rows: {matched:,}")
print(f"Unmatched Airbnb rows: {unmatched:,}")


# =========================================================
# 9. SHOW FIRST 5 ROWS
# =========================================================

"""Display the first five rows to visually check
   that the joined dataset looks correct."""

print("\n===================================")
print("FIRST 5 ROWS")
print("===================================")

print(joined.head())


# =========================================================
# 10. SAVE FINAL DATASET
# =========================================================

output_file = "Deliverable5/output_data/Airbnb_bond_joined_final.csv"

"""Save the final joined dataset without the pandas index."""
joined.to_csv(output_file, index=False)

"""Save the prepared bond dataset for testing/reference."""
bond.to_csv(
    "Deliverable5/input_data/tenancy_cleaned_test.csv",
    index=False
)


# =========================================================
# 11. DONE
# =========================================================

print("\n===================================")
print("DONE!")
print("===================================")

print(f"Saved to: {output_file}")
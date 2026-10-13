import pandas as pd
import pyreadr

"""Lincoln's code: Joining the Airbnb and Bonds datasets"""


# =========================================================
# 1. LOAD DATASETS
# =========================================================

"""Load the cleaned Airbnb and Tenancy Services datasets."""

airbnb_result = pyreadr.read_r(
    "output_data/Airbnb_listings_sa2.rds"
)

airbnb_data = next(
    iter(airbnb_result.values())
)


bond_result = pyreadr.read_r(
    "output_data/tenancy_cleaned.rds"
)

bond_data = next(
    iter(bond_result.values())
)


# =========================================================
# 2. PREPARE AREA CODES
# =========================================================

"""
Convert both area-code columns to strings so they can be
matched consistently between the two datasets.

strip() removes any extra whitespace.

Rename Location Id so both datasets use the same column
name for the area code.
"""

airbnb_data["sa2_code"] = (
    airbnb_data["sa2_code"]
    .astype("string")
    .str.strip()
)

bond_data["Location Id"] = (
    bond_data["Location Id"]
    .astype("string")
    .str.strip()
)

bond_data = bond_data.rename(
    columns={
        "Location Id": "sa2_code"
    }
)


# =========================================================
# 3. CREATE AIRBNB TIME COLUMN
# =========================================================

"""
Convert each Airbnb month into its corresponding quarter
so it can be matched with the bond data.
"""

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

airbnb_data["quarter"] = (
    airbnb_data["month"].map(quarterly)
)


# =========================================================
# 4. CREATE BOND TIME COLUMN
# =========================================================

"""
Map each Tenancy Services reporting date to its
corresponding quarter.

Check that the TimeFrame values have been converted
to the expected quarter values.
"""

bond_quarterly = {
    "2025-10-01": 4,
    "2026-01-01": 1,
    "2026-04-01": 2
}

bond_data["TimeFrame"] = (
    bond_data["TimeFrame"]
    .astype("string")
)

bond_data["quarter"] = (
    bond_data["TimeFrame"]
    .map(bond_quarterly)
)


print(
    bond_data["TimeFrame"].head()
)

print(
    bond_data["quarter"].head()
)


# =========================================================
# 5. FILTER BOND DATA
# =========================================================

"""
Keep only the overall rental statistics:

- All dwelling types
- All numbers of beds

This prevents more specific categories from being
included in the join.
"""

bond_data_aggregate = bond_data[
    (bond_data["Dwelling Type"] == "ALL") &
    (bond_data["Number Of Beds"] == "ALL")
].copy()


# =========================================================
# 6. CHECK FOR DUPLICATES
# =========================================================

"""
Check for duplicate SA2 and quarter combinations.

Duplicates could cause Airbnb rows to be duplicated
when the datasets are joined.
"""

duplicates = (
    bond_data_aggregate
    .duplicated(
        subset=[
            "sa2_code",
            "quarter"
        ]
    )
    .sum()
)


print(
    "==================================="
)

print(
    "BOND DATA CHECK"
)

print(
    "==================================="
)


print(
    f"Bond rows after filtering: "
    f"{len(bond_data_aggregate):,}"
)

print(
    f"Duplicate SA2 + quarter combinations: "
    f"{duplicates:,}"
)


# =========================================================
# 7. JOIN AIRBNB AND BOND DATA
# =========================================================

"""
Use a left join so all Airbnb listings are retained.

Matching bond information is added where the SA2 code
and quarter are the same in both datasets.
"""

joined = pd.merge(
    airbnb_data,
    bond_data_aggregate,
    on=[
        "sa2_code",
        "quarter"
    ],
    how="left"
)


# =========================================================
# 8. CHECK JOIN RESULTS
# =========================================================

print(
    "\n==================================="
)

print(
    "JOIN RESULTS"
)

print(
    "==================================="
)


"""
Compare the number of rows before and after the join
to check for unexpected changes.

Count Airbnb observations that successfully matched
with a bond median rent value.
"""

print(
    f"Airbnb rows before join: "
    f"{len(airbnb_data):,}"
)

print(
    f"Rows after join: "
    f"{len(joined):,}"
)


matched = (
    joined["Median Rent"]
    .notna()
    .sum()
)

unmatched = (
    joined["Median Rent"]
    .isna()
    .sum()
)


print(
    f"Matched Airbnb rows: "
    f"{matched:,}"
)

print(
    f"Unmatched Airbnb rows: "
    f"{unmatched:,}"
)


# =========================================================
# 9. SHOW FIRST 5 ROWS
# =========================================================

"""
Display the first five rows to visually check
that the joined dataset looks correct.
"""

print(
    "\n==================================="
)

print(
    "FIRST 5 ROWS"
)

print(
    "==================================="
)


print(
    joined.head()
)


# =========================================================
# 10. SAVE FINAL DATASET
# =========================================================

output_file = (
    "output_data/Airbnb_bond_joined_final.rds"
)


"""
Convert pandas nullable values to standard Python None
so pyreadr can write the dataframe correctly.
"""

joined = joined.astype(object).where(
    pd.notna(joined),
    None
)


"""
Save the final joined dataset as an RDS file.
"""

pyreadr.write_rds(
    output_file,
    joined
)


# =========================================================
# 11. DONE
# =========================================================

print(
    "\n==================================="
)

print(
    "DONE!"
)

print(
    "==================================="
)

print(
    f"Saved to: {output_file}"
)
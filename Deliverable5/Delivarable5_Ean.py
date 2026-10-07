import pandas as pd
import pyreadr
import matplotlib.pyplot as plt


# =========================================================
# 1. LOAD JOINED DATASET
# =========================================================

"""
Load the final Airbnb and Tenancy Services joined dataset.

The dataset contains Airbnb listings from October 2025
to August 2026, with Airbnb SA2 codes and quarterly
Tenancy Services rental information.
"""

joined_result = pyreadr.read_r(
    "output_data/Airbnb_bond_joined_final.rds"
)

joined = next(
    iter(joined_result.values())
)


# =========================================================
# 2. CLEAN AREA CODES
# =========================================================

"""
Convert the SA2 codes to strings and remove any
unnecessary whitespace.
"""

joined["sa2_code"] = (
    joined["sa2_code"]
    .astype("string")
    .str.strip()
)


# =========================================================
# 3. LOAD SA2 TO SA3 MAPPING
# =========================================================

"""
Load the Stats NZ geographic mapping that links each
SA2 code to its corresponding SA3 code and SA3 name.
"""

area_mapping = pd.read_csv(
    "input_data/sa2_to_sa3.csv",
    dtype={
        "sa2_code": "string",
        "sa3_code": "string"
    }
)


area_mapping["sa2_code"] = (
    area_mapping["sa2_code"]
    .str.strip()
)

area_mapping["sa3_code"] = (
    area_mapping["sa3_code"]
    .str.strip()
)


# =========================================================
# 4. ADD SA3 INFORMATION
# =========================================================

"""
Match each Airbnb SA2 code to its corresponding SA3
code and SA3 name.
"""

joined = pd.merge(
    joined,
    area_mapping[
        [
            "sa2_code",
            "sa3_code",
            "sa3_name"
        ]
    ],
    on="sa2_code",
    how="left"
)


# =========================================================
# 5. CHECK SA3 MAPPING
# =========================================================

"""
Check whether all Airbnb SA2 areas were successfully
matched to an SA3 area.
"""

unmatched_sa3 = (
    joined["sa3_code"]
    .isna()
    .sum()
)

print("\n===================================")
print("SA3 MAPPING CHECK")
print("===================================")

print(
    f"Airbnb rows without an SA3 match: "
    f"{unmatched_sa3:,}"
)


# =========================================================
# 6. COUNT AIRBNB PROPERTIES BY SA3
# =========================================================

"""
Count unique Airbnb properties in each SA3 area
for each quarter.

Using nunique() prevents the same Airbnb property
from being counted more than once.
"""

airbnb_counts = (
    joined
    .groupby(
        [
            "year",
            "quarter",
            "sa3_code",
            "sa3_name"
        ]
    )
    .agg(
        Airbnb_Count=("id", "nunique")
    )
    .reset_index()
)


# =========================================================
# 7. GET LONG-TERM RENTAL COUNTS
# =========================================================

"""
Get the number of active long-term rental bonds in
each SA3 area for each quarter.

The same Active Bonds value is repeated across Airbnb
rows within an area, so only the first value is used.
"""

rental_counts = (
    joined
    .dropna(subset=["Active Bonds"])
    .groupby(
        [
            "year",
            "quarter",
            "sa3_code",
            "sa3_name"
        ]
    )
    .agg(
        Rental_Count=("Active Bonds", "first")
    )
    .reset_index()
)


# =========================================================
# 8. COMBINE AIRBNB AND RENTAL COUNTS
# =========================================================

"""
Combine the Airbnb and long-term rental counts using
the SA3 area and quarter as the matching variables.
"""

comparison = pd.merge(
    airbnb_counts,
    rental_counts,
    on=[
        "year",
        "quarter",
        "sa3_code",
        "sa3_name"
    ],
    how="left"
)


# =========================================================
# 9. KEEP AREAS WITH RENTAL DATA
# =========================================================

comparison_available = comparison.dropna(
    subset=["Rental_Count"]
).copy()


# =========================================================
# 10. SHOW COMPARISON
# =========================================================

print("\n===================================")
print("AIRBNB VS LONG-TERM RENTALS")
print("===================================")

print(
    comparison_available.head(20)
)


# =========================================================
# 11. FIND LATEST QUARTER
# =========================================================

"""
Find the latest year and quarter available in the
joined dataset.
"""

latest_year = (
    comparison_available["year"].max()
)

latest_quarter = (
    comparison_available[
        comparison_available["year"] == latest_year
    ]["quarter"].max()
)


# =========================================================
# 12. KEEP LATEST QUARTER
# =========================================================

latest_comparison = comparison_available[
    (comparison_available["year"] == latest_year)
    &
    (comparison_available["quarter"] == latest_quarter)
].copy()


# =========================================================
# 13. SORT SA3 AREAS
# =========================================================

"""
Sort SA3 areas by the number of Airbnb properties.
"""

latest_comparison = (
    latest_comparison
    .sort_values(
        "Airbnb_Count",
        ascending=False
    )
)


# =========================================================
# 14. SELECT TOP SA3 AREAS
# =========================================================

"""
Select the top 15 SA3 areas so the graph remains
readable and the area names fit on the x-axis.
"""

top_locations = (
    latest_comparison
    .head(15)
)


print("\n===================================")
print(
    f"TOP SA3 AREAS - "
    f"{latest_year} Q{latest_quarter}"
)
print("===================================")

print(
    top_locations[
        [
            "sa3_code",
            "sa3_name",
            "Airbnb_Count",
            "Rental_Count"
        ]
    ]
)


# =========================================================
# 15. CREATE COMPARISON GRAPH
# =========================================================

"""
Create a bar chart comparing Airbnb properties with
long-term rentals across the top SA3 areas.

SA3 names are used instead of SA2 codes so the graph
is easier to interpret.
"""

ax = top_locations.plot(
    x="sa3_name",
    y=[
        "Airbnb_Count",
        "Rental_Count"
    ],
    kind="bar",
    figsize=(12, 6)
)


plt.title(
    f"Airbnb vs Long-Term Rentals by SA3 "
    f"({latest_year} Q{latest_quarter})"
)

plt.xlabel("SA3 Area")

plt.ylabel(
    "Number of Properties"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()


plt.savefig(
    "output_data/airbnb_vs_rentals_sa3.png",
    bbox_inches="tight",
    dpi=300
)

plt.show()
import pandas as pd
import pyreadr
import matplotlib.pyplot as plt


# =========================================================
# 1. LOAD DATA
# =========================================================

joined_result = pyreadr.read_r(
    "output_data/Airbnb_bond_joined_final.rds"
)

joined = next(iter(joined_result.values()))


# =========================================================
# 2. CLEAN SA2 CODES
# =========================================================

joined["sa2_code"] = (
    joined["sa2_code"]
    .astype("string")
    .str.strip()
)


# =========================================================
# 3. LOAD SA2 TO SA3 MAPPING
# =========================================================

mapping = pd.read_csv(
    "input_data/geographic-areas-table-2023.csv"
)

mapping["SA22023_code"] = (
    mapping["SA22023_code"]
    .astype("string")
    .str.strip()
)

mapping["SA32023_code"] = (
    mapping["SA32023_code"]
    .astype("string")
    .str.strip()
)


# =========================================================
# 4. FIND SA3 NAME COLUMN
# =========================================================

possible_name_columns = [
    "SA32023_name",
    "SA32023_name_ascii",
    "SA32023",
]

sa3_name_column = next(
    (
        column
        for column in possible_name_columns
        if column in mapping.columns
    ),
    None
)

if sa3_name_column is None:
    raise ValueError(
        "Could not find an SA3 name column. "
        "Available columns are: "
        + ", ".join(mapping.columns)
    )


# =========================================================
# 5. KEEP UNIQUE SA2 TO SA3 MAPPING
# =========================================================

mapping_unique = mapping[
    [
        "SA22023_code",
        "SA32023_code",
        sa3_name_column
    ]
].drop_duplicates(
    subset="SA22023_code"
)

mapping_unique = mapping_unique.rename(
    columns={
        sa3_name_column: "sa3_name"
    }
)


# =========================================================
# 6. JOIN SA3 INFORMATION
# =========================================================

joined = pd.merge(
    joined,
    mapping_unique,
    left_on="sa2_code",
    right_on="SA22023_code",
    how="left"
)

joined = joined.drop(
    columns=["SA22023_code"]
)


# =========================================================
# 7. COUNT AIRBNB LISTINGS
# =========================================================

airbnb_counts = (
    joined
    .groupby(
        [
            "year",
            "quarter",
            "SA32023_code",
            "sa3_name"
        ],
        dropna=False
    )
    .agg(
        Airbnb_Count=("id", "nunique")
    )
    .reset_index()
)


# =========================================================
# 8. COUNT RENTAL BONDS
# =========================================================

rental_counts = (
    joined
    .groupby(
        [
            "year",
            "quarter",
            "SA32023_code",
            "sa3_name"
        ],
        dropna=False
    )
    .agg(
        Rental_Count=("Active Bonds", "first")
    )
    .reset_index()
)


# =========================================================
# 9. COMBINE AIRBNB AND RENTAL COUNTS
# =========================================================

comparison = pd.merge(
    airbnb_counts,
    rental_counts,
    on=[
        "year",
        "quarter",
        "SA32023_code",
        "sa3_name"
    ],
    how="inner"
)


# =========================================================
# 10. SELECT Q2 2026
# =========================================================

latest_quarter = comparison[
    (comparison["year"] == 2026) &
    (comparison["quarter"] == 2)
].copy()


# =========================================================
# 11. SELECT TOP 15 SA3 AREAS
# =========================================================

top_locations = (
    latest_quarter
    .sort_values(
        "Airbnb_Count",
        ascending=False
    )
    .head(15)
)


# =========================================================
# 12. CREATE GRAPH
# =========================================================

ax = top_locations.plot(
    x="sa3_name",
    y=[
        "Airbnb_Count",
        "Rental_Count"
    ],
    kind="bar",
    figsize=(12, 6)
)

ax.set_xlabel("SA3 Area")
ax.set_ylabel("Number of Listings / Rental Bonds")

ax.set_title(
    "Airbnb Listings vs Rental Bonds by SA3 - Q2 2026"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()


# =========================================================
# 13. SAVE GRAPH
# =========================================================

plt.savefig(
    "output_data/airbnb_vs_rentals_sa3.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
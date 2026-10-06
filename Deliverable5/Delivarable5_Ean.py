import pandas as pd
import matplotlib.pyplot as plt
import pyreadr

from pathlib import Path


# File locations
INPUT_DIR = Path("input_data")
OUTPUT_DIR = Path("output_data")

AIRBNB_FILE = OUTPUT_DIR / "airbnb_cleaned.rds"
TENANCY_FILE = OUTPUT_DIR / "tenancy_cleaned.rds"

COMPARISON_FILE = OUTPUT_DIR / "airbnb_vs_rentals_sa3.rds"
GRAPH_FILE = OUTPUT_DIR / "airbnb_vs_rentals_sa3.png"


# Read an RDS file and return the dataframe
def read_rds(file_path):
    result = pyreadr.read_r(str(file_path))
    return next(iter(result.values()))


# Load cleaned data from the previous deliverables
airbnb = read_rds(AIRBNB_FILE)
bond = read_rds(TENANCY_FILE)


# Find the geographic areas table in input_data
geo_files = [
    file for file in INPUT_DIR.glob("*.csv")
    if "geographic" in file.name.lower()
    and "area" in file.name.lower()
]

if len(geo_files) == 0:
    raise FileNotFoundError(
        "Geographic Areas Table CSV was not found in input_data."
    )


# Prefer the 2026 version if it is available
geo_2026 = [
    file for file in geo_files
    if "2026" in file.name
]

if geo_2026:
    geo_file = geo_2026[0]
else:
    geo_file = geo_files[0]
    print(
        "Warning: using a geographic areas table that is not labelled 2026."
    )


print("Using geographic lookup:", geo_file)

geo = pd.read_csv(
    geo_file,
    dtype="string"
)


# Find the SA2 code column
sa2_candidates = [
    col for col in geo.columns
    if "SA2" in col.upper()
    and "NAME" not in col.upper()
]

# Find the SA3 code column
sa3_candidates = [
    col for col in geo.columns
    if "SA3" in col.upper()
    and "NAME" not in col.upper()
]

# Find the SA3 name column
sa3_name_candidates = [
    col for col in geo.columns
    if "SA3" in col.upper()
    and "NAME" in col.upper()
    and "ASCII" not in col.upper()
]


if not sa2_candidates:
    raise ValueError("SA2 code column could not be found.")

if not sa3_candidates:
    raise ValueError("SA3 code column could not be found.")

if not sa3_name_candidates:
    raise ValueError("SA3 name column could not be found.")


sa2_column = sa2_candidates[0]
sa3_column = sa3_candidates[0]
sa3_name_column = sa3_name_candidates[0]


print("SA2 column:", sa2_column)
print("SA3 column:", sa3_column)
print("SA3 name column:", sa3_name_column)


# Create a simple SA2 to SA3 lookup table
geo_lookup = (
    geo[
        [
            sa2_column,
            sa3_column,
            sa3_name_column
        ]
    ]
    .rename(
        columns={
            sa2_column: "sa2_code",
            sa3_column: "sa3_code",
            sa3_name_column: "sa3_name"
        }
    )
    .drop_duplicates()
)


# Clean the location codes so they match
airbnb["sa2_code"] = (
    airbnb["sa2_code"]
    .astype("string")
    .str.replace(r"\.0$", "", regex=True)
    .str.strip()
)

bond["Location Id"] = (
    bond["Location Id"]
    .astype("string")
    .str.replace(r"\.0$", "", regex=True)
    .str.strip()
)

bond = bond.rename(
    columns={"Location Id": "sa2_code"}
)

geo_lookup["sa2_code"] = (
    geo_lookup["sa2_code"]
    .astype("string")
    .str.replace(r"\.0$", "", regex=True)
    .str.strip()
)


# Create quarter for Airbnb data if it does not already exist
if "quarter" not in airbnb.columns:

    month_numbers = {
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

    airbnb["month_number"] = airbnb["month"].map(
        month_numbers
    )

    airbnb["quarter"] = (
        ((airbnb["month_number"] - 1) // 3) + 1
    )


# Create year and quarter for tenancy data
if "quarter" not in bond.columns:

    bond["TimeFrame"] = pd.to_datetime(
        bond["TimeFrame"],
        errors="coerce"
    )

    bond["year"] = bond["TimeFrame"].dt.year
    bond["quarter"] = bond["TimeFrame"].dt.quarter


# Keep the overall rental figures
bond_all = bond[
    (bond["Dwelling Type"].astype(str).str.upper() == "ALL")
    &
    (bond["Number Of Beds"].astype(str).str.upper() == "ALL")
].copy()


# Add SA3 information to Airbnb data
airbnb = pd.merge(
    airbnb,
    geo_lookup,
    on="sa2_code",
    how="left"
)


# Add SA3 information to tenancy data
bond_all = pd.merge(
    bond_all,
    geo_lookup,
    on="sa2_code",
    how="left"
)


# Sanity check for locations that did not match
print("\n===================================")
print("SA3 MAPPING CHECK")
print("===================================")

print(
    "Airbnb rows without SA3:",
    airbnb["sa3_code"].isna().sum()
)

print(
    "Tenancy rows without SA3:",
    bond_all["sa3_code"].isna().sum()
)


# Count unique Airbnb properties in each SA3
airbnb_counts = (
    airbnb
    .dropna(subset=["sa3_code"])
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


# Make sure each SA2 is counted once per quarter
bond_sa2 = (
    bond_all
    .dropna(
        subset=[
            "sa3_code",
            "Active Bonds"
        ]
    )
    .drop_duplicates(
        subset=[
            "year",
            "quarter",
            "sa2_code"
        ]
    )
)


# Add together the rental properties from all SA2 areas
# that belong to the same SA3 area
rental_counts = (
    bond_sa2
    .groupby(
        [
            "year",
            "quarter",
            "sa3_code",
            "sa3_name"
        ]
    )
    .agg(
        Rental_Count=("Active Bonds", "sum")
    )
    .reset_index()
)


# Combine Airbnb and rental counts
comparison = pd.merge(
    airbnb_counts,
    rental_counts,
    on=[
        "year",
        "quarter",
        "sa3_code",
        "sa3_name"
    ],
    how="inner"
)


# Show the complete comparison
print("\n===================================")
print("AIRBNB VS LONG-TERM RENTALS - SA3")
print("===================================")

print(comparison)


# Find the latest period shared by both datasets
latest_period = (
    comparison[
        ["year", "quarter"]
    ]
    .drop_duplicates()
    .sort_values(
        ["year", "quarter"]
    )
    .iloc[-1]
)

latest_year = latest_period["year"]
latest_quarter = latest_period["quarter"]


# Keep the latest quarter
latest_comparison = comparison[
    (comparison["year"] == latest_year)
    &
    (comparison["quarter"] == latest_quarter)
].copy()


# Sort the graph from highest to lowest Airbnb count
latest_comparison = (
    latest_comparison
    .sort_values(
        "Airbnb_Count",
        ascending=False
    )
)


print("\n===================================")
print(
    f"LATEST COMPARISON - "
    f"{latest_year} Q{int(latest_quarter)}"
)
print("===================================")

print(
    latest_comparison[
        [
            "sa3_name",
            "Airbnb_Count",
            "Rental_Count"
        ]
    ]
)


# Save the comparison as an RDS output
pyreadr.write_rds(
    str(COMPARISON_FILE),
    comparison
)


# Create the SA3 comparison graph
latest_comparison.plot(
    x="sa3_name",
    y=[
        "Airbnb_Count",
        "Rental_Count"
    ],
    kind="bar",
    figsize=(16, 8)
)

plt.title(
    f"Airbnb vs Long-Term Rentals by SA3 Area "
    f"({latest_year} Q{int(latest_quarter)})"
)

plt.xlabel("SA3 Area")
plt.ylabel("Number of Properties")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

# Save graph for the automated report
plt.savefig(
    GRAPH_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nSaved:")
print(COMPARISON_FILE)
print(GRAPH_FILE)
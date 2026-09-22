import pandas as pd

"Lincoln's code (Joining the Datasets Airbnb and Bonds)"

# # =========================================================
# # 1. LOAD DATASETS
# # =========================================================

airbnb = pd.read_csv("data3/Airbnb_listings_sa2.csv", dtype={"id": "string"})
bond = pd.read_csv("data3/tenancy_cleaned.csv")

# # =========================================================
# # 2. PREPARE AREA CODES
# # =========================================================

# # Make both area-code columns text
airbnb["sa2_code"] = (airbnb["sa2_code"].astype("string").str.strip())

bond["Location Id"] = (bond["Location Id"].astype("string").str.strip())

# # Rename Location Id so both datasets use sa2_code
bond = bond.rename(columns={"Location Id": "sa2_code"})

# # =========================================================
# # 3. CREATE AIRBNB TIME COLUMN
# # =========================================================

month_numbers = {"January": 1,"February": 2,"March": 3,"April": 4,"May": 5,"June": 6,
                "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

airbnb["month_number"] = (airbnb["month"].map(month_numbers))
airbnb["time"] = (airbnb["year"].astype(str)+ "-" + airbnb["month_number"].astype("Int64").astype(str).str.zfill(2))

# # =========================================================
# # 4. CREATE BOND TIME COLUMN
# # =========================================================

bond["TimeFrame"] = pd.to_datetime(bond["TimeFrame"], errors="coerce")
bond["time"] = (bond["TimeFrame"].dt.strftime("%Y-%m").astype("string"))

# # =========================================================
# # 5. FILTER BOND DATA
# # =========================================================

# # Keep only the overall rental statistics:
# # - All dwelling types
# # - All numbers of beds

bond_all = bond[(bond["Dwelling Type"] == "ALL") & (bond["Number Of Beds"] == "ALL")].copy()

# # =========================================================
# # 6. CHECK FOR DUPLICATES
# # =========================================================

duplicates = bond_all.duplicated(subset=["sa2_code", "time"]).sum()

print("===================================")
print("BOND DATA CHECK")
print("===================================")

print(f"Bond rows after filtering: "f"{len(bond_all):,}")
print(f"Duplicate SA2 + time combinations: "f"{duplicates:,}")

# # =========================================================
# # 7. JOIN AIRBNB AND BOND DATA
# # =========================================================

joined = pd.merge(airbnb, bond_all, on=["sa2_code", "time"], how="left")

# # =========================================================
# # 8. CHECK JOIN RESULTS
# # =========================================================

print("\n===================================")
print("JOIN RESULTS")
print("===================================")

print(f"Airbnb rows before join: "f"{len(airbnb):,}")

print(f"Rows after join: "f"{len(joined):,}")

# # Check how many Airbnb observations matched
matched = joined["Median Rent"].notna().sum()
unmatched = joined["Median Rent"].isna().sum()

print(f"Matched Airbnb rows: "f"{matched:,}")

print(f"Unmatched Airbnb rows: "f"{unmatched:,}")

# # =========================================================
# # 9. SHOW FIRST 5 ROWS
# # =========================================================

print("\n===================================")
print("FIRST 5 ROWS")
print("===================================")

print(joined.head())

# # =========================================================
# # 10. SAVE FINAL DATASET
# # =========================================================

output_file = ("data3/Airbnb_bond_joined_final.csv")
joined.to_csv(output_file, index=False)

# # =========================================================
# # 11. DONE
# # =========================================================

print("\n===================================")
print("DONE!")
print("===================================")

print(f"Saved to: {output_file}")
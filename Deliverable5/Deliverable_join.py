import pandas as pd

"Lincoln's code (Joining the Datasets Airbnb and Bonds)"

# # =========================================================
# # 1. LOAD DATASETS
# # =========================================================

airbnb = pd.read_csv("Deliverable5/input_data/Airbnb_listings_sa2.csv", dtype={"id": "string"})
bond = pd.read_csv("Deliverable5/input_data/tenancy_cleaned.csv")

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


quarterly = {"January": 1,"February": 1,"March": 1,"April": 2,"May": 2,"June": 2,
                "July": 3, "August": 3, "September": 3, "October": 4, "November": 4, "December": 4}

airbnb["quarter"] = (airbnb["month"].map(quarterly))

# # =========================================================
# # 4. CREATE BOND TIME COLUMN
# # =========================================================

bond_quarterly = {"2025-10-01": 4, "2026-01-01": 1,"2026-04-01": 2}
bond["TimeFrame"] = bond["TimeFrame"].astype("string")
bond["quarter"] = (bond["TimeFrame"].map(bond_quarterly))

print(bond["TimeFrame"].head())
print(bond["quarter"].head())

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

duplicates = bond_all.duplicated(subset=["sa2_code", "quarter"]).sum()

print("===================================")
print("BOND DATA CHECK")
print("===================================")

print(f"Bond rows after filtering: "f"{len(bond_all):,}")
print(f"Duplicate SA2 + quarter combinations: "f"{duplicates:,}")

# # =========================================================
# # 7. JOIN AIRBNB AND BOND DATA
# # =========================================================

joined = pd.merge(airbnb, bond_all, on=["sa2_code", "quarter"], how="left")

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

# final_data = joined.drop(columns="quarter")

output_file = ("Deliverable5/output_data/Airbnb_bond_joined_final.csv")
joined.to_csv(output_file, index=False)

bond.to_csv("Deliverable5/input_data/tenancy_cleaned_test.csv", index=False)

# # =========================================================
# # 11. DONE
# # =========================================================

print("\n===================================")
print("DONE!")
print("===================================")

print(f"Saved to: {output_file}")
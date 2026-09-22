import pandas as pd
airbnb_data = pd.read_csv("data3/Airbnb_listings_cleaned.csv")
airbnb_data['sa2_code'] = None

"Daniel's code"
import requests
import multiprocessing
import time

# =========================================================
# 1. LOAD AIRBNB DATA
# =========================================================

airbnb_data = pd.read_csv("data3/Airbnb_listings_cleaned.csv", dtype={"id": "string"})

# =========================================================
# 2. API DETAILS
# =========================================================

API_KEY = "6bc49b9afc514295a2478b656738aaf8"
LAYER = 123515

API_URL = ("https://datafinder.stats.govt.nz/services/query/v1/vector.json")

# =========================================================
# 3. FUNCTION TO GET SA2 CODE
# =========================================================

def get_sa2(row):
    index, lat, lon = row
    url = (
        f"{API_URL}"
        f"?key={API_KEY}"
        f"&layer={LAYER}"
        f"&x={lon}"
        f"&y={lat}"
        f"&max_results=3"
        f"&radius=10000"
        f"&geometry=true"
        f"&with_field_names=true"
    )

    try:

        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(
                f"Row {index} FAILED | "
                f"Status: {response.status_code} | "
                f"{response.text[:100]}")

            return index, None

        data = response.json()

        # -------------------------------------------------
        # Search response for SA2 information
        # -------------------------------------------------

        def find_sa2(obj):
            if isinstance(obj, dict):
                if "SA22026_V1_00" in obj:
                    return obj

                for value in obj.values():
                    result = find_sa2(value)

                    if result is not None:
                        return result

            elif isinstance(obj, list):
                for item in obj:
                    result = find_sa2(item)

                    if result is not None:
                        return result

            return None

        properties = find_sa2(data)

        # -------------------------------------------------
        # Extract SA2 code
        # -------------------------------------------------

        if properties is not None:
            sa2_code = properties["SA22026_V1_00"]
            return index, sa2_code

        else:
            print(f"Row {index} | No SA2 found")
            return index, None


    except Exception as e:
        print(f"Row {index} | ERROR: {e}")
        return index, None

# =========================================================
# 4. RUN FULL DATASET
# =========================================================

if __name__ == "__main__":
    test_rows = [
        (i, airbnb_data.loc[i, "latitude"], airbnb_data.loc[i, "longitude"])
        for i in airbnb_data.index[:15]
    ]

    print("===================================")
    print("STARTING 15-ROW TEST")
    print("===================================")

    with multiprocessing.Pool(processes=40) as pool:
        test_results = pool.map(get_sa2, test_rows)

    # Add SA2 results to the 15 rows
    test_data = airbnb_data.iloc[:15].copy()

    for index, sa2_code in test_results:
        test_data.loc[index, "sa2_code"] = sa2_code

    # Save test file
    test_file = "data3/Airbnb_listings_sa2_TEST.csv"
    test_data.to_csv(test_file, index=False)

    print("\nTEST RESULTS")
    print("===================================")
    print(test_data[["id", "latitude", "longitude", "sa2_code"]])

    print("\nTest file saved to:")
    print(test_file)

    print("===================================")
    print("15-ROW TEST COMPLETE")
    print("===================================")


    rows = [(i, airbnb_data.loc[i, "latitude"], airbnb_data.loc[i, "longitude"])
        for i in airbnb_data.index]

    total = len(rows)
    n_p = 40 # ADJUST OF NUMBER OF PROCESSES BASED ON YOUR SYSTEM CAPABILITIES HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    print("===================================")
    print("STARTING FULL SA2 QUERY")
    print("===================================")
    print(f"Total Airbnb rows: {total:,}")
    print(f"Using {n_p} processes...")
    print()

    start_time = time.time()
    results = []

    # -----------------------------------------------------
    # Multiprocessing
    # -----------------------------------------------------
    
    with multiprocessing.Pool(processes=n_p) as pool:

        for result in pool.imap_unordered(get_sa2, rows):
            results.append(result)
            completed = len(results)


            # -------------------------------------------------
            # Progress update every 100 rows
            # -------------------------------------------------

            if completed % 100 == 0 or completed == total:
                elapsed = time.time() - start_time
                speed = completed / elapsed
                remaining = total - completed

                estimated_seconds = (remaining / speed if speed > 0 else 0)

                print(
                    f"Completed {completed:,} / {total:,} "
                    f"({completed / total * 100:.1f}%) | "
                    f"{speed:.1f} rows/sec | "
                    f"ETA: {estimated_seconds / 60:.1f} min")


    # =========================================================
    # 5. ADD RESULTS TO DATASET
    # =========================================================

    print()
    print("Adding SA2 codes to dataset...")

    for index, sa2_code in results:

        airbnb_data.loc[index, "sa2_code"] = sa2_code

    # =========================================================
    # 6. CHECK RESULTS
    # =========================================================

    successful = (airbnb_data["sa2_code"].notna().sum())
    failed = (airbnb_data["sa2_code"].isna().sum())

    print()
    print("===================================")
    print("RESULTS")
    print("===================================")

    print(f"Total rows:       {total:,}")
    print(f"Successful:       {successful:,}")
    print(f"Failed / missing: {failed:,}")

    # =========================================================
    # 7. SAVE DATASET
    # =========================================================

    output_file = ("data3/Airbnb_listings_sa2.csv")
    airbnb_data.to_csv(output_file,index=False)

    # =========================================================
    # 8. FINISH
    # =========================================================

    elapsed = time.time() - start_time
    print()
    print("===================================")
    print("DONE!")
    print("===================================")

    print(f"Saved to: {output_file}")
    print(f"Total time: {elapsed / 60:.2f} minutes")









#__________________________________________________________________________________________________________________________________________________________
"Lincoln's code (Joining the Datasets Airbnb and Bonds)"

# # =========================================================
# # 1. LOAD DATASETS
# # =========================================================

# airbnb = pd.read_csv("data3/Airbnb_listings_sa2.csv", dtype={"id": "string"})
# bond = pd.read_csv("data3/tenancy_cleaned.csv")

# # =========================================================
# # 2. PREPARE AREA CODES
# # =========================================================

# # Make both area-code columns text
# airbnb["sa2_code"] = (airbnb["sa2_code"].astype("string").str.strip())

# bond["Location Id"] = (bond["Location Id"].astype("string").str.strip())

# # Rename Location Id so both datasets use sa2_code
# bond = bond.rename(columns={"Location Id": "sa2_code"})

# # =========================================================
# # 3. CREATE AIRBNB TIME COLUMN
# # =========================================================

# month_numbers = {"January": 1,"February": 2,"March": 3,"April": 4,"May": 5,"June": 6,
#                 "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

# airbnb["month_number"] = (airbnb["month"].map(month_numbers))
# airbnb["time"] = (airbnb["year"].astype(str)+ "-" + airbnb["month_number"].astype("Int64").astype(str).str.zfill(2))

# # =========================================================
# # 4. CREATE BOND TIME COLUMN
# # =========================================================

# bond["TimeFrame"] = pd.to_datetime(bond["TimeFrame"], errors="coerce")
# bond["time"] = (bond["TimeFrame"].dt.strftime("%Y-%m").astype("string"))

# # =========================================================
# # 5. FILTER BOND DATA
# # =========================================================

# # Keep only the overall rental statistics:
# # - All dwelling types
# # - All numbers of beds

# bond_all = bond[(bond["Dwelling Type"] == "ALL") & (bond["Number Of Beds"] == "ALL")].copy()

# # =========================================================
# # 6. CHECK FOR DUPLICATES
# # =========================================================

# duplicates = bond_all.duplicated(subset=["sa2_code", "time"]).sum()

# print("===================================")
# print("BOND DATA CHECK")
# print("===================================")

# print(f"Bond rows after filtering: "f"{len(bond_all):,}")
# print(f"Duplicate SA2 + time combinations: "f"{duplicates:,}")

# # =========================================================
# # 7. JOIN AIRBNB AND BOND DATA
# # =========================================================

# joined = pd.merge(airbnb, bond_all, on=["sa2_code", "time"], how="left")

# # =========================================================
# # 8. CHECK JOIN RESULTS
# # =========================================================

# print("\n===================================")
# print("JOIN RESULTS")
# print("===================================")

# print(f"Airbnb rows before join: "f"{len(airbnb):,}")

# print(f"Rows after join: "f"{len(joined):,}")

# # Check how many Airbnb observations matched
# matched = joined["Median Rent"].notna().sum()
# unmatched = joined["Median Rent"].isna().sum()

# print(f"Matched Airbnb rows: "f"{matched:,}")

# print(f"Unmatched Airbnb rows: "f"{unmatched:,}")

# # =========================================================
# # 9. SHOW FIRST 5 ROWS
# # =========================================================

# print("\n===================================")
# print("FIRST 5 ROWS")
# print("===================================")

# print(joined.head())

# # =========================================================
# # 10. SAVE FINAL DATASET
# # =========================================================

# output_file = ("data3/Airbnb_bond_joined_final.csv")
# joined.to_csv(output_file, index=False)

# # =========================================================
# # 11. DONE
# # =========================================================

# print("\n===================================")
# print("DONE!")
# print("===================================")

# print(f"Saved to: {output_file}")














#__________________________________________________________________________________________________________________________________________________________
"Ean's code"






#__________________________________________________________________________________________________________________________________________________________
"Pallima's code"








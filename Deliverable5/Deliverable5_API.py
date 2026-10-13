# =========================================================
# DELIVERABLE 5 - UNIQUE AIRBNB LISTINGS SA2 API QUERY
# =========================================================

import os
import time
import multiprocessing
import pandas as pd
import requests
from dotenv import load_dotenv


# =========================================================
# 1. FILE PATHS AND SETTINGS
# =========================================================

input_file = "output_data/Deliverable4_output/Airbnb_listings_cleaned.csv"
unique_output_file = "output_data/Deliverable5_output/Airbnb_unique_listings_sa2.csv"
final_output_file = "output_data/Deliverable5_output/Airbnb_listings_sa2.csv"
test_output_file = "output_data/Deliverable5_output/Airbnb_unique_listings_sa2_TEST.csv"

# Number of parallel API requests
N_PROCESSES = 40
os.makedirs("output_data/Deliverable5_output", exist_ok=True)


# =========================================================
# 2. API DETAILS
# =========================================================

load_dotenv()
API_KEY = os.getenv("DATAFINDER_API_KEY")
LAYER = 123515
API_URL = ("https://datafinder.stats.govt.nz/services/query/v1/vector.json")

if not API_KEY:
    raise ValueError("DATAFINDER_API_KEY was not found. "
                     "Check that your .env file contains the API key.")


# =========================================================
# 3. FUNCTION TO FIND SA2 CODE IN API RESPONSE
# =========================================================

def find_sa2(obj):
    """Recursively search an API response for the SA2 field."""

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


# =========================================================
# 4. FUNCTION TO QUERY SA2 CODE
# =========================================================

def get_sa2(row):
    """Query the Stats NZ DataFinder API for one listing."""

    listing_id, lat, lon = row

    if pd.isna(lat) or pd.isna(lon):
        print(f"Listing {listing_id} | Missing coordinates", flush=True)
        return listing_id, None

    params = {
        "key": API_KEY,
        "layer": LAYER,
        "x": lon,
        "y": lat,
        "max_results": 3,
        "radius": 10000,
        "geometry": "true",
        "with_field_names": "true"
    }

    max_retries = 5

    for attempt in range(max_retries):
        try:
            response = requests.get(API_URL, params=params, timeout=20)

            if response.status_code == 200:
                data = response.json()
                properties = find_sa2(data)

                if properties is not None:
                    sa2_code = properties.get("SA22026_V1_00")

                    if sa2_code is not None:
                        return listing_id, sa2_code

                print(f"Listing {listing_id} | No SA2 found", flush=True)
                return listing_id, None

            elif response.status_code == 429:
                retry_after = response.headers.get("Retry-After")

                if retry_after is not None:
                    try:
                        wait_time = float(retry_after)
                    except ValueError:
                        wait_time = 2 ** (attempt + 1)
                else:
                    wait_time = 2 ** (attempt + 1)

                print(f"Listing {listing_id} | Rate limited | "
                      f"Waiting {wait_time:.1f}s...", flush=True)

                time.sleep(wait_time)

            elif response.status_code >= 500:
                wait_time = 2 ** (attempt + 1)

                print(f"Listing {listing_id} | Server error "
                      f"{response.status_code} | "
                      f"Retrying in {wait_time}s...", flush=True)

                time.sleep(wait_time)

            else:
                print(f"Listing {listing_id} FAILED | "
                      f"Status: {response.status_code} | "
                      f"{response.text[:100]}", flush=True)

                return listing_id, None

        except requests.exceptions.RequestException as error:
            wait_time = 2 ** (attempt + 1)

            print(f"Listing {listing_id} | Request error: {error} | "
                  f"Retrying in {wait_time}s...", flush=True)

            time.sleep(wait_time)

    print(f"Listing {listing_id} | "
          f"Failed after {max_retries} attempts", flush=True)

    return listing_id, None


# =========================================================
# 5. RUN API QUERIES WITH MULTIPROCESSING
# =========================================================

def process_listings(unique_listings, rows, test_mode=False):
    """Process listings and print progress checkpoints."""

    total = len(rows)

    if total == 0:
        print("No listings require API queries.")
        return unique_listings

    n_processes = min(N_PROCESSES, total)

    if test_mode:
        checkpoint_interval = 5
    else:
        checkpoint_interval = max(1, min(500, total // 20))

    print("===================================")
    print("STARTING API QUERIES")
    print("===================================")
    print(f"Listings to query: {total:,}")
    print(f"Processes: {n_processes}")
    print(f"Checkpoint interval: {checkpoint_interval:,} listings")
    print()

    start_time = time.time()
    results = []

    with multiprocessing.Pool(processes=n_processes) as pool:
        for completed, result in enumerate(
                pool.imap_unordered(get_sa2, rows), start=1):

            results.append(result)

            if completed % checkpoint_interval == 0 or completed == total:
                percentage = completed / total * 100

                print(f"Checkpoint: {completed:,} / {total:,} listings "
                      f"completed ({percentage:.1f}%)", flush=True)

    results_df = pd.DataFrame(results, columns=["id", "sa2_code"])
    results_df["id"] = results_df["id"].astype("string")
    result_mapping = results_df.set_index("id")["sa2_code"]
    matching = unique_listings["id"].isin(result_mapping.index)

    unique_listings.loc[matching, "sa2_code"] = (
        unique_listings.loc[matching, "id"].map(result_mapping)
    )

    elapsed = time.time() - start_time

    print(f"Completed {total:,} queries.")
    print(f"Elapsed time: {elapsed:.1f} seconds.")

    if test_mode:
        print("15-listing test completed.")

    return unique_listings


# =========================================================
# 6. MAIN SCRIPT
# =========================================================

if __name__ == "__main__":

    # =====================================================
    # 6A. LOAD AIRBNB DATA
    # =====================================================

    airbnb_data = pd.read_csv(input_file, dtype={"id": "string"})
    required_columns = ["id", "latitude", "longitude"]

    missing_columns = [column for column in required_columns if column not in airbnb_data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # =====================================================
    # 6B. CREATE UNIQUE LISTINGS DATAFRAME
    # =====================================================

    unique_listings = (airbnb_data[["id", "latitude", "longitude"]].drop_duplicates(subset=["id"]).copy().reset_index(drop=True))

    unique_listings["sa2_code"] = pd.Series([None] * len(unique_listings), dtype="object")

    print("===================================")
    print("UNIQUE AIRBNB LISTINGS")
    print("===================================")
    print(f"Full Airbnb rows: {len(airbnb_data):,}")
    print(f"Unique listing IDs: {len(unique_listings):,}")
    print("===================================")

    # =====================================================
    # 6C. LOAD EXISTING RESULTS IF AVAILABLE
    # =====================================================

    if os.path.exists(unique_output_file):

        previous_mapping = pd.read_csv(unique_output_file, dtype={"id": "string"})

        if {"id", "sa2_code"}.issubset(previous_mapping.columns):

            previous_mapping = (previous_mapping[["id", "sa2_code"]].drop_duplicates(subset=["id"], keep="last"))
            previous_codes = previous_mapping.set_index("id")["sa2_code"]

            unique_listings["sa2_code"] = (unique_listings["id"].map(previous_codes))

            print("Loaded previously saved SA2 codes. "
                  "Listings with existing codes will be skipped.")

    # =====================================================
    # 6D. RUN A 15-LISTING TEST
    # =====================================================

    remaining_listings = unique_listings[unique_listings["sa2_code"].isna()].copy()

    if len(remaining_listings) > 0:

        test_rows_df = remaining_listings.head(15)
        test_rows = [(row.id, row.latitude, row.longitude) for row in test_rows_df.itertuples(index=False)]

        print()
        print("===================================")
        print("STARTING 15-LISTING TEST")
        print("===================================")

        unique_listings = process_listings(unique_listings, test_rows, test_mode=True)

        test_mapping = unique_listings[unique_listings["id"].isin(test_rows_df["id"])][["id", "sa2_code"]].copy()
        test_mapping.to_csv(test_output_file, index=False)

        print(f"Test results saved to: {test_output_file}")

    # =====================================================
    # 6E. QUERY REMAINING UNIQUE LISTINGS
    # =====================================================

    remaining_listings = unique_listings[unique_listings["sa2_code"].isna()].copy()
    rows = [(row.id, row.latitude, row.longitude) for row in remaining_listings.itertuples(index=False)]

    if len(rows) > 0:

        print()
        print("===================================")
        print("QUERYING REMAINING LISTINGS")
        print("===================================")

        unique_listings = process_listings(unique_listings, rows)

    else:
        print("All unique listings already have SA2 codes.")

    # =====================================================
    # 7. CHECK RESULTS
    # =====================================================

    successful = unique_listings["sa2_code"].notna().sum()
    failed = unique_listings["sa2_code"].isna().sum()

    print()
    print("===================================")
    print("UNIQUE LISTING RESULTS")
    print("===================================")
    print(f"Unique listings: {len(unique_listings):,}")
    print(f"Successful SA2 codes: {successful:,}")
    print(f"Missing SA2 codes: {failed:,}")

    # =====================================================
    # 8. SAVE UNIQUE LISTING MAPPING
    # =====================================================

    unique_listings.to_csv(unique_output_file, index=False)
    print(f"Unique mapping saved to: {unique_output_file}")

    # =====================================================
    # 9. JOIN SA2 CODES BACK TO FULL AIRBNB DATA
    # =====================================================

    sa2_mapping = (unique_listings[["id", "sa2_code"]].drop_duplicates(subset=["id"], keep="last"))
    airbnb_data = airbnb_data.drop(columns=["sa2_code"], errors="ignore")

    airbnb_final = airbnb_data.merge(sa2_mapping, on="id", how="left", validate="many_to_one")

    # =====================================================
    # 10. SAVE FINAL DATASET
    # =====================================================

    airbnb_final.to_csv(final_output_file, index=False)

    print()
    print("===================================")
    print("DONE!")
    print("===================================")
    print(f"Unique mapping saved to: {unique_output_file}")
    print(f"Full Airbnb dataset saved to: {final_output_file}")
    print(f"Full Airbnb rows: {len(airbnb_final):,}")

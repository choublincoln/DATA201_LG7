# =========================================================
# DELIVERABLE 5 - UNIQUE AIRBNB LISTINGS SA2 API QUERY
# =========================================================

import os
import time
import multiprocessing
import pandas as pd
import requests
import pyreadr
from dotenv import load_dotenv


# =========================================================
# 1. FILE PATHS
# =========================================================

input_file = "output_data/Airbnb_listings_cleaned.rds"

unique_output_file = (
    "output_data/Airbnb_unique_listings_sa2.rds"
)

final_output_file = "output_data/Airbnb_listings_sa2.rds"

test_output_file = (
    "output_data/Airbnb_unique_listings_sa2_TEST.rds"
)


# =========================================================
# 2. API DETAILS
# =========================================================

load_dotenv()

API_KEY = os.getenv("DATAFINDER_API_KEY")

LAYER = 123515

API_URL = (
    "https://datafinder.stats.govt.nz/services/query/v1/vector.json"
)

if not API_KEY:
    raise ValueError(
        "DATAFINDER_API_KEY was not found. "
        "Check that your .env file contains the API key."
    )


# =========================================================
# 3. FUNCTION TO GET SA2 CODE
# =========================================================

def get_sa2(row):
    """Query the Stats NZ Datafinder API for one unique listing."""

    listing_id, lat, lon = row

    # -----------------------------------------------------
    # Check for missing coordinates
    # -----------------------------------------------------

    if pd.isna(lat) or pd.isna(lon):

        print(f"Listing {listing_id} | Missing coordinates")

        return listing_id, None

    # -----------------------------------------------------
    # Construct API URL
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Retry settings
    # -----------------------------------------------------

    max_retries = 5
    data = None

    for attempt in range(max_retries):

        try:

            response = requests.get(
                url,
                timeout=10
            )

            # ---------------------------------------------
            # Successful response
            # ---------------------------------------------

            if response.status_code == 200:

                data = response.json()
                break

            # ---------------------------------------------
            # Rate limited
            # ---------------------------------------------

            elif response.status_code == 429:

                retry_after = response.headers.get(
                    "Retry-After"
                )

                if retry_after is not None:
                    wait_time = float(retry_after)
                else:
                    wait_time = 2 ** attempt

                print(
                    f"Listing {listing_id} | "
                    f"Rate limited | "
                    f"Waiting {wait_time:.1f}s..."
                )

                time.sleep(wait_time)

            # ---------------------------------------------
            # Other API errors
            # ---------------------------------------------

            else:

                print(
                    f"Listing {listing_id} FAILED | "
                    f"Status: {response.status_code} | "
                    f"{response.text[:100]}"
                )

                return listing_id, None

        except requests.exceptions.RequestException as error:

            wait_time = 2 ** attempt

            print(
                f"Listing {listing_id} | "
                f"Request error: {error} | "
                f"Retrying in {wait_time}s..."
            )

            time.sleep(wait_time)

    else:

        print(
            f"Listing {listing_id} | "
            f"Failed after {max_retries} attempts"
        )

        return listing_id, None

    if data is None:
        return listing_id, None

    # =====================================================
    # SEARCH RESPONSE FOR SA2
    # =====================================================

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

    properties = find_sa2(data)

    # =====================================================
    # EXTRACT SA2 CODE
    # =====================================================

    if properties is not None:

        sa2_code = properties.get("SA22026_V1_00")

        return listing_id, sa2_code

    else:

        print(f"Listing {listing_id} | No SA2 found")

        return listing_id, None


# =========================================================
# 4. MAIN SCRIPT
# =========================================================

if __name__ == "__main__":

    # =====================================================
    # 4A. LOAD AIRBNB DATA
    # =====================================================

    airbnb_result = pyreadr.read_r(input_file)
    airbnb_data = next(iter(airbnb_result.values()))

    # Ensure listing IDs are treated as text.
    airbnb_data["id"] = airbnb_data["id"].astype("string")

    # =====================================================
    # 4B. CREATE UNIQUE LISTINGS DATAFRAME
    # =====================================================

    # Keep one row per unique listing ID and its coordinates.
    unique_listings = (
        airbnb_data[["id", "latitude", "longitude"]]
        .drop_duplicates(subset=["id"])
        .copy()
        .reset_index(drop=True)
    )

    # Create a column to store the SA2 codes.
    unique_listings["sa2_code"] = pd.Series(
        [None] * len(unique_listings),
        dtype="object"
    )

    # Print dataset summary once.
    print("===================================")
    print("UNIQUE AIRBNB LISTINGS")
    print("===================================")
    print(f"Full Airbnb rows:       {len(airbnb_data):,}")
    print(f"Unique listing IDs:     {len(unique_listings):,}")
    print("===================================")

    # =====================================================
    # 4C. CHECK HOW MUCH DATA REMAINS
    # =====================================================

    remaining_listings = unique_listings[
        unique_listings["sa2_code"].isna()
    ].copy()

    total_unique = len(unique_listings)
    total_remaining = len(remaining_listings)

    print()
    print("===================================")
    print("UNIQUE LISTING SA2 API")
    print("===================================")
    print(f"Unique listings:       {total_unique:,}")
    print(f"Remaining to query:    {total_remaining:,}")
    print("===================================")

    # =====================================================
    # 4D. RUN API QUERIES
    # =====================================================

    if total_remaining == 0:

        print("No listings require API queries.")

    else:

        # -------------------------------------------------
        # 4D(i). RUN A 15-LISTING TEST
        # -------------------------------------------------

        test_rows = remaining_listings.head(15)

        test_inputs = [
            (row.id, row.latitude, row.longitude)
            for row in test_rows.itertuples(index=False)
        ]

        print()
        print("===================================")
        print("STARTING 15-LISTING TEST")
        print("===================================")

        with multiprocessing.Pool(
            processes=min(40, max(1, len(test_inputs)))
        ) as pool:

            test_results = pool.map(
                get_sa2,
                test_inputs
            )

        test_mapping = pd.DataFrame(
            test_results,
            columns=["id", "sa2_code"]
        )

        test_mapping["id"] = (
            test_mapping["id"].astype("string")
        )

        # Add test results to the unique listings dataframe.
        test_codes = test_mapping.set_index("id")["sa2_code"]

        test_mask = unique_listings["id"].isin(
            test_codes.index
        )

        unique_listings.loc[test_mask, "sa2_code"] = (
            unique_listings.loc[test_mask, "id"].map(test_codes)
        )

        # Save the test results.
        pyreadr.write_rds(
            test_output_file,
            test_mapping
        )

        print(f"Test mapping saved to: {test_output_file}")
        print("15-listing test complete.")

        # -------------------------------------------------
        # 4D(ii). PREPARE REMAINING UNIQUE LISTINGS
        # -------------------------------------------------

        # Keep successful test results.
        # Query only listings that still lack SA2 codes.
        remaining_listings = unique_listings[
            unique_listings["sa2_code"].isna()
        ].copy()

        rows = [
            (row.id, row.latitude, row.longitude)
            for row in remaining_listings.itertuples(index=False)
        ]

        total = len(rows)
        n_processes = min(40, max(1, total))

        # -------------------------------------------------
        # 4D(iii). RUN FULL API QUERY
        # -------------------------------------------------

        if total > 0:

            print()
            print("===================================")
            print("STARTING REMAINING API QUERIES")
            print("===================================")
            print(f"Unique listings remaining: {total:,}")
            print(f"Using {n_processes} processes...")
            print()

            start_time = time.time()
            completed = 0

            with multiprocessing.Pool(
                processes=n_processes
            ) as pool:

                for listing_id, sa2_code in pool.imap_unordered(
                    get_sa2,
                    rows
                ):

                    # Update the corresponding listing by ID.
                    matching = (
                        unique_listings["id"] == listing_id
                    )

                    unique_listings.loc[
                        matching,
                        "sa2_code"
                    ] = sa2_code

                    completed += 1

                    # -------------------------------------
                    # Report progress every 100 rows
                    # -------------------------------------

                    if completed % 100 == 0 or completed == total:

                        elapsed = time.time() - start_time

                        speed = (
                            completed / elapsed
                            if elapsed > 0
                            else 0
                        )

                        remaining = total - completed

                        eta_seconds = (
                            remaining / speed
                            if speed > 0
                            else 0
                        )

                        print(
                            f"Completed {completed:,} / "
                            f"{total:,} "
                            f"({completed / total * 100:.1f}%) | "
                            f"{speed:.1f} listings/sec | "
                            f"ETA: {eta_seconds / 60:.1f} min"
                        )

    # =====================================================
    # 5. CHECK RESULTS
    # =====================================================

    successful = unique_listings["sa2_code"].notna().sum()
    failed = unique_listings["sa2_code"].isna().sum()

    print()
    print("===================================")
    print("UNIQUE LISTING RESULTS")
    print("===================================")
    print(f"Unique listings:       {len(unique_listings):,}")
    print(f"Successful SA2 codes:  {successful:,}")
    print(f"Missing SA2 codes:     {failed:,}")

    # =====================================================
    # 6. SAVE UNIQUE LISTING MAPPING
    # =====================================================

    pyreadr.write_rds(
        unique_output_file,
        unique_listings
    )

    print(f"Unique mapping saved to: {unique_output_file}")

    # =====================================================
    # 7. JOIN SA2 CODES BACK TO FULL AIRBNB DATA
    # =====================================================

    # Keep only the listing ID and its SA2 code for the join.
    sa2_mapping = unique_listings[
        ["id", "sa2_code"]
    ].drop_duplicates(
        subset=["id"],
        keep="last"
    )

    # Remove any previous SA2 column before joining.
    airbnb_data = airbnb_data.drop(
        columns=["sa2_code"],
        errors="ignore"
    )

    # Each listing can match only one mapping row.
    airbnb_final = airbnb_data.merge(
        sa2_mapping,
        on="id",
        how="left",
        validate="many_to_one"
    )

    # =====================================================
    # 8. SAVE FINAL DATASET
    # =====================================================

    pyreadr.write_rds(
        final_output_file,
        airbnb_final
    )

    print()
    print("===================================")
    print("DONE!")
    print("===================================")
    print(f"Unique mapping saved to: {unique_output_file}")
    print(f"Full Airbnb dataset saved to: {final_output_file}")
    print(f"Full Airbnb rows: {len(airbnb_final):,}")

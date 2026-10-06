# =========================================================
# DELIVERABLE 5 - AIRBNB SA2 API QUERY
# =========================================================

import pandas as pd
import requests
import multiprocessing
import time
import os
import pyreadr
from dotenv import load_dotenv


# =========================================================
# 1. LOAD CLEANED AIRBNB DATA
# =========================================================

input_file = (
    "output_data/Airbnb_listings_cleaned.rds"
)

checkpoint_file = (
    "output_data/Airbnb_listings_sa2_checkpoint.rds"
)

airbnb_result = pyreadr.read_r(
    input_file
)

airbnb_data = next(
    iter(airbnb_result.values())
)


# =========================================================
# 2. LOAD PREVIOUS CHECKPOINT IF IT EXISTS
# =========================================================

if os.path.exists(checkpoint_file):

    print("===================================")
    print("CHECKPOINT FOUND")
    print("===================================")

    print(
        "Loading previous API progress..."
    )

    checkpoint_result = pyreadr.read_r(
        checkpoint_file
    )

    airbnb_data = next(
        iter(checkpoint_result.values())
    )

    print(
        "Previous progress loaded."
    )

else:

    print(
        "No checkpoint found."
    )

    # Create SA2 column for first run
    airbnb_data["sa2_code"] = None


# Ensure Airbnb ID is treated as text
airbnb_data["id"] = airbnb_data["id"].astype("string")


# Make sure SA2 column exists
if "sa2_code" not in airbnb_data.columns:

    airbnb_data["sa2_code"] = None


# =========================================================
# 3. API DETAILS
# =========================================================

load_dotenv()

API_KEY = os.getenv(
    "DATAFINDER_API_KEY"
)

LAYER = 123515

API_URL = (
    "https://datafinder.stats.govt.nz/services/query/v1/vector.json"
)


# =========================================================
# 4. FUNCTION TO GET SA2 CODE
# =========================================================

def get_sa2(row):

    index, lat, lon = row


    # -----------------------------------------------------
    # Check for missing coordinates
    # -----------------------------------------------------

    if pd.isna(lat) or pd.isna(lon):

        print(
            f"Row {index} | Missing coordinates"
        )

        return index, None


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


    for attempt in range(max_retries):

        try:

            response = requests.get(
                url,
                timeout=10
            )


            # =============================================
            # SUCCESS
            # =============================================

            if response.status_code == 200:

                data = response.json()

                break


            # =============================================
            # RATE LIMITED
            # =============================================

            elif response.status_code == 429:

                retry_after = (
                    response.headers.get(
                        "Retry-After"
                    )
                )


                if retry_after is not None:

                    wait_time = float(
                        retry_after
                    )

                else:

                    wait_time = 2 ** attempt


                print(
                    f"Row {index} | "
                    f"Rate limited | "
                    f"Waiting {wait_time:.1f}s..."
                )


                time.sleep(
                    wait_time
                )


            # =============================================
            # OTHER API ERROR
            # =============================================

            else:

                print(
                    f"Row {index} FAILED | "
                    f"Status: "
                    f"{response.status_code} | "
                    f"{response.text[:100]}"
                )

                return index, None


        except requests.exceptions.RequestException as e:

            wait_time = 2 ** attempt


            print(
                f"Row {index} | "
                f"Request error: {e} | "
                f"Retrying in "
                f"{wait_time}s..."
            )


            time.sleep(
                wait_time
            )


    else:

        print(
            f"Row {index} | "
            f"Failed after "
            f"{max_retries} attempts"
        )

        return index, None


    # =====================================================
    # SEARCH RESPONSE FOR SA2
    # =====================================================

    def find_sa2(obj):

        if isinstance(obj, dict):

            if "SA22026_V1_00" in obj:

                return obj


            for value in obj.values():

                result = find_sa2(
                    value
                )

                if result is not None:

                    return result


        elif isinstance(obj, list):

            for item in obj:

                result = find_sa2(
                    item
                )

                if result is not None:

                    return result


        return None


    properties = find_sa2(
        data
    )


    # =====================================================
    # EXTRACT SA2 CODE
    # =====================================================

    if properties is not None:

        sa2_code = properties[
            "SA22026_V1_00"
        ]

        return index, sa2_code


    else:

        print(
            f"Row {index} | "
            f"No SA2 found"
        )

        return index, None


# =========================================================
# 5. RUN API
# =========================================================

if __name__ == "__main__":


    # =====================================================
    # 5A. CHECK HOW MUCH DATA REMAINS
    # =====================================================

    remaining_rows = [
        i
        for i in airbnb_data.index
        if pd.isna(
            airbnb_data.loc[
                i,
                "sa2_code"
            ]
        )
    ]


    total_remaining = len(
        remaining_rows
    )


    total_dataset = len(
        airbnb_data
    )


    completed_before = (
        total_dataset
        - total_remaining
    )


    print()
    print("===================================")
    print("AIRBNB SA2 API")
    print("===================================")

    print(
        f"Total dataset:     "
        f"{total_dataset:,}"
    )

    print(
        f"Already completed: "
        f"{completed_before:,}"
    )

    print(
        f"Remaining:         "
        f"{total_remaining:,}"
    )

    print("===================================")


    # =====================================================
    # 5B. STOP IF EVERYTHING IS COMPLETE
    # =====================================================

    if total_remaining == 0:

        print()
        print(
            "All rows already have SA2 codes."
        )

    else:


        # =================================================
        # 5C. 15-ROW TEST
        # =================================================

        test_indices = remaining_rows[:15]


        test_rows = [
            (
                i,
                airbnb_data.loc[
                    i,
                    "latitude"
                ],
                airbnb_data.loc[
                    i,
                    "longitude"
                ]
            )
            for i in test_indices
        ]


        print()
        print("===================================")
        print("STARTING 15-ROW TEST")
        print("===================================")


        # Use only 40 processes
        with multiprocessing.Pool(
            processes=40
        ) as pool:

            test_results = pool.map(
                get_sa2,
                test_rows
            )


        # -------------------------------------------------
        # Add test results
        # -------------------------------------------------

        test_data = airbnb_data.loc[
            test_indices
        ].copy()


        for index, sa2_code in test_results:

            test_data.loc[
                index,
                "sa2_code"
            ] = sa2_code


        # -------------------------------------------------
        # Save test file
        # -------------------------------------------------

        test_file = (
            "output_data/"
            "Airbnb_listings_sa2_TEST.rds"
        )


        pyreadr.write_rds(
            test_file,
            test_data
        )


        # -------------------------------------------------
        # Display test results
        # -------------------------------------------------

        print()
        print("TEST RESULTS")
        print("===================================")


        print(
            test_data[
                [
                    "id",
                    "latitude",
                    "longitude",
                    "sa2_code"
                ]
            ]
        )


        print()
        print(
            "Test file saved to:"
        )

        print(
            test_file
        )


        print()
        print("===================================")
        print("15-ROW TEST COMPLETE")
        print("===================================")


        # =================================================
        # 5D. PREPARE FULL DATASET
        # =================================================

        rows = [
            (
                i,
                airbnb_data.loc[
                    i,
                    "latitude"
                ],
                airbnb_data.loc[
                    i,
                    "longitude"
                ]
            )
            for i in remaining_rows
        ]


        total = len(
            rows
        )


        # Number of API processes
        n_p = 40


        print()
        print("===================================")
        print("STARTING FULL SA2 QUERY")
        print("===================================")


        print(
            f"Rows remaining: "
            f"{total:,}"
        )


        print(
            f"Using {n_p} processes..."
        )


        print()


        # =================================================
        # 5E. RUN FULL API QUERY
        # =================================================

        start_time = time.time()

        results = []


        try:

            with multiprocessing.Pool(
                processes=n_p
            ) as pool:


                for result in pool.imap_unordered(
                    get_sa2,
                    rows
                ):


                    results.append(
                        result
                    )


                    completed = len(
                        results
                    )


                    # =====================================
                    # UPDATE DATAFRAME
                    # =====================================

                    index, sa2_code = result


                    airbnb_data.loc[
                        index,
                        "sa2_code"
                    ] = sa2_code


                    # =====================================
                    # CHECKPOINT EVERY 1,000 ROWS
                    # =====================================

                    if (
                        completed % 1000 == 0
                    ):

                        pyreadr.write_rds(
                            checkpoint_file,
                            airbnb_data
                        )


                        print()
                        print(
                            "-----------------------------------"
                        )

                        print(
                            f"CHECKPOINT SAVED: "
                            f"{completed:,} / "
                            f"{total:,}"
                        )

                        print(
                            f"File: "
                            f"{checkpoint_file}"
                        )

                        print(
                            "-----------------------------------"
                        )


                    # =====================================
                    # PROGRESS EVERY 100 ROWS
                    # =====================================

                    if (
                        completed % 100 == 0
                        or completed == total
                    ):


                        elapsed = (
                            time.time()
                            - start_time
                        )


                        speed = (
                            completed
                            / elapsed
                        )


                        remaining = (
                            total
                            - completed
                        )


                        estimated_seconds = (
                            remaining / speed
                            if speed > 0
                            else 0
                        )


                        print(
                            f"Completed "
                            f"{completed:,} / "
                            f"{total:,} "
                            f"("
                            f"{completed / total * 100:.1f}%"
                            f") | "
                            f"{speed:.1f} rows/sec | "
                            f"ETA: "
                            f"{estimated_seconds / 60:.1f} min"
                        )


        except KeyboardInterrupt:

            # =============================================
            # SAVE PROGRESS IF MANUALLY STOPPED
            # =============================================

            print()
            print(
                "Script stopped manually."
            )


            print(
                "Saving current progress..."
            )


            pyreadr.write_rds(
                checkpoint_file,
                airbnb_data
            )


            print(
                f"Checkpoint saved to: "
                f"{checkpoint_file}"
            )


            raise


        # =================================================
        # 6. CHECK RESULTS
        # =================================================

        successful = (
            airbnb_data[
                "sa2_code"
            ]
            .notna()
            .sum()
        )


        failed = (
            airbnb_data[
                "sa2_code"
            ]
            .isna()
            .sum()
        )


        print()
        print("===================================")
        print("RESULTS")
        print("===================================")


        print(
            f"Total rows:       "
            f"{total_dataset:,}"
        )


        print(
            f"Successful:       "
            f"{successful:,}"
        )


        print(
            f"Failed / missing: "
            f"{failed:,}"
        )


        # =================================================
        # 7. SAVE FINAL DATASET
        # =================================================

        output_file = (
            "output_data/"
            "Airbnb_listings_sa2.rds"
        )


        pyreadr.write_rds(
            output_file,
            airbnb_data
        )


        # =================================================
        # 8. FINISH
        # =================================================

        elapsed = (
            time.time()
            - start_time
        )


        print()
        print("===================================")
        print("DONE!")
        print("===================================")


        print(
            f"Saved to: "
            f"{output_file}"
        )


        print(
            f"Total API time: "
            f"{elapsed / 60:.2f} minutes"
        )


        print()
        print(
            "Final Airbnb SA2 dataset created."
        )
"Lincoln's code"
import pandas as pd
airbnb_data = pd.read_csv("data3/Airbnb_listings_cleaned.csv")
airbnb_data['sa2_code'] = None


#__________________________________________________________________________________________________________________________________________________________
"Daniel's code"
import pandas as pd
import requests
import multiprocessing
import time


# =========================================================
# 1. LOAD AIRBNB DATA
# =========================================================

airbnb_data = pd.read_csv("data3/Airbnb_listings_cleaned.csv")

# Create SA2 column
airbnb_data["sa2_code"] = None


# =========================================================
# 2. API DETAILS
# =========================================================

API_KEY = "6bc49b9afc514295a2478b656738aaf8"
LAYER = 123515

API_URL = (
    "https://datafinder.stats.govt.nz/services/query/v1/vector.json"
)


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
                f"{response.text[:100]}"
            )

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

    rows = [
        (
            i,
            airbnb_data.loc[i, "latitude"],
            airbnb_data.loc[i, "longitude"]
        )
        for i in airbnb_data.index
    ]


    total = len(rows)

    print("===================================")
    print("STARTING FULL SA2 QUERY")
    print("===================================")
    print(f"Total Airbnb rows: {total:,}")
    print("Using 8 processes...")
    print()


    start_time = time.time()

    results = []


    # -----------------------------------------------------
    # Multiprocessing
    # -----------------------------------------------------

    with multiprocessing.Pool(processes=8) as pool:

        for result in pool.imap_unordered(
            get_sa2,
            rows
        ):

            results.append(result)

            completed = len(results)


            # -------------------------------------------------
            # Progress update every 100 rows
            # -------------------------------------------------

            if completed % 100 == 0 or completed == total:

                elapsed = time.time() - start_time

                speed = completed / elapsed

                remaining = total - completed

                estimated_seconds = (
                    remaining / speed
                    if speed > 0
                    else 0
                )


                print(
                    f"Completed {completed:,} / {total:,} "
                    f"({completed / total * 100:.1f}%) | "
                    f"{speed:.1f} rows/sec | "
                    f"ETA: {estimated_seconds / 60:.1f} min"
                )


    # =========================================================
    # 5. ADD RESULTS TO DATASET
    # =========================================================

    print()
    print("Adding SA2 codes to dataset...")


    for index, sa2_code in results:

        airbnb_data.loc[
            index,
            "sa2_code"
        ] = sa2_code


    # =========================================================
    # 6. CHECK RESULTS
    # =========================================================

    successful = (
        airbnb_data["sa2_code"].notna().sum()
    )

    failed = (
        airbnb_data["sa2_code"].isna().sum()
    )


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

    output_file = (
        "data3/Airbnb_listings_sa2.csv"
    )

    airbnb_data.to_csv(
        output_file,
        index=False
    )


    # =========================================================
    # 8. FINISH
    # =========================================================

    elapsed = time.time() - start_time

    print()
    print("===================================")
    print("DONE!")
    print("===================================")

    print(f"Saved to: {output_file}")
    print(
        f"Total time: {elapsed / 60:.2f} minutes"
    )




#__________________________________________________________________________________________________________________________________________________________
"Lincoln's code"

# Tencancy_data = pd.read_csv("data3/tenancy_cleaned.csv")

# # Creates a date and quarter in Airbnb:
# airbnb_data["date"] = pd.to_datetime(
#     airbnb_data[["year", "month"]].assign(day=1)
# )

# airbnb_data["quarter"] = airbnb_data["date"].dt.to_period("Q")

# # Convert Tenancy_data timeframe to datetime 
# Tencancy_data["TimeFrame"] = pd.to_datetime(Tencancy_data["TimeFrame"],
#     dayfirst=True
# )

# Tencancy_data["quarter"] = Tencancy_data["TimeFrame"].dt.to_period("Q")

# # merging columns
# merged_dataset = pd.merge(airbnb_data, Tencancy_data,
#     left_on=["sa2code", "quarter"],
#     right_on=["Location Id", "quarter"],
#     how="left"
# )

#__________________________________________________________________________________________________________________________________________________________
"Ean's code"






#__________________________________________________________________________________________________________________________________________________________
"Pallima's code"
"Lincoln's code"
import pandas as pd
airbnb_data = pd.read_csv("data3/Airbnb_listings_cleaned.csv")
airbnb_data['sa2_code'] = None
print(airbnb_data)


#__________________________________________________________________________________________________________________________________________________________
"Daniel's code"
import requests
import multiprocessing
import time

API_URL = "https://datafinder.stats.govt.nz/services/query/v1/vector.json"
API_KEY = "6bc49b9afc514295a2478b656738aaf8"
LAYER = 123515


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

        if response.status_code == 200:
            data = response.json()
            return index, data.get("sa2_code", None)
        else:
            return index, None

    except requests.RequestException:
        return index, None


if __name__ == "__main__":

    # Create list of rows to process
    rows = [
        (i, airbnb_data.loc[i, "latitude"], airbnb_data.loc[i, "longitude"])
        for i in range(len(airbnb_data))
    ]

    total = len(rows)

    print(f"Starting {total} API requests...")
    print("Waiting for responses...")

    start_time = time.time()

    results = []

    # Use 8 processes
    with multiprocessing.Pool(processes=8) as pool:

        for result in pool.imap_unordered(get_sa2, rows):

            results.append(result)

            completed = len(results)

            # Print progress every 100 rows
            if completed % 100 == 0 or completed == total:

                elapsed = time.time() - start_time
                speed = completed / elapsed

                remaining = total - completed
                estimated_seconds = remaining / speed if speed > 0 else 0

                print(
                    f"Completed {completed:,} / {total:,} "
                    f"({completed / total * 100:.1f}%) | "
                    f"Speed: {speed:.1f} rows/sec | "
                    f"Estimated remaining: {estimated_seconds / 60:.1f} min"
                )

    # Add results back to dataframe
    for index, sa2_code in results:
        airbnb_data.loc[index, "sa2_code"] = sa2_code

    # Save the new dataset
    airbnb_data.to_csv(
        "data3/Airbnb_listings_sa2.csv",
        index=False
    )

    elapsed = time.time() - start_time

    print("DONE!")
    print(f"Total time: {elapsed / 60:.2f} minutes")
    print("Saved to data3/Airbnb_listings_sa2.csv")





#__________________________________________________________________________________________________________________________________________________________
"Lincoln's code"
Tencancy_data = pd.read_csv("data3/tenancy_cleaned.csv")

# Creates a date and quarter in Airbnb:
airbnb_data["date"] = pd.to_datetime(
    airbnb_data[["year", "month"]].assign(day=1)
)

airbnb_data["quarter"] = airbnb_data["date"].dt.to_period("Q")

# Convert Tenancy_data timeframe to datetime 
Tencancy_data["TimeFrame"] = pd.to_datetime(Tencancy_data["TimeFrame"],
    dayfirst=True
)

Tencancy_data["quarter"] = Tencancy_data["TimeFrame"].dt.to_period("Q")

# merging columns
merged_dataset = pd.merge(airbnb_data, Tencancy_data,
    left_on=["sa2code", "quarter"],
    right_on=["Location Id", "quarter"],
    how="left"
)

#__________________________________________________________________________________________________________________________________________________________
"Ean's code"






#__________________________________________________________________________________________________________________________________________________________
"Pallima's code"
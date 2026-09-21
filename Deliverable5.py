"Lincoln's code"
import pandas as pd
airbnb_data = pd.read_csv("data3/Airbnb_listings_cleaned.csv")
airbnb_data['sa2_code'] = None


#__________________________________________________________________________________________________________________________________________________________
"Daniel's code"

import requests
import multiprocessing as mp

def fetch_sa2_code(index):
    lat = airbnb_data.loc[index, 'latitude']
    lon = airbnb_data.loc[index, 'longitude']
    url = f"https://datafinder.stats.govt.nz/services/query/v1/vector.json?key=6bc49b9afc514295a2478b656738aaf8&layer=123515&x={lon}&y={lat}&max_results=3&radius=10000&geometry=true&with_field_names=true"  # Replace with actual API endpoint
    response = requests.get(url)
        
    if response.status_code == 200:
        data = response.json()
        sa2_code = data.get('sa2_code', None)
        airbnb_data.loc[index, 'sa2_code'] = sa2_code
    else:
        print(f"Failed to retrieve SA2 code for index {index}: {response.status_code}")

pool = mp.Pool(mp.cpu_count())
results = pool.map(fetch_sa2_code, range(len(airbnb_data)))
pool.close()

if __name__ == '__main__':
    mp.freeze_support()

airbnb_data.to_csv("data3/Airbnb_listings_sa2.csv", index=False)
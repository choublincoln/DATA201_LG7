"Lincoln's code"
import pandas as pd
airbnb_data = pd.read_csv("data3/Airbnb_listings_cleaned.csv")
airbnb_data['sa2_code'] = None


#__________________________________________________________________________________________________________________________________________________________
"Daniel's code"

import requests
import multiprocessing as mp
from itertools import chain

def fetch_sa2_code(lat, lon):
    url = f"https://datafinder.stats.govt.nz/services/query/v1/vector.json?key=6bc49b9afc514295a2478b656738aaf8&layer=123515&x={lon}&y={lat}&max_results=3&radius=10000&geometry=true&with_field_names=true"  # Replace with actual API endpoint
    try:
        response = requests.get(url)
    except Exception as e:
        return {}
    if response != None and response.status_code == 200:
        jsonResponse = response.json()
        return jsonResponse
    return {}
        
def get_data_list(row):
    data_list = []
    json_data_batch = fetch_sa2_code(row['latitude'], row['longitude'])
    data_list.append(json_data_batch)
    return data_list

pool = mp.Pool(mp.cpu_count())
results = pool.map(get_data_list, [row for _, row in airbnb_data.iterrows()])
pool.close()

final_results = list(chain(*results))
for i in range(len(final_results)):
    if final_results[i]:
        airbnb_data.loc[i, 'sa2_code'] = final_results[i].get('sa2_code', None)
airbnb_data.to_csv("data3/Airbnb_listings_sa2.csv", index=False)
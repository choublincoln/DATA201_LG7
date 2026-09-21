"Lincoln's code"
import pandas as pd
airbnb_data = pd.read_csv("data3/Airbnb_listings_cleaned.csv")
airbnb_data['sa2_code'] = None


#__________________________________________________________________________________________________________________________________________________________
"Daniel's code"

import requests

rnum = len(airbnb_data)
for i in range(rnum):
    lat = airbnb_data.loc[i, 'latitude']
    lon = airbnb_data.loc[i, 'longitude']
    url = f"https://datafinder.stats.govt.nz/services/query/v1/vector.json?key=6bc49b9afc514295a2478b656738aaf8&layer=123515&x={lon}&y={lat}&max_results=3&radius=10000&geometry=true&with_field_names=true"  # Replace with actual API endpoint
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        sa2_code = data.get('sa2_code', None)
        airbnb_data.loc[i, 'sa2_code'] = sa2_code
    else:
        print(f"Failed to retrieve SA2 code for index {i}: {response.status_code}")

airbnb_data.to_csv("data3/Airbnb_listings_sa2.csv", index=False)
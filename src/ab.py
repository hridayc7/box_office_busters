import pandas as pd
import requests
from tqdm import tqdm

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2EzYjE0YmJkYzY5MjcyZmNiMDUwZDI3M2Y3Mjc3ZCIsInN1YiI6IjY1YzZjNjQ0NjgwYmU4MDE3ZWEzNDhhMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NZeryWwYxMP1qjN0Stw33lF7cPmnJBuwmPmguIiIvMs"
}

# Define the function to get actor birthday
def get_actor_birthday(id):
    if id is None:
        return None
    
    url = f"https://api.themoviedb.org/3/person/{id}?language=en-US"
    response = requests.get(url, headers=headers)
    json_response = response.json()
    birthday = json_response.get('birthday', None)
    return birthday

# Read the CSV data into a DataFrame
df = pd.read_csv('/Users/hridayc/Developer/box_office_busters/data/super_regression/combined.csv')

# Iterate through each row and get actor birthdays
actor_birthdays = []
for index, row in tqdm(df.iterrows(), total=len(df), desc="Getting actor birthdays"):
    actor_ids = [row['actor_0_id'], row['actor_1_id'], row['actor_2_id'], row['actor_3_id'], row['actor_4_id']]
    birthdays = [get_actor_birthday(actor_id) for actor_id in actor_ids]
    actor_birthdays.append(birthdays)

# Add the actor birthdays as a new column in the DataFrame
df['actor_birthdays'] = actor_birthdays

# Write the modified DataFrame to a new CSV file
df.to_csv('modified_output.csv', index=False)

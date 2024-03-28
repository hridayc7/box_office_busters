import requests
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
BASE_URL = "https://api.themoviedb.org/3/movie/{id}?language=en-US"
TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2EzYjE0YmJkYzY5MjcyZmNiMDUwZDI3M2Y3Mjc3ZCIsInN1YiI6IjY1YzZjNjQ0NjgwYmU4MDE3ZWEzNDhhMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NZeryWwYxMP1qjN0Stw33lF7cPmnJBuwmPmguIiIvMs"
HEADERS = {"accept": "application/json", "Authorization": f"Bearer {TOKEN}"}

def get_movie_info(tmdb_id):
    # Construct the URL with the TMDB ID
    url = BASE_URL.format(id=tmdb_id)
    # Make the API call
    response = requests.get(url, headers=HEADERS)
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for movie with ID {tmdb_id}: HTTP {response.status_code}")
        return None

def main():
    # Skip the first 25000 rows and read the next 25000 rows of the CSV file into a DataFrame
    # Note: Python ranges are zero-based so the first line of data (after headers) is considered line 0.
    movies_df = pd.read_csv('movies_out.csv', skiprows=range(1, 25001), nrows=25000)

    # Prepare the list to hold movie information
    movie_info_list = []

    # Iterate through DataFrame rows without multithreading
    for index, row in tqdm(movies_df.iterrows(), total=len(movies_df), desc="Fetching movie info"):
        # Get the TMDB ID from the row
        tmdb_id = row['tmdb_id']
        
        # Fetch the movie information using the API
        movie_info = get_movie_info(tmdb_id)
        
        # Add the movie information to the list if it is not None
        if movie_info:
            movie_info_list.append(movie_info)
    
    # Convert the list of dictionaries to a DataFrame
    result_df = pd.json_normalize(movie_info_list)
    
    # Save the DataFrame to a CSV file
    result_df.to_csv('tmdb_info_2.csv', index=False)

if __name__ == "__main__":
    main()




if __name__ == "__main__":
    main()

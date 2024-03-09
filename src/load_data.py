"""
File: load_data.py
Description: This script goes through all the data in the Kaggle dataset (https://www.kaggle.com/datasets/rajugc/imdb-movies-dataset-based-on-genre?resource=download) 
and fetches the tmdb id, movie name and movie release data using the TMDB api.

Our output file is stored in the box_office_busters/data/tmdb_ids.csv
"""

import csv
import os
import requests
import pandas as pd
import tqdm
from tqdm import tqdm



# api headers including user login key for auth
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2EzYjE0YmJkYzY5MjcyZmNiMDUwZDI3M2Y3Mjc3ZCIsInN1YiI6IjY1YzZjNjQ0NjgwYmU4MDE3ZWEzNDhhMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NZeryWwYxMP1qjN0Stw33lF7cPmnJBuwmPmguIiIvMs"
}

def generate_tmdb_url(imdb_id):
    base_url = "https://api.themoviedb.org/3/find/"
    external_source = "external_source=imdb_id"
    return f"{base_url}{imdb_id}?{external_source}"


def fetch_movie_info(imdb_id):

    url = generate_tmdb_url(imdb_id=imdb_id)

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:

        response_json = response.json()

        # handle case movie doesn't exist
        if len(response_json['movie_results']) == 0:
        
            return None, None
    
        
        movie_result = response_json['movie_results'][0]  # Access the first (and only) movie result
        id = movie_result.get('id')
        movie_info = {
            'title': movie_result.get('title'),
            'release_date': movie_result.get('release_date'),
        }
        return id, movie_info
    
    else:
        return None



def load_movie_data():
    print("eeehehehehehhehehEH")

    base_path = '../data/imdb/'

    movie_files = ['action.csv', 'adventure.csv', 'animation.csv', 'biography.csv', 'crime.csv', 'family.csv', 'fantasy.csv', 'film-noir.csv', 'history.csv', 'horror.csv', 'mystery.csv', 'romance.csv', 'scifi.csv', 'sports.csv', 'thriller.csv', 'war.csv']
    
    # this will be used for creating the pandas dataframe -> which we can then output as a csv file
    movie_dict = {}
    

    for file in tqdm(movie_files):

        file_path = os.path.join(base_path, file)
        print(file_path)
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:

                imdb_id = row[0]

                id, movie_info = fetch_movie_info(imdb_id=imdb_id)

                if id is not None:
                    movie_dict[id] = movie_info
                    # print(f"{id}, {movie_info['title']}, {movie_info['release_date']}")
            
    
                    
    print("Finished fetching... creating csv now")
    print(movie_dict)
    df = pd.DataFrame.from_dict(movie_dict, orient='index')
    print(df.head(10))
    df.to_csv('movies_out.csv', index=True)

    return 0


if __name__ == '__main__':
    # Load the movie data
    load_movie_data()

    # movie_info = fetch_movie_info('tt0117705')
    


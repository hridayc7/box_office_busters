import requests
import json
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, List, Set

class CastInfo():
    def __init__(self):
        self.BASE_URL = "https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"
        self.TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2EzYjE0YmJkYzY5MjcyZmNiMDUwZDI3M2Y3Mjc3ZCIsInN1YiI6IjY1YzZjNjQ0NjgwYmU4MDE3ZWEzNDhhMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NZeryWwYxMP1qjN0Stw33lF7cPmnJBuwmPmguIiIvMs"
        self.HEADERS = {"accept": "application/json", "Authorization": f"Bearer {self.TOKEN}"}
        self.TMDB_IDS = pd.read_csv('../data/tmdb/combined_tmdb_data.csv')
        self.ACTORS = self.load_unique_actors_from_file('../data/tmdb/all_actors.txt')

    def get_full_cast(self, tmdb_id:int) -> Optional[dict]:
        # Construct the URL with the TMDB ID
        url = self.BASE_URL.format(id=tmdb_id)
        # Make the API call
        response = requests.get(url, headers=self.HEADERS)
        # Check if the response is successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data for movie with ID {tmdb_id}: HTTP {response.status_code}")
            return None
    
    def get_top_three_actors_by_movie(self, tmdb_id: int) -> Optional[List[str]]:
        try:
            movie = self.get_full_cast(tmdb_id)
            if movie and 'cast' in movie:  # Check if movie is not None and has a 'cast' key
                cast = movie['cast']
                # Ensure cast list is sorted by 'order' and extract top three
                top_three = sorted(cast, key=lambda x: x.get('order', 999))[:3]  # Use 999 as default order value to handle missing 'order'
                top_three_names = [actor['name'] for actor in top_three]
                return top_three_names
        except Exception as e:
            print(f"An error occurred while fetching top three actors for TMDB ID {tmdb_id}: {e}")
        return None

    def get_top_three_actors_all_movies(self) -> Dict[int, List[str]]:
        results = {}
        tmdb_ids = self.TMDB_IDS['id'].tolist() 
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures_list = []
            for tmdb_id in tmdb_ids: 
                future = executor.submit(self.get_top_three_actors_by_movie, tmdb_id)
                futures_list.append((future, tmdb_id))

            for future, tmdb_id in futures_list:
                try:
                    top_three_actors = future.result()
                    if top_three_actors:
                        results[int(tmdb_id)] = top_three_actors
                except Exception as exc:
                    print(f"TMDB ID {tmdb_id} generated an exception: {exc}")
        return results


    def create_actor_set(self) -> Optional[Set]:
        results = self.get_top_three_actors_all_movies()
        unique_actors = set()
        for actors in results.values():
            unique_actors.update(actors)
        return unique_actors

    def get_movie_name_by_id(self, tmdb_id:int) -> Optional[str]:
        name = self.TMDB_IDS[self.TMDB_IDS['id'] == tmdb_id]
        if not name.empty:
            return name.iloc[0]['title']
        else:
            print(f'No movie found for \'{tmdb_id}\'')
            return None
        
    def save_movie_actors_to_json(self, file_path:str)-> None:
        results = self.get_top_three_actors_all_movies()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"Saved results to {file_path}")

    def load_movie_actors_from_json(self, file_path:str) -> Dict[int, List[str]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_unique_actors_to_file(self, file_path:str) -> None:
        unique_actors = self.create_actor_set()
        with open(file_path, 'w', encoding='utf-8') as file:
            for actor in unique_actors:
                file.write(actor+'\n')
        print(f'Saved {len(unique_actors)} to {file_path}')

    def load_unique_actors_from_file(self, file_path:str) -> Set[str]:
        with open(file_path, 'r', encoding='utf-8') as file:
            return {line.strip() for line in file}
    
    def generate_and_save_actor_ids(self, file_path:str):
        actor_ids = {actor_id: actor_name for actor_id, actor_name in enumerate(self.ACTORS)}
        with open(file_path, 'w') as f:
            json.dump(actor_ids, f)
        
        
##cast = CastInfo()
#print(cast.get_full_cast(646389))
#print(cast.get_top_five_actors_by_movie(646389))
#print(cast.get_top_five_actors_all_movies())
#print(len(cast.create_actor_set()))
#cast.save_unique_actors_to_file('../data/tmdb/all_actors.txt')
#cast.save_movie_actors_to_json('../data/tmdb/top_three_actors_by_movie.json')
#cast.generate_and_save_actor_ids('../data/tmdb/actor_ids.json')